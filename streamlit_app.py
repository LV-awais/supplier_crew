__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from main import AiSuppliersCrew
import time
# ---------------------------
# Initialize session state variables if they don't exist
# ---------------------------
if "research_done" not in st.session_state:
    st.session_state.research_done = False
if "result" not in st.session_state:
    st.session_state.result = ""
if "inputs" not in st.session_state:
    st.session_state.inputs = {}

# ---------------------------
# Set up base directory and logo path
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_url = os.path.join(BASE_DIR, "search.jpg")

# ---------------------------
# Environment Setup (API Keys)
# ---------------------------
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]
os.environ["SCRAPFLY_API_KEY"] = st.secrets["SCRAPFLY_API_KEY"]
os.environ["APIVOID_API_KEY"] = st.secrets["APIVOID_API_KEY"]

# ---------------------------
# Set page config with a custom logo and title
# ---------------------------
st.set_page_config(page_title="Supplier Acquisition Tool", layout="wide", page_icon=logo_url)

# ---------------------------
# Custom Styling
# ---------------------------
st.markdown(
    """
    <style>
        .block-container { 
            padding-top: 2rem; 
            padding-bottom: 2rem; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        }
        .custom-header {
            background: linear-gradient(90deg, #1a73e8, #4285f4);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            color: #fff;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .custom-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 600;
        }
        .sidebar .sidebar-content {
            font-family: 'Segoe UI', sans-serif;
        }
        .sidebar-header {
            font-size: 1.3rem; 
            font-weight: 600; 
            color: #1a73e8; 
            margin-bottom: 10px;
        }
        .stButton button {
            background-color: #1a73e8;
            color: #fff;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 1rem;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #135ab6;
        }
        .final-answer-box {
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 8px;
            background-color: #fff;
            margin: 15px 0;
            white-space: pre-wrap;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Header with Logo & Title
# ---------------------------
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo_url, width=120)
with col2:
    st.markdown("<div class='custom-header'><h1>Supplier Acquisition Tool</h1></div>", unsafe_allow_html=True)

# ---------------------------
# Sidebar: Query Input
# ---------------------------
st.sidebar.markdown("<div class='sidebar-header'>Enter Your Search Criteria</div>", unsafe_allow_html=True)
user_query = st.sidebar.text_area("Brand Name", placeholder="Enter the brand or supplier category", height=80)

# Full list of countries (alphabetically sorted)
all_countries = sorted([
    # Africa
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cape Verde",
    "Cameroon", "Central African Republic", "Chad", "Comoros", "Congo", "Democratic Republic of the Congo",
    "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana",
    "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi",
    "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda",
    "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan",
    "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe",

    # Americas
    "Antigua and Barbuda", "Argentina", "Bahamas", "Barbados", "Belize", "Bolivia", "Brazil", "Canada",
    "Chile", "Colombia", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "Ecuador", "El Salvador",
    "Grenada", "Guatemala", "Guyana", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama",
    "Paraguay", "Peru", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines",
    "Suriname", "Trinidad and Tobago", "United States", "Uruguay", "Venezuela",

    # Asia
    "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia",
    "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan",
    "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia",
    "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar",
    "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand",
    "Timor-Leste", "Turkey", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen",

    # Europe
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria",
    "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania",
    "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia",
    "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia",
    "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatican City",

    # Oceania
    "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand",
    "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"
])
selected_country = st.sidebar.selectbox("Select Country", options=all_countries, index=all_countries.index("United States"))

search_button = st.sidebar.button("Search")
status_container = st.empty()

# ---------------------------
# Main Process: Run Supplier Research
# ---------------------------
if search_button:
    if not user_query.strip():
        st.error("⚠ Please enter a valid brand or supplier category.")
    else:
        # Provide immediate feedback to the user
        status_container.markdown("*🔍 Running Supplier Research...*", unsafe_allow_html=True)
        # Store the inputs in session state for persistence
        st.session_state.inputs = {"topic": user_query.strip(), "country": selected_country}
        # Run the research process and store the result in session state
        research_crew = AiSuppliersCrew(st.session_state.inputs)
        st.session_state.result = research_crew.run()
        st.session_state.research_done = True
        # Clear the status container and indicate completion
        status_container.empty()
        status_container.markdown("*✅ Research Complete!*", unsafe_allow_html=True)

# If research has been completed, display the results
if st.session_state.research_done:
    st.markdown("### 📌 Results of Supplier Research:")
    st.markdown(str(st.session_state.result), unsafe_allow_html=True,*,help=None)
