# test.py
#
# Author: Christian Colella
# Created: May 14, 2025
#
# A test suite for the functions implemented for the project.
#

from main import *
from utils import print_color
import os

def test_soap_from_dict():
  """
  Tests the SOAPNote fromDict method.

  Returns:
      bool: True if test passed, false if test failed.
  """
  
  # Construct a test SOAP note
  subjective = 'test subjective'
  objective = 'test objective'
  assessment = 'test assessment'
  plan = 'test plan'
  
  dict = {
    'subjective': subjective,
    'objective': objective,
    'assessment': assessment,
    'plan': plan
  }
  
  soap_note: SOAPNote = SOAPNote.fromDict(dict)
  
  # Ensure properties have expected values
  if soap_note.subjective != subjective:
    return False
  
  if soap_note.objective != objective:
    return False
  
  if soap_note.assessment != assessment:
    return False
  
  if soap_note.plan != plan:
    return False
  
  # Test passed
  return True

def test_read_transcript():
  """
  Tests the read_transcript function.

  Returns:
      bool: True if test passed, false if test failed.
  """
  
  # Path to test text file
  test_filepath = os.getcwd() + '/test/test_transcript.txt'
  
  # The expected value of the transcript read
  expected_str = 'Some text'
  
  # Read the file
  transcript = read_transcript(test_filepath)
  
  # Return true if result matches expectation
  return transcript == expected_str

def test_save_soap_note():
  """
  Tests the save_soap_note function.

  Returns:
      bool: True if test passed, false if test failed.
  """
  
  # Test soap object
  test_soap_note = SOAPNote(
    subjective='test subjective',
    objective='test objective',
    assessment='test assessment',
    plan='test plan'
  )
  
  # Test output file name
  test_filename = 'test_soap_note'
  
  # The expected contents of the SOAP note
  expected_str = """# Generated SOAP Note

## Subjective
test subjective

## Objective
test objective

## Assessment
test assessment

## Plan
test plan"""
  
  # Save the soap note to a file
  save_soap_note(test_soap_note, test_filename)
  
  # Return true if result content matches expectation
  filepath = os.getcwd() + '/generated_soap_notes/test_soap_note.md'
  with open(filepath, 'r') as f:
    content_lines = [line.rstrip() for line in f]
  
  expected_lines = [line.rstrip() for line in expected_str.splitlines()]
  return content_lines == expected_lines
  
def run_test_suite():
  """
  Executes the test suite for this project's functions.
  """
  
  # Print start message
  print_color('Starting test suite...', color='yellow')
  n_passed = 0
  n_total = 0
  
  # soap_from_dict
  if test_soap_from_dict():
    print_color(' PASS: test_soap_from_dict', color='green')
    n_passed += 1
    n_total += 1
  else:
    print_color(' FAIL: test_soap_from_dict', color='red')
    n_total += 1
  
  # read_transcript
  if test_read_transcript():
    print_color(' PASS: test_read_transcript', color='green')
    n_passed += 1
    n_total += 1
  else:
    print_color(' FAIL: test_read_transcript', color='red')
    n_total += 1
  
  # save_soap_note
  if test_save_soap_note():
    print_color(' PASS: test_save_soap_note', color='green')
    n_passed += 1
    n_total += 1
  else:
    print_color(' FAIL: test_save_soap_note', color='red')
    n_total += 1
    
  # Print overall results
  if n_passed == n_total:
    print_color(f'ALL TESTS PASSED!', color='green')
  else:
    print_color(f'{n_passed}/{n_total} TESTS PASSED', color='yellow')
  
run_test_suite()