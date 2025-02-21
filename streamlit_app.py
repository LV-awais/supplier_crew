import os
import streamlit as st
from main import AiSuppliersCrew
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory

logo_url = os.path.join(BASE_DIR, "search.jpg")
# ---------------------------
# Environment Setup (API Keys)
# ---------------------------
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]
# ---------------------------
# Environment Setup (API Keys)

os.environ["SCRAPFLY_API_KEY"] = st.secrets["SCRAPFLY_API_KEY"]  # ✅ Added ScrapeFly API Keylogo_url = os.path.join(BASE_DIR, "search.jpg")
os.environ["APIVOID_API_KEY"] = st.secrets["APIVOID_API_KEY"]
st.set_page_config(page_title="Supplier Acquisition Tool", layout="wide", page_icon=logo_url)

# ---------------------------
# Custom Styling
# ---------------------------
st.markdown(
    """
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 1rem; }
        .dataframe { width: 100% !important; overflow-x: auto; }
        .header { display: flex; align-items: center; justify-content: center; margin-bottom: 10px; }
        .header img { height: 70px; margin-right: 15px; }
        .title { font-size: 2rem; font-weight: bold; color: #2c3e50; }
        .final-answer-box {
            border: 1px solid #ddd; padding: 15px; border-radius: 6px;
            background-color: #fff; margin: 10px 0; white-space: pre-wrap;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1); overflow-x: auto;
        }
        .sidebar-header { font-size: 1.2rem; font-weight: 600; color: #34495e; margin-bottom: 10px; }
        .stButton button { background-color: #2c3e50; color: white; border: none; border-radius: 4px; padding: 10px 16px; font-size: 1rem; }
        .stButton button:hover { background-color: #34495e; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Header with Logo & Title
# ---------------------------
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo_url, width=100)
with col2:
    st.markdown("<h1 class='title'>Supplier Acquisition Tool</h1>", unsafe_allow_html=True)

# ---------------------------
# Sidebar: Query Input
# ---------------------------
st.sidebar.markdown("<div class='sidebar-header'>Enter Your Search Criteria</div>", unsafe_allow_html=True)
user_query = st.sidebar.text_area("Brand Name", placeholder="Enter the brand or supplier category", height=80)

# ---------------------------
# Full List of All Countries
# ---------------------------
all_countries = sorted([
    # 🌍 Africa
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cape Verde",
    "Cameroon", "Central African Republic", "Chad", "Comoros", "Congo", "Democratic Republic of the Congo",
    "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana",
    "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi",
    "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda",
    "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan",
    "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe",

    # 🌎 Americas
    "Antigua and Barbuda", "Argentina", "Bahamas", "Barbados", "Belize", "Bolivia", "Brazil", "Canada",
    "Chile", "Colombia", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "Ecuador", "El Salvador",
    "Grenada", "Guatemala", "Guyana", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama",
    "Paraguay", "Peru", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines",
    "Suriname", "Trinidad and Tobago", "United States", "Uruguay", "Venezuela",

    # 🌏 Asia
    "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia",
    "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan",
    "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia",
    "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar",
    "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand",
    "Timor-Leste", "Turkey", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen",

    # 🌍 Europe
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria",
    "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania",
    "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia",
    "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia",
    "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatican City",

    # 🌏 Oceania
    "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand",
    "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"
])

# Dropdown for country selection
selected_country = st.sidebar.selectbox("Select Country", options=all_countries, index=0)

search_button = st.sidebar.button("Search")
status_container = st.empty()

# ---------------------------
# Function to Run Crew Process
# ---------------------------







if search_button:
    if not user_query.strip():
        st.error("⚠ Please enter a valid brand or supplier category.")
    else:
        status_container.markdown("*🔍 Running Supplier Research...*")

        # ✅ Prepare Inputs
        inputs = {
            "topic": user_query.strip(),
            "country": selected_country }

        # ✅ Run AiSuppliersCrew (from main.py)
        research_crew = AiSuppliersCrew(inputs)
        result = research_crew.run()

        # ✅ Display Results
        st.subheader("📌 Results of Supplier Research:")
        st.write(result)