from crewai import Task
from crewai_tools import SerperDevTool
from custom_tools.custom_tool import CombinedTool
from agents import ai_suppliers_writer, domain_researcher_agent, retrieve_suppliers

# Retrieve Suppliers Task
retrieve_suppliers_task = Task(
    description=(
        "Use the Serper tool to search for suppliers related to the input topic. "
        "Execute multiple search queries using the input topic, for example:\n"
        "- '{topic} reliable, potentials, top-rated potential distributors {country}'\n"
        "- '{topic} reliable, potentials, top-rated suppliers {country}'\n"
        "Aggregate the results into a structured dataset including:\n"
        "- **Supplier name and description except 'Amazon'**\n"
        "- **Main website link**\n"
        "- **Any additional metadata or sitelinks**."
    ),
    expected_output=(
        "A structured JSON containing supplier details:\n"
        "- `business_name`\n"
        "- `url`\n"
        "- `description`\n"
        "- `metadata` (if available)."
    ),
    agent=retrieve_suppliers,  # Uses AI Suppliers Retriever agent
    tools=[SerperDevTool()]  # Uses Serper for searching suppliers
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
ai_suppliers_write_task = Task(
    description=(
        "Review the context you have received and expand each topic into a comprehensive section for a report.\n"
        "DO NOT include Amazon in the report.\n\n"
        "The report should include:\n"
        "- Detailed descriptions of each supplier's business model and offerings.\n"
        "- Supplier's associated URL.\n"
        "- Domain age information (years since registration).\n"
        "- Trustpilot ratings and review insights.\n"
        "- Complete ZoomInfo details including name, URL, founding year, revenue, contact details, address, and other metadata.\n\n"
        "Additionally, include a markdown table summarizing key data:\n"
        "| Supplier Name | URL | Domain Age | Trustpilot Rating | Contact Email | Founding Year | Contact Details | Revenue | Employees | Address |\n"
        "|--------------|-----|------------|------------------|--------------|--------------|---------------|--------|----------|---------|\n"
        "| Example Inc. | www.example.com | 10 years | 4.5/5 | contact@example.com | 2010 | (Phone, Email) | $100M | 500 | 1234 Example St, City, Country |"
    ),
    expected_output=(
        "A structured markdown report containing:\n"
        "- Sections covering each supplier with detailed insights.\n"
        "- Markdown-formatted tables summarizing key data points.\n"
        "- Clear and readable formatting with headings and bullet points."
    ),
    agent=ai_suppliers_writer  # Uses AI Suppliers Writer agent
)

# List of tasks
tasks = [retrieve_suppliers_task, domain_and_trustpilot_researcher_task, ai_suppliers_write_task]
