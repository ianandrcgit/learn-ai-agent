import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

# --- TOOLS ---
def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return f"{result}"
    except Exception as e:
        return f"Error: {e}"

def get_weather(city: str) -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code == 200:
        return f"{data['main']['temp']}°C, {data['weather'][0]['description']}"
    return f"Could not get weather for {city}"

def count_words(text: str) -> str:
    return f"{len(text.split())} words"

def compare_numbers(a: float, b: float) -> str:
    if a > b:
        return f"{a} is greater than {b}"
    elif b > a:
        return f"{b} is greater than {a}"
    return f"{a} and {b} are equal"

# --- TOOL DEFINITIONS ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression"}
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
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_words",
            "description": "Count words in a text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to count"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_numbers",
            "description": "Compare two numbers and find which is greater",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
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
    elif name == "compare_numbers":
        return compare_numbers(args["a"], args["b"])
    return "Unknown tool"

# --- AGENT LOOP ---
def run_agent(question: str, max_iterations: int = 5) -> None:
    print(f"\n{'='*50}")
    print(f"❓ Task: {question}")
    print(f"{'='*50}")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful agent. Use tools to answer questions. "
                      "Use multiple tools if needed. Be thorough and complete."
        },
        {"role": "user", "content": question}
    ]

    iteration = 0

    # --- THE LOOP ---
    while iteration < max_iterations:
        iteration += 1
        print(f"\n🔄 Iteration {iteration}")

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
        messages.append(message)

        # AI used a tool
        if message.get("tool_calls"):
            for tool_call in message["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])

                print(f"🔧 Tool: {tool_name}")
                print(f"📥 Args: {tool_args}")

                tool_result = execute_tool(tool_name, tool_args)
                print(f"📤 Result: {tool_result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": tool_result
                })

        # AI finished — no more tools needed
        else:
            print(f"\n✅ Final Answer: {message['content']}")
            print(f"📊 Completed in {iteration} iteration(s)")
            return

    print(f"\n⚠️ Max iterations reached ({max_iterations})")


# --- RUN ---
run_agent("What is 15 multiplied by 23? Then compare that result with 400.")
run_agent("Get the weather in both London and Bangalore, then tell me which city is warmer.")