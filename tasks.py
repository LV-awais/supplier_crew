from customtools.custom_tools import CombinedTool,SerperSearchTool
from agents import ai_suppliers_writer, domain_researcher_agent, retrieve_suppliers

# Retrieve Suppliers Task
from crewai import Task
from agents import retrieve_suppliers  # Import updated tool

# Updated Retrieve Suppliers Task
retrieve_suppliers_task = Task(
    description=(
        "Use the Serper tool to search for **verified suppliers** related to the input topic.\n"
        "Execute multiple search queries using the input topic, ensuring that results:\n"
        "❌ **EXCLUDE** platforms like Amazon, Reddit, Quora, eBay, Alibaba forums, and other non-supplier sources.\n"
        "✅ **INCLUDE** verified distributors, wholesalers, manufacturers, and direct suppliers.\n"
        "\n"
        "Example queries:\n"
        "- '{topic} trusted distributors, verified suppliers {country}'\n"
        "- '{topic} manufacturers, B2B suppliers {country}'\n"
        "- '{topic} wholesale suppliers, industrial providers {country}'\n"
        "\n"
        "Filter and aggregate the results into a structured dataset including:\n"
        "- **Supplier name (excluding 'Amazon' or other non-suppliers like Reddit,Quora and other forums like research paper)**\n"
        "- **Official website link**\n"
        "- **Relevant metadata like location, industry, and verification badges (if available)**"
    ),
    expected_output=(
        "A structured JSON containing supplier details:\n"
        "- `business_name`\n"
        "- `url`\n"
        "- `description`\n"
        "- `metadata` (if available)."
    ),
    agent=retrieve_suppliers,  # Uses AI Suppliers Retriever agent
    tools=[SerperSearchTool()],  # Now using the improved tool
    inputs={"topic": "electronics manufacturers", "country": "United States"}  # Example input
)


# Domain and Trustpilot Researcher Task
domain_and_trustpilot_researcher_task = Task(
    description=(
        "For each **verified supplier** from the search results, conduct additional research using the CombinedTool:\n"
        "\n"
        "1️ **Domain Age Lookup**\n"
        "- Extract the domain age.\n"
        "- If unavailable, mark as 'Check Manually'.\n"
        "\n"
        "2 **Trustpilot Review Check**\n"
        "- Retrieve Trustpilot ratings and extract 'og:title' + 'AggregateRating'.\n"
        "- If no reviews exist, return 'No Trustpilot Data'.\n"
        "\n"
        "3️ **ZoomInfo Company Lookup**\n"
        "- Extract details: business name, founding year, revenue, headquarters, phone, and contact email.\n"
        "- Include only legitimate **B2B suppliers** (filter out marketplaces like Amazon, eBay, Alibaba, etc.).\n"
        "- If details are missing, return 'Check Manually'."
    ),
    expected_output=(
        "A structured JSON mapping suppliers to their research data, e.g.:\n"
        "{\n"
        "  'Supplier Name': {\n"
        "    'website_url': 'https://www.example.com',\n"
        "    'domain_age': '12 years',\n"
        "    'trustpilot': {'trustpilot_rating': '4.6/5'},\n"
        "    'zoominfo': {\n"
        "      'name': 'SupplierX',\n"
        "      'url': 'www.supplierx.com',\n"
        "      'foundingYear': '1995',\n"
        "      'revenue': '$500M',\n"
        "      'address': '5678 Business Ave, NY, USA',\n"
        "      'contact_number': '+1-555-987-6543',\n"
        "      'contact_email': 'info@supplierx.com'\n"
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
        "Based on the collected data, generate a detailed supplier report **excluding any non-supplier sources**.\n"
        "DO NOT include Amazon, Reddit, Alibaba forums, or any other forums like research papers(etc).\n\n"
        "The report should contain:\n"
        "A structured breakdown of each **verified supplier**, including:\n"
        "- Business overview and key offerings.\n"
        "- Official website link.\n"
        "- Domain age (years since registration).\n"
        "- Trustpilot ratings and review summaries.\n"
        "- Complete ZoomInfo data: company name, founding year, revenue, address, and contact details.\n\n"
        "**Include a markdown summary table for quick reference:**\n"
        "| Supplier Name | URL | Domain Age | Trustpilot Rating | Contact Email | Founding Year | Contact Details | Revenue | Address |\n"
        "|--------------|-----|------------|------------------|--------------|--------------|---------------|--------|---------|\n"
        "| SupplierX | www.supplierx.com | 12 years | 4.6/5 | info@supplierx.com | 1995 | +1-555-987-6543 | $500M | 5678 Business Ave, NY, USA |"
    ),
    expected_output=(
        "A well-formatted markdown report containing:\n"
        "- **Detailed supplier insights** (no forums, no marketplaces).\n"
        "- **A structured table summarizing key data.**"
    ),
    agent=ai_suppliers_writer  # Uses AI Suppliers Writer agent
)

# List of tasks
tasks = [retrieve_suppliers_task, domain_and_trustpilot_researcher_task, ai_suppliers_write_task]
