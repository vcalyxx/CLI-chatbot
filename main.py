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

    response = client.messages.create(
        model="us.anthropic.claude-sonnet-4-6",
        max_tokens=300,
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    print("Claude:", response.content[0].text)

if __name__ == "__main__":
    main()
