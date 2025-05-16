# Cofactor AI MLE Takehome - Part 1
Christian Colella

## Quick Start
1. Place an OpenAI API key in .env defined as `OPENAI_APIKEY`.
2. Run main.py from the project directory.
3. Use the `generate` command to generate a new SOAP note from a transcript file. (e.g. `generate ./transcripts/encounter_1.txt encounter_1`). The SOAP note will be saved as a Markdown file in the `generated_soap_notes` directory.
4. Repeat step 2 for as many SOAP notes as you wish to generate.
5. Use the `exit` command to terminate the program.

## Overall Pipeline Design
1. Define a function that instructs the LLM to extract the SOAP components from relevant text.
2. Read the contents of the transcript file.
3. Call the model with the raw text of the transcript and the function.
4. Parse the response into a custom `SOAPNote` object with each component as a property.
5. Format a Markdown file from the `SOAPNote` object and write to disk.

## Design Rationale

### GPT 4.1 for minimal pre-processing
This model is relatively cheap ($2.00 per 1M tokens) and excellent at providing written responses. GPT 4.1 has a very large context window (1M tokens), which eliminates the need for pre-processing the transcript text. For a less-robust LLM, it may be necessary to split the text into chunks that fit within the model's context window.

### Function calling
Using OpenAI's functions allows for a structured JSON output with a tailored response message for each SOAP component. This design choice enables a separate prompt for each of the components. Engineering a single prompt to force the desired format would be tricky otherwise. Moreover, responses for each component are held separately in the response object with this method, which makes post-processing and formatting much easier than with an aggregate response message.

### Prompt engineering
The core idea is to enable the LLM to organize information from a transcript into the SOAP format. The function schema facilitates this process by providing a clear and action-oriented name and top-level description, concise and domain-specific descriptions for each component, and enforced output structure. Furthermore, the system prompt--"You are a helpful clinical scribe."--primes the model to take the role of a note-taker familiar with medical documentation best practices.

### Post-processing and formatting
The resulting `SOAPNote` object is checked for non-empty values for each of the components, and the program throws an error if any is missing. After all properties are ensured to be present, the object is formatted as a Markdown file, chosen for its simplicity and readability.

## Limitations & Future Improvements

### Context loss
As mentioned, GPT 4.1 has a context window of 1 million tokens. This implementation does not handle the case where this window is (though unlikely) exceeded. Furthermore, earlier versions of GPT have context windows of only a few thousand tokens, which is *often* exceeded by the sample transcript files. An improvement would be a pre-processing procedure to adhere to the context window of the LLM.

### Clinical accuracy
LLMs can hallucinate, and the accuracy of these generated SOAP notes is vital to proper treatment. A future version could highlight some the most uncertain areas for human review.

### Output formatting
The document should include a header with the patient's information and a footer with a signature field. This information would be difficult to reliably infer from the transcript alone, and should be provided separately. It would also likely be helpful if the resulting file type was PDF rather than Markdown.

## References
* Function calling: https://platform.openai.com/docs/guides/function-calling?api-mode=responses
* Prompt engineering: https://platform.openai.com/docs/guides/text?api-mode=responses