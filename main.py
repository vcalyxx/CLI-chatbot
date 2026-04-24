import os
from anthropic import AnthropicBedrock
from dotenv import load_dotenv

load_dotenv()

client = AnthropicBedrock(
    api_key=os.getenv("BEDROCK_API_KEY"),
    aws_region=os.getenv("AWS_REGION", "us-east-1"),
)

# Tool implementation
def get_weather(city):
    return f"Weather in {city} is 35°C"


tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
]


def main():
    system_prompt = (
        "You are a concise AI Engineer assistant. "
        "Use tools when needed for real-world info like weather."
    )

    messages = []

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        # store user message
        messages.append({"role": "user", "content": user_input})

        print("Claude: ", end="", flush=True)

        full_response = ""

        # streaming response
        with client.messages.stream(
            model="us.anthropic.claude-sonnet-4-6",
            max_tokens=300,
            system=system_prompt,
            messages=messages,
            tools=tools,
        ) as stream:

            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text

            print()

            # get structured final response
            response = stream.get_final_message()

        # tool handling
        tool_used = None
        for block in response.content:
            if block.type == "tool_use":
                tool_used = block

        if tool_used:
            tool_name = tool_used.name
            tool_input = tool_used.input

            if tool_name == "get_weather":
                result = get_weather(tool_input["city"])

            # store assistant tool call
            assistant_content = []
            for block in response.content:
                if block.type == "text":
                    assistant_content.append({"type": "text", "text": block.text})
                elif block.type == "tool_use":
                    assistant_content.append({"type": "tool_use", "id": block.id, "name": block.name, "input": block.input})
            messages.append({"role": "assistant", "content": assistant_content})

            # send tool result
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_used.id,
                        "content": result
                    }
                ]
            })

            # get final response after tool result
            final = client.messages.create(
                model="us.anthropic.claude-sonnet-4-6",
                max_tokens=300,
                system=system_prompt,
                messages=messages,
            )

            final_text = final.content[0].text
            print("Claude:", final_text)

            messages.append({
                "role": "assistant",
                "content": final_text
            })

        else:
            # normal flow
            messages.append({
                "role": "assistant",
                "content": full_response
            })


if __name__ == "__main__":
    main()