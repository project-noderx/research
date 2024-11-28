import os
import argparse
import openai

def initialize_openai():
    """Initialize OpenAI API with the provided key."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OpenAI API key not found. Set it as an environment variable: OPENAI_API_KEY")
    print("OpenAI API initialized successfully.")

def diagnose_logs_with_openai(log_file_path):
    """Analyze Ethereum node logs using OpenAI GPT."""
    try:
        # Construct full path to the log file
        logs_dir = os.path.join(os.path.dirname(__file__), "logs")
        log_file_full_path = os.path.join(logs_dir, log_file_path)

        # Read the log file
        with open(log_file_full_path, 'r') as log_file:
            logs = log_file.readlines()

        # Combine logs for analysis
        logs_combined = "\n".join(logs[-20:])  # Reduce to last 20 lines to minimize token usage

        # Prepare prompt for GPT
        prompt = (
            f"The following are Ethereum node logs:\n{logs_combined}\n\n"
            "What issues do you observe, and how can they be resolved?"
        )
        print("Analyzing logs with OpenAI GPT...")

        # Use OpenAI Chat API with reduced max tokens and gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for cost efficiency
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes Ethereum node logs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,  # Reduce to 100 tokens
            temperature=0.7
        )

        return response['choices'][0]['message']['content'].strip()

    except FileNotFoundError:
        return f"Error: Log file '{log_file_path}' not found in 'logs/' directory."
    except Exception as e:
        return f"Error during log analysis: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NodeRx: AI-Powered Ethereum Node Diagnostic Tool using OpenAI GPT")
    parser.add_argument("--log-file", required=True, help="Log file name in the 'logs/' directory (e.g., ethereum-node.log)")
    args = parser.parse_args()

    try:
        # Initialize OpenAI API
        initialize_openai()

        # Run log analysis and print the result
        result = diagnose_logs_with_openai(args.log_file)
        print("\nDiagnosis Result:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
