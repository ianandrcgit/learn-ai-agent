import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

# --- LLM SETUP (new CrewAI style) ---
llm = LLM(
    model=f"openai/{os.getenv('OPENROUTER_MODEL', 'gpt-4o-mini')}",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# --- AGENTS ---
researcher = Agent(
    role="Research Specialist",
    goal="Find accurate and detailed information on any topic",
    backstory="""You are an expert researcher with years of experience
    gathering information. You are thorough, accurate, and always
    provide well-structured findings.""",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Transform research into clear, engaging content",
    backstory="""You are a skilled writer who takes complex research
    and turns it into simple, readable content. You write clearly
    and concisely for a general audience.""",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Review content for accuracy, clarity and completeness",
    backstory="""You are a meticulous reviewer who checks content
    for quality. You ensure information is accurate, well structured,
    and easy to understand. You provide a final quality score.""",
    llm=llm,
    verbose=True
)

# --- TASKS ---
research_task = Task(
    description="""Research the topic: {topic}
    Gather key facts, important points, and relevant information.
    Provide a structured summary of your findings.""",
    expected_output="A detailed research summary with key facts and findings",
    agent=researcher
)

writing_task = Task(
    description="""Using the research provided, write a clear and
    engaging explanation of: {topic}
    Make it easy to understand for a beginner.
    Use simple language and structure it well.""",
    expected_output="A well written, beginner-friendly explanation",
    agent=writer
)

review_task = Task(
    description="""Review the written content about: {topic}
    Check for accuracy, clarity and completeness.
    Provide a quality score out of 10 and brief feedback.""",
    expected_output="Quality review with score out of 10 and feedback",
    agent=reviewer
)

# --- CREW ---
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, writing_task, review_task],
    process=Process.sequential,
    verbose=True
)

# --- RUN ---
print("\n" + "="*50)
print("🚀 Starting Research Crew...")
print("="*50)

result = crew.kickoff(inputs={"topic": "How RAG systems work in AI"})

print("\n" + "="*50)
print("✅ FINAL OUTPUT:")
print("="*50)
print(result)