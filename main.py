# main.py
#
# Author: Christian Colella
# Created: May 14, 2025
#
# Implementation of a program that generates a SOAP note from a clinical visit
# transcript using an LLM.
#

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path

from utils import *

# Use OpenAI's GPT 4.1 LLM
load_dotenv()

client = OpenAI(
  api_key=os.getenv("OPENAI_APIKEY")
)
    
# Define the OpenAI function schema for generating a SOAP note
#   Documentation: https://platform.openai.com/docs/guides/function-calling?api-mode=responses#function-calling-steps
tools = [{
  'type': 'function',
  'name': 'generate_soap_note',
  'description': 'Extract Subjective, Objective, Assessment, and Plan from a clinical transcript',
  'parameters': {
    'type': 'object',
    'properties': {
      # What brings the patient to the doctor's office
      'subjective': {
        'type': 'string',
        'description': 'Patient\'s reported symptoms and concerns'
      },
      
      # What does the doctor observe from the patient's condition
      'objective': {
        'type': 'string',
        'description': 'Vital signs, exam findings, labs, and other observable data'
      },
      
      # What is the diagnosis from the visit
      'assessment': {
        'type': 'string',
        'description': 'Clinical impressions and diagnoses'
      },
      
      # What are the next steps for treatment
      'plan': {
        'type': 'string',
        'description': 'Recommended next steps: tests, therapies, follow-up'
      }
    },
    'required': [
      'subjective',
      'objective',
      'assessment',
      'plan'
    ],
    'additionalProperties': False
  }
}]

# Define a SOAP note object with the desired components
class SOAPNote:
  subjective: str
  objective: str
  assessment: str
  plan: str
  
  # Initialize a SOAP note object from components
  def __init__(self, subjective: str, objective: str, assessment: str, plan: str):
    self.subjective = subjective
    self.objective = objective
    self.assessment = assessment
    self.plan = plan
    
  @staticmethod
  def new():
    return SOAPNote('', '', '', '')
    
  @staticmethod
  def fromDict(dict: dict):
    """
    Method to construct a SOAPNote object from a dictionary with the
    proper fields.

    Args:
        dict (dict): _description_
        
    Returns:
        SOAPNote: The SOAPNote object representation of the dictionary.
    """
    soap_note = SOAPNote.new()
        
    for key in dict:
        setattr(soap_note, key, dict.get(key, None))
        
    return soap_note
    
def read_transcript(filepath: str) -> str:
  """
  Converts a transcript text document into a single string.
  
  Note: GPT 4.1 has a context window of 1 million tokens, which is plenty
  for this application. For a less robust model, chunk the transcript into
  smaller overlapping pieces using tiktoken.

  Args:
      filepath (str): The filepath of the transcript document.

  Returns:
      str: The raw text of the transcript.
  """
  
  with open(filepath, 'r') as f:
    return f.read()

def generate_soap_note(transcript: str) -> SOAPNote:
  """
  Compiles a SOAP note from a doctor's visit transcript.

  Args:
      transcript (str): The raw text of the conversation.

  Returns:
      SOAPNote: The generated SOAP note.
  """
  
  # Define the messages passed to the model
  input_messages = [
    {
      'role': 'system',
      'content': 'You are a helpful clinical scribe.'
    },
    {
      'role': 'user',
      'content': transcript
    }
  ]
  
  # Call the model
  response = client.chat.completions.create(
    model='gpt-4.1',
    messages=input_messages,
    functions=tools,
    function_call='auto'
  )
  
  # Parse the SOAP components from the response and load to SOAPNote object
  msg = response.choices[0].message
  args = json.loads(msg.function_call.arguments)
  
  soap_note: SOAPNote = SOAPNote.fromDict(args)
  
  # Ensure all components are present
  if not soap_note.subjective.strip():
    raise ValueError('LLM returned empty Subjective')
  
  if not soap_note.objective.strip():
    raise ValueError('LLM returned empty objective')
  
  if not soap_note.assessment.strip():
    raise ValueError('LLM returned empty assessment')
  
  if not soap_note.plan.strip():
    raise ValueError('LLM returned empty plan')
  
  # Return the SOAP note
  return soap_note

def save_soap_note(soap_note: SOAPNote, filename: str):
  """
  Creates a Markdown file for the given SOAP note.

  Args:
      soap_note (SOAPNote): The SOAP note to format and save.
      outfile (str): The output filepath.
  """
  
  filepath = os.getcwd() + '/generated_soap_notes/' + filename + '.md'
  
  with open(filepath, 'w') as f:
    f.write('# Generated SOAP Note\n')
    f.write('\n')
    f.write('## Subjective\n')
    f.write(soap_note.subjective + '\n')
    f.write('\n')
    f.write('## Objective\n')
    f.write(soap_note.objective + '\n')
    f.write('\n')
    f.write('## Assessment\n')
    f.write(soap_note.assessment + '\n')
    f.write('\n')
    f.write('## Plan\n')
    f.write(soap_note.plan + '\n')
    
def prompt() -> str:
  """
  Prompts the user to enter a command.

  Returns:
      str: The command input by the user.
  """
  
  print()
  print_color('Commands:', color='yellow')
  print('generate <transcript-filepath> <result-filename>')
  print(' - Generates a SOAP note from the provided transcript file and saves to ./generated_soap_notes/ with the given name')
  print('exit')
  print(' - Terminates the program')
  print()
  print_color('Enter a command:', color='cyan')
  return input('> ')
  
def parse_generate(args: list):
  """
  Executes the workflow that generates and saves a SOAP note from the desired
  transcript file.
  
  Steps:
    1. Get the raw text from the transcript file.
    2. Call the LLM to generate the SOAP note from the text.
    3. Parse the result into a SOAPNote object.
    4. Format the components in a Markdown file and save to disk.

  Args:
      args (list): The list of arguments in the command.
        - 1st argument is 'generate' (the command name)
        - 2nd argument is the transcript filepath
        - 3rd argument is the name of the saved output file
  """
  
  # Ensure correct input
  n_args = len(args)
  
  if n_args < 3:
    print_color(f'Too few arguments in command. Got {n_args}, expected 3', color='red')
    print(' Usage: generate <transcript-filepath> <result-filename>')
    return
  
  if n_args > 3:
    print_color(f'Too many arguments in command. Got {n_args}, expected 3', color='red')
    print(' Usage: generate <transcript-filepath> <result-filename>')
    return
  
  # Get the filepath from user input
  transcript_filepath = Path(args[1])
  
  if not transcript_filepath.exists():
    print_color(f'No such file: {transcript_filepath}')
    return
  
  # Get the output filename from user input
  output_filename = args[2]
  
  # Run the workflow
  transcript = read_transcript(transcript_filepath)
  soap_note = generate_soap_note(transcript)
  save_soap_note(soap_note, output_filename)
  
  print_color(f'Success! Saved as ${output_filename}.md in ./generated_soap_notes/', color='green')

def parse_exit():
  """
  Prints a program exit message to console.
  """
  
  print_color('Goodbye!', color='cyan')
  
def main():
  """
  The main function for the CLI.
  """
  
  print_color('Hello!', color='cyan')
  
  # Loop to prompt input until exit
  while True:
    cmd = prompt()
    args = cmd.split()
    
    if args[0] == 'generate':
      parse_generate(args)
      continue
      
    if args[0] == 'exit':
      parse_exit()
      break
    
    print_color(f'Unknown command: {args[0]}', color='red')
    
main()
    