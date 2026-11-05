import anthropic
from dotenv import load_dotenv

load_dotenv()  # reads the .env file and loads the key into the environment

client = anthropic.Anthropic()

def get_current_time():
    return datetime.now().strftime("%H:%M")

def write_note(text):
    with open("notes.txt", "a") as f:
        f.write(text + "\n")
    return f"Saved: {text}"

# The link YOU build: tool NAME (what the model emits) -> real function.
# The model never sees this dict.
TOOLS_REGISTRY = {
    "get_current_time": get_current_time,
    "write_note": write_note,
}

ALLOWED_TOOLS = {"get_current_time"} #"write_note"}


tools = [
    {
        "name": "get_current_time",
        "description": "Returns the current time as HH:MM",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "write_note",
        "description": "Appends a note to the user's notes file",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string", "description": "The note to save"}},
            "required": ["text"],
        },
    },
]


def run_tool(name, tool_input):
    if name not in ALLOWED_TOOLS:
        return f"Denied: tool '{name}' is not allowed."
    return TOOLS_REGISTRY[name](**tool_input)

def ask(prompt):
    messages = [{"role": "user", "content": prompt}]  # this list IS the memory

    while True:  # this loop IS the agent
        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=300,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            return response.content[0].text  # final text answer

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                output = run_tool(block.name, block.input)  # <- the gate runs here
                print(f"[tool] {block.name} -> {output}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    print(ask("Save a note that says: buy milk"))