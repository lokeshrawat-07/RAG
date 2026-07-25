import os
if "MISTRAL_API_KEY" in os.environ:
    del os.environ["MISTRAL_API_KEY"]

try:
    from langchain_mistralai import ChatMistralAI
    llm = ChatMistralAI(model="mistral-small-latest")
    print("Success")
except Exception as e:
    print(f"Error: {e}")
