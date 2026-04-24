# CLI Chatbot

A simple terminal chatbot built with Claude. It keeps conversation history across turns and supports tool calling, with a weather tool included as an example.

## What it does

- Streams Claude's responses to the terminal as they arrive
- Keeps the full conversation history so Claude has context from earlier messages
- Supports tool calling (currently has a `get_weather` tool)
- Type `exit` or `quit` to stop

## Requirements

- Python 3.8+
- A Claude API key (direct from Anthropic) or an AWS Bedrock account with Claude access

## Setup

1. Clone the repo and create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

**If you're using AWS Bedrock** (what this repo uses by default):

```
BEDROCK_API_KEY=your_key_here
AWS_REGION=us-east-1
```

**If you have a direct Anthropic API key**, swap out the client in `main.py`:

```python
# remove this
from anthropic import AnthropicBedrock
client = AnthropicBedrock(
    api_key=os.getenv("BEDROCK_API_KEY"),
    aws_region=os.getenv("AWS_REGION", "us-east-1"),
)

# use this instead
import anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

And set `ANTHROPIC_API_KEY=your_key_here` in your `.env`. Everything else stays the same.

## Running

```bash
uv run main.py
```

Then just type your messages. Claude will respond and stream the output back. If you ask about the weather for a city, it will call the `get_weather` tool and follow up with a real response.

## Adding more tools

Tools are defined in the `tools` list in `main.py`. Each tool needs a name, description, and input schema. The actual function that runs when the tool is called goes in the `if tool_used:` block in `main()`.

The `get_weather` function is a stub that returns a hardcoded temperature. Replace it with a real weather API call if you need actual data.
