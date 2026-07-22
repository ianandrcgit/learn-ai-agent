import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import operator

load_dotenv()

# Use OpenRouter as backend
llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL", "gpt-4o-mini"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# --- STATE --- (data that flows through the graph)
class AgentState(TypedDict):
    question: str
    tool_result: str
    final_answer: str
    steps: Annotated[list, operator.add]

# --- NODES (steps in the agent) ---
def analyze_node(state: AgentState) -> AgentState:
    print("\n🔍 Node: Analyzing question...")
    question = state["question"]

    response = llm.invoke([
        SystemMessage(content="You analyze questions and decide what calculation or lookup is needed. Be brief."),
        HumanMessage(content=f"What do I need to find out to answer: {question}")
    ])

    print(f"   Analysis: {response.content}")
    return {"steps": [f"Analyzed: {response.content}"]}


def tool_node(state: AgentState) -> AgentState:
    print("\n🔧 Node: Using calculator tool...")
    question = state["question"]

    # Extract numbers and calculate
    import re
    numbers = re.findall(r'\d+', question)

    if len(numbers) >= 2:
        expression = f"{numbers[0]} * {numbers[1]}"
        result = eval(expression)
        tool_result = f"Calculated {expression} = {result}"
    else:
        tool_result = "Could not extract numbers from question"

    print(f"   Result: {tool_result}")
    return {
        "tool_result": tool_result,
        "steps": [f"Tool used: {tool_result}"]
    }


def answer_node(state: AgentState) -> AgentState:
    print("\n✍️ Node: Generating final answer...")
    question = state["question"]
    tool_result = state.get("tool_result", "No tool used")

    response = llm.invoke([
        SystemMessage(content="You give clear, concise answers."),
        HumanMessage(content=f"Question: {question}\nContext: {tool_result}\nGive a clear final answer.")
    ])

    print(f"   Answer: {response.content}")
    return {
        "final_answer": response.content,
        "steps": [f"Answer generated"]
    }


# --- ROUTING (decide what happens next) ---
def should_use_tool(state: AgentState) -> str:
    question = state["question"].lower()
    if any(word in question for word in ["calculate", "multiply", "add", "subtract", "times", "plus"]):
        return "use_tool"
    return "skip_tool"


# --- BUILD THE GRAPH ---
def build_agent():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("analyze", analyze_node)
    graph.add_node("tool", tool_node)
    graph.add_node("answer", answer_node)

    # Set entry point
    graph.set_entry_point("analyze")

    # Add conditional edge
    graph.add_conditional_edges(
        "analyze",
        should_use_tool,
        {
            "use_tool": "tool",
            "skip_tool": "answer"
        }
    )

    # Tool always goes to answer
    graph.add_edge("tool", "answer")
    graph.add_edge("answer", END)

    return graph.compile()


# --- RUN ---
agent = build_agent()

def run(question: str):
    print(f"\n{'='*50}")
    print(f"❓ Question: {question}")
    print(f"{'='*50}")

    result = agent.invoke({
        "question": question,
        "tool_result": "",
        "final_answer": "",
        "steps": []
    })

    print(f"\n📊 Steps taken: {result['steps']}")
    print(f"✅ Final Answer: {result['final_answer']}")


run("Calculate 25 times 48")
run("What is the capital of France?")