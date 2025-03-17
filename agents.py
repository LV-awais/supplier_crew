from crewai import Agent
from .customtools.custom_tools import  SerperSearchTool,CombinedTool

# AI Suppliers Retriever Agent
retrieve_suppliers = Agent(
    role="{topic} AI Suppliers Retriever",
    goal="Uncover cutting-edge developments in {topic}",
    backstory=(
        "You're a seasoned researcher with a knack for uncovering the latest "
        "developments in {topic}. Known for your ability to find the most relevant "
        "information and present it in a clear and concise manner."
    ),
    memory=True,
    allow_delegation=True,
    verbose=True,
    tools=[SerperSearchTool()]  # Uses Serper for search
)

# Domain Researcher Agent
domain_researcher_agent = Agent(
    role="Domain Researcher",
    goal=(
        "Retrieve domain age using the DomainAgeTool and Trustpilot review information "
        "using the CustomTrustpilotTool for the supplier URLs provided by the retrieve_suppliers agent."
    ),
    backstory=(
        "Renowned for your ability to parse JSON responses from API calls and scraped Trustpilot pages, "
        "you extract critical data such as the domain_age parameter for websites and comprehensive review "
        "insights (ratings, review counts, reputation summaries) to help gauge supplier credibility."
    ),
    memory="short_term",
    allow_delegation=True,
    verbose=True,
    tools=[CombinedTool(result_as_answer=True)]  # Uses CombinedTool for domain + Trustpilot research
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
    memory="short_term",
    verbose=True,
)

# List of agents
agents = [retrieve_suppliers, domain_researcher_agent, ai_suppliers_writer]
