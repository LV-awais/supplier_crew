from crewai import Agent, LLM
from crewai_tools.tools.serper_dev_tool.serper_dev_tool import SerperDevTool
from customtools.custom_tools import CombinedTool, SerperSearchTool

# Define LLM instance
gemini_llm = LLM(model="gemini/gemini-2.0-flash")

# AI Suppliers Retriever Agent
retrieve_suppliers = Agent(
    role="{topic} AI Suppliers Retriever",
    goal="Identify and gather detailed information about the best suppliers for {topic} in {country}.",
    backstory=(
        "You are a skilled market researcher specializing in sourcing high-quality "
        "suppliers for {topic}. With extensive experience in supplier evaluation, "
        "you analyze market trends, verify supplier credibility, and ensure "
        "the best options are presented."
    ),
    memory=True,
    allow_delegation=True,
    verbose=True,
    llm=gemini_llm,  # Corrected LLM assignment
    tools=[SerperSearchTool()]  # Ensure this tool is correctly implemented
)

# Domain Researcher Agent
domain_researcher_agent = Agent(
    role="Domain Researcher",
    goal=(
        "Retrieve domain age using the DomainAgeTool and Trustpilot review information "
        "for the supplier URLs provided by the retrieve_suppliers agent."
    ),
    backstory=(
        "Renowned for your ability to parse JSON responses from API calls and scraped Trustpilot pages, "
        "you extract critical data such as the domain_age parameter for websites and comprehensive review "
        "insights (ratings, review counts, reputation summaries) to help gauge supplier credibility."
    ),
    memory=True,  # Corrected memory parameter
    allow_delegation=True,
    verbose=True,
    tools=[CombinedTool(result_as_answer=True)]  # Ensure CombinedTool is correctly implemented
)

# AI Suppliers Research Writer Agent
ai_suppliers_writer = Agent(
    role="AI Suppliers Research Writer",
    goal="Write a **comprehensive and detailed supplier research report** based on gathered data.",
    backstory=(
        "You're an **expert market analyst and technical writer** with a deep understanding of supplier evaluation. "
        "Your expertise lies in **transforming raw supplier data** into **engaging, well-structured, and insightful reports**. "
        "Your reports help **supplier acquisition teams make informed decisions** by providing **strategic insights, "
        "risk assessments, and key recommendations**."
    ),
    memory=True,  # Ensuring memory is properly set
    verbose=True,
)

# List of agents
agents = [retrieve_suppliers, domain_researcher_agent, ai_suppliers_writer]
