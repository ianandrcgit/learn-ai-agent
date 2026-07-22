import os
import asyncio
import json
import requests
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")


async def run():
    # Connect to MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available MCP tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Convert MCP tools to OpenRouter format
            openrouter_tools = []
            for tool in tools_result.tools:
                openrouter_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })

            # Ask AI a question using MCP tools
            question = "Calculate 144 divided by 12, then count the words in 'I am building AI agents with MCP'"
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
                    "tools": openrouter_tools
                }
            )

            data = response.json()
            message = data["choices"][0]["message"]

            if message.get("tool_calls"):
                # Add assistant message ONCE before the loop
                messages.append(message)

                for tool_call in message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = json.loads(tool_call["function"]["arguments"])

                    print(f"\n🔧 AI calling MCP tool: {tool_name}")
                    print(f"📥 Args: {tool_args}")

                    # Call the tool via MCP
                    result = await session.call_tool(tool_name, tool_args)
                    tool_result = result.content[0].text
                    print(f"📤 MCP Result: {tool_result}")

                    # Add each tool result
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": tool_result
                    })

                # Get final answer after ALL tool results are added
                final = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={"model": MODEL, "messages": messages}
                )
                final_data = final.json()

                if "choices" in final_data:
                    answer = final_data["choices"][0]["message"]["content"]
                    print(f"\n✅ Final Answer: {answer}")
                else:
                    print(f"\n⚠️ API Error: {final_data}")

            else:
                print(f"\n✅ Final Answer: {message['content']}")


if __name__ == "__main__":
    asyncio.run(run())