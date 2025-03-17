from crewai import Task
from crewai_tools import SerperDevTool
from customtools.custom_tools import CombinedTool,SerperSearchTool
from agents import ai_suppliers_writer, domain_researcher_agent, retrieve_suppliers

# Retrieve Suppliers Task
retrieve_suppliers_task = Task(
    description=(
        "Use the Serper tool to search for verified **wholesale distributors, suppliers, and manufacturers** "
        "for {topic} in {country}. Focus only on **official supplier directories, verified wholesale distributors, "
        "and manufacturer websites**. Avoid generic e-commerce platforms and marketplaces.\n\n"
        "🚫 **EXCLUDE results from:**\n"
        "- Amazon, Alibaba, eBay,newEgg, LinkedIn, Quora, Reddit, ResearchGate, ScienceDirect, Wikipedia, blogs, and news articles.\n\n"
        "🔍 **Search queries should include:**\n"
        "- 'Official {topic} wholesale distributors {country}'\n"
        "- '{topic} authorized suppliers and distributors {country}'\n"
        "- 'Verified {topic} retailer {country}'\n"
        "Extract the results into a structured dataset including:\n"
        "- **Supplier Name** (Exclude Amazon, Alibaba, etc.)\n"
        "- **Official Website Link**\n"
        "- **Business Type** (e.g., Manufacturer, Distributor, Wholesaler)\n"
        "- **Any Additional Metadata**"
    ),
    expected_output=(
        "A structured JSON containing verified supplier details:\n"
        "- `business_name`\n"
        "- `url`\n"
        "- `business_type` (Manufacturer, Distributor, Wholesaler)\n"
        "- `metadata` (if available)."
    ),
    agent=retrieve_suppliers,
    tools=[SerperSearchTool()]  # Uses Serper search with better filtering
)
# Domain and Trustpilot Researcher Task
domain_and_trustpilot_researcher_task = Task(
    description=(
        "Using the CombinedTool, for each supplier from search results, perform the following:\n"
        "1. Fetch the domain age for the supplier website.\n"
        "   - Ensure the input URL is properly formatted.\n"
        "   - If a lookup fails, record a placeholder ('Check Manually').\n"
        "2. Retrieve Trustpilot review data.\n"
        "   - Extract 'og:title' and 'AggregateRating' data.\n"
        "   - If unavailable, return 'Check Manually'.\n"
        "3. Fetch ZoomInfo company data:\n"
        "   - Extract fields such as name, URL, founding year, revenue, address, and contact number.\n"
        "   - Extract email from the 'emailPatterns' field and include it as both 'contact_email' and 'email'.\n"
        "   - If data is unavailable, record 'Check Manually'."
    ),
    expected_output=(
        "A JSON dictionary mapping each supplier to its research data, for example:\n"
        "{\n"
        "  'Supplier Name': {\n"
        "    'website_url': 'https://www.example.com',\n"
        "    'domain_age': '15 years',\n"
        "    'trustpilot': {'trustpilot_rating': '4.2/5'},\n"
        "    'zoominfo': {\n"
        "      'name': 'Tesla',\n"
        "      'url': 'www.tesla.com',\n"
        "      'foundingYear': '2003',\n"
        "      'revenue': '123',\n"
        "      'address': '19266 Coastal Hwy, Delaware, US',\n"
        "      'contact number': '(302) 786-5213',\n"
        "      'contact_email': 'JSmith@tesla.com',\n"
        "      'email': 'JSmith@tesla.com'\n"
        "    }\n"
        "  }\n"
        "}"
    ),
    agent=domain_researcher_agent,  # Uses Domain Researcher agent
    inputs={"suppliers_data": retrieve_suppliers_task},  # Takes input from retrieve_suppliers_task
    tools=[CombinedTool(result_as_answer=True)]  # Uses CombinedTool for research
)

# AI Suppliers Report Writing Task
from crewai import Task
from agents import ai_suppliers_writer

# AI Suppliers Report Writing Task
ai_suppliers_write_task = Task(
    description=(
        "Generate a **comprehensive supplier research report**, ensuring only **verified distributors, "
        "wholesale suppliers, and manufacturers** are included.\n\n"
        "🚫 **EXCLUDE**: Amazon, eBay,newEgg, Alibaba, Reddit, LinkedIn, Quora, blogs, research papers, and unauthorized sellers.\n\n"
        "✅ **The report should include:**\n"
        "- Verified supplier name & URL.\n"
        "- Business type (Distributor, Manufacturer, Wholesaler).\n"
        "- Domain age verification.\n"
        "- Trustpilot reviews and ratings.\n"
        "- Complete ZoomInfo company details (founding year, revenue, contacts, etc.).\n\n"
        "🔍 **Include a markdown table summarizing key supplier data:**\n"
        "| Supplier Name | URL | Business Type | Domain Age | Trustpilot Rating | Contact Email | Founding Year | Revenue | Address |\n"
        "|--------------|-----|--------------|------------|------------------|--------------|--------------|--------|---------|"
    ),
    expected_output=(
        "A structured markdown report with:\n"
        "- Supplier profiles and business details.\n"
        "- Markdown tables summarizing supplier credibility.\n"
        "- Clear formatting with headers and bullet points."
    ),
    agent=ai_suppliers_writer
)


# List of tasks
tasks = [retrieve_suppliers_task, domain_and_trustpilot_researcher_task, ai_suppliers_write_task]
