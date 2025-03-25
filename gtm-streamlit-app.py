import streamlit as st
import openai
import json
import os
from fpdf import FPDF

# Set page config
st.set_page_config(page_title="GTM Launch Tool", layout="wide")

st.title("🚀 GTM Launch Tool")
st.write("Create a structured Go-To-Market strategy in minutes.")

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.error("OpenAI API Key is missing. Please set it in your environment variables.")

# Session state initialization
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'playbook_generated' not in st.session_state:
    st.session_state.playbook_generated = ""

def generate_playbook(form_data):
    """Generates a GTM Playbook using OpenAI."""
    prompt = f"""
    Generate a GTM launch playbook based on these inputs:
    
    ## Product & Market Fit
    - Product Name: {form_data.get('productName', 'N/A')}
    - Product Type: {form_data.get('productType', 'N/A')}
    - Target Audience: {form_data.get('targetAudience', 'N/A')}
    - Primary Value Proposition: {form_data.get('primaryValueProp', 'N/A')}
    - Secondary Benefits: {form_data.get('secondaryBenefits', 'N/A')}

    ## Competition & Pricing
    - Competitors: {form_data.get('competitors', 'N/A')}
    - Market Maturity: {form_data.get('marketMaturity', 'N/A')}
    - Pricing Model: {form_data.get('pricingModel', 'N/A')}
    - Price Point: {form_data.get('pricePoint', 'N/A')}

    ## Sales & Budget
    - Sales Cycle: {form_data.get('salesCycle', 'N/A')}
    - Launch Budget: {form_data.get('launchBudget', 'N/A')}
    - Timeline: {form_data.get('timelineConstraints', 'N/A')}
    - Technical Complexity: {form_data.get('technicalComplexity', 'N/A')}

    ## Expansion & Execution
    - Existing Customer Base: {form_data.get('existingCustomerBase', 'No')}
    - Geographic Focus: {form_data.get('geographicFocus', 'N/A')}
    - Industry Focus: {form_data.get('industryFocus', 'N/A')}
    - Team Size: {form_data.get('teamSize', 'N/A')}

    Provide:
    - Prelaunch, Launch, and Postlaunch strategies
    - Primary and secondary channel recommendations
    - Budget allocation based on the value proposition
    - A cold email/message for outreach
    - Success metrics (KPIs)
    - Potential risks and how to mitigate them
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an expert GTM strategist."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

def save_playbook_as_pdf(content, filename="GTM_Playbook.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename)
    return filename

# Navigation
if st.session_state.step == 1:
    st.header("📌 Product & Market Fit")
    st.session_state.form_data['productName'] = st.text_input("Product Name")
    st.session_state.form_data['productType'] = st.selectbox("Product Type", ["SaaS", "Fintech", "Healthtech", "Martech", "Other"])
    st.session_state.form_data['targetAudience'] = st.selectbox("Target Audience", ["Gen Z", "Millennials", "Gen Alpha", "Founders", "Sales Leaders"])
    st.session_state.form_data['primaryValueProp'] = st.text_area("Primary Value Proposition")
    st.session_state.form_data['secondaryBenefits'] = st.text_area("Secondary Benefits")
    if st.button("Next →"):
        st.session_state.step = 2

elif st.session_state.step == 2:
    st.header("📌 Competition & Pricing")
    st.session_state.form_data['competitors'] = st.text_area("Competitors")
    st.session_state.form_data['marketMaturity'] = st.selectbox("Market Maturity", ["Emerging", "Growing", "Mature"])
    st.session_state.form_data['pricingModel'] = st.selectbox("Pricing Model", ["Freemium", "Subscription", "One-time Payment"])
    st.session_state.form_data['pricePoint'] = st.text_input("Price Point")
    if st.button("← Back"):
        st.session_state.step = 1
    if st.button("Next →"):
        st.session_state.step = 3

elif st.session_state.step == 3:
    st.header("📌 Sales & Budget")
    st.session_state.form_data['salesCycle'] = st.selectbox("Sales Cycle", ["Short (2 days - 3 weeks)", "Medium (1-3 months)", "Long (3-6 months)"])
    st.session_state.form_data['launchBudget'] = st.text_input("Launch Budget")
    st.session_state.form_data['timelineConstraints'] = st.text_input("Launch Timeline")
    st.session_state.form_data['technicalComplexity'] = st.text_area("Technical Complexity")
    if st.button("← Back"):
        st.session_state.step = 2
    if st.button("Next →"):
        st.session_state.step = 4

elif st.session_state.step == 4:
    st.header("📌 Expansion & Execution")
    st.session_state.form_data['existingCustomerBase'] = st.checkbox("Do you have an existing customer base?")
    st.session_state.form_data['geographicFocus'] = st.text_input("Geographic Focus")
    st.session_state.form_data['industryFocus'] = st.text_input("Industry Focus")
    st.session_state.form_data['teamSize'] = st.text_input("Team Size")
    if st.button("← Back"):
        st.session_state.step = 3
    if st.button("Generate GTM Playbook 🚀"):
        with st.spinner("Generating playbook..."):
            st.session_state.playbook_generated = generate_playbook(st.session_state.form_data)
            save_playbook_as_pdf(st.session_state.playbook_generated)
        st.success("Playbook generated successfully! Download below.")
        st.download_button("📥 Download PDF", "GTM_Playbook.pdf", "application/pdf")

st.write(st.session_state.playbook_generated)
