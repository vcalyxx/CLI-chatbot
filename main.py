import os
from anthropic import AnthropicBedrock
from dotenv import load_dotenv

load_dotenv()

client = AnthropicBedrock(
    api_key=os.getenv("BEDROCK_API_KEY"),
    aws_region=os.getenv("AWS_REGION", "us-east-1"),
)

def main():
    user_input = input("You: ")

    print("Claude: ", end="", flush=True)

    with client.messages.stream(
        model="us.anthropic.claude-sonnet-4-6",
        max_tokens=300,
        messages=[
            {"role": "user", "content": user_input}
        ]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()

if __name__ == "__main__":
    main()
