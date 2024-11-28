from transformers import pipeline
try:
    pipe = pipeline("text2text-generation")
    print("Pipeline initialized successfully.")
except Exception as e:
    print(f"Pipeline initialization failed: {e}")
