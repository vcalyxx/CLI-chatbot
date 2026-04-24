import os
from anthropic import AnthropicBedrock
from dotenv import load_dotenv

load_dotenv()

client = AnthropicBedrock(
    api_key=os.getenv("BEDROCK_API_KEY"),
    aws_region=os.getenv("AWS_REGION", "us-east-1"),
)

def main():
    messages = []

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        # add user message to the history
        messages.append({"role": "user", "content": user_input})

        print("Claude: ", end="", flush=True)

        full_response = ""

        with client.messages.stream(
            model="us.anthropic.claude-sonnet-4-6",
            max_tokens=300,
            messages=messages
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text
        print()

        # add assistant response to the history
        messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
