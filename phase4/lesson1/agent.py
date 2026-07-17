import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

# --- TOOLS (functions AI can call) ---
def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

def get_weather(city: str) -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code == 200:
        return f"Weather in {city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
    return f"Could not get weather for {city}"

def count_words(text: str) -> str:
    count = len(text.split())
    return f"Word count: {count}"

# --- TOOL DEFINITIONS (tells AI what tools exist) ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression e.g. 2+2 or 10*5"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name e.g. London"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_words",
            "description": "Count the number of words in a text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to count words in"
                    }
                },
                "required": ["text"]
            }
        }
    }
]

# --- TOOL EXECUTOR ---
def execute_tool(name: str, args: dict) -> str:
    if name == "calculate":
        return calculate(args["expression"])
    elif name == "get_weather":
        return get_weather(args["city"])
    elif name == "count_words":
        return count_words(args["text"])
    return "Unknown tool"

# --- AGENT ---
def run_agent(question: str) -> None:
    print(f"\n❓ Question: {question}")

    messages = [{"role": "user", "content": question}]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": messages,
            "tools": tools
        }
    )

    data = response.json()
    message = data["choices"][0]["message"]

    # AI decided to use a tool
    if message.get("tool_calls"):
        tool_call = message["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        tool_args = json.loads(tool_call["function"]["arguments"])

        print(f"🔧 AI is using tool: {tool_name}")
        print(f"📥 With args: {tool_args}")

        tool_result = execute_tool(tool_name, tool_args)
        print(f"📤 Tool result: {tool_result}")

        # Send tool result back to AI for final answer
        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": tool_result
        })

        final = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={"model": MODEL, "messages": messages}
        )
        final_data = final.json()
        answer = final_data["choices"][0]["message"]["content"]
        print(f"🤖 Answer: {answer}")

    else:
        print(f"🤖 Answer: {message['content']}")


# --- RUN ---
run_agent("What is 25 multiplied by 48?")
run_agent("What is the weather in Bangalore?")
run_agent("Count the words in: I am learning AI development in 2026")