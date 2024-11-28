import os
from transformers import pipeline
import torch


def initialize_model():
    print("Initializing AI model...")
    model_id = "meta-llama/Llama-3.2-3B"
    try:
        llm_pipeline = pipeline("text-generation", model=model_id)
        print("AI model initialized successfully.")
        return llm_pipeline
    except Exception as e:
        print(f"Error initializing model: {e}")
        exit(1)


def diagnose_logs_with_ai(log_file_path, llm_pipeline):
    """Diagnose Ethereum node logs using AI."""
    try:
        # Read the log file from the provided path
        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()

        # Combine logs for analysis
        logs_combined = "\n".join(line for line in logs if "ERROR" in line or "FATAL" in line)[-50:]
        prompt = f"Analyze the following Ethereum node error logs:\n{logs_combined}\n\n" \
                  "Identify the error, explain its potential cause, and provide a step-by-step resolution."
        print("Analyzing logs with AI...")


        # Use the pipeline to generate a response
        response = llm_pipeline(prompt, max_new_tokens=500, truncation=True)

        return response[0]["generated_text"]
    except FileNotFoundError:
        return f"Error: Log file '{log_file_path}' not found."
    except Exception as e:
        return f"Error during log analysis: {e}"


if __name__ == "__main__":
    # Define the log file path
    log_file_path = "/content/ethereum-node.log"

    # Initialize the AI model
    print("Setting up the model...")
    llm_pipeline = initialize_model()

    # Run log analysis and print the result
    result = diagnose_logs_with_ai(log_file_path, llm_pipeline)
    print("\nDiagnosis Result:")
    print(result)
