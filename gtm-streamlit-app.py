import streamlit as st
import openai
import os
from fpdf import FPDF
import base64
from io import BytesIO

# Set page config with enhanced styling
st.set_page_config(
    page_title="GTM Launch Playbook Generator", 
    page_icon="🚀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main-container {
        background-color: #f4f6f9;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stApp {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        transform: scale(1.05);
    }
    .step-header {
        color: #2c3e50;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .generated-playbook {
        background-color: #ecf0f1;
        padding: 1.5rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'playbook_generated' not in st.session_state:
    st.session_state.playbook_generated = ""

# OpenAI API Key Configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.error("OpenAI API Key is missing. Please set it in your environment variables.")

def generate_playbook(form_data):
    """Enhanced playbook generation with detailed prompt"""
    prompt = f"""
    Create a comprehensive Go-To-Market (GTM) Playbook with the following strategic insights:

    🔹 PRODUCT OVERVIEW
    - Product Name: {form_data.get('productName', 'N/A')}
    - Product Type: {form_data.get('productType', 'N/A')}
    - Target Audience: {form_data.get('targetAudience', 'N/A')}

    🔹 VALUE PROPOSITION
    Primary Value Prop: {form_data.get('primaryValueProp', 'N/A')}
    Secondary Benefits: {form_data.get('secondaryBenefits', 'N/A')}

    🔹 MARKET LANDSCAPE
    - Competitors: {form_data.get('competitors', 'N/A')}
    - Market Maturity: {form_data.get('marketMaturity', 'N/A')}
    - Pricing Strategy: {form_data.get('pricingModel', 'N/A')} at {form_data.get('pricePoint', 'N/A')}

    🔹 GO-TO-MARKET STRATEGY
    Detailed execution plan considering:
    - Sales Cycle: {form_data.get('salesCycle', 'N/A')}
    - Launch Budget: {form_data.get('launchBudget', 'N/A')}
    - Geographic Focus: {form_data.get('geographicFocus', 'N/A')}

    Provide a structured playbook with:
    1. Comprehensive market analysis
    2. Detailed launch strategy
    3. Channel and distribution plan
    4. Pricing and positioning strategy
    5. Sales and marketing alignment
    6. Key performance indicators (KPIs)
    7. Risk mitigation strategies
    8. 90-day post-launch roadmap
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a world-class GTM strategy consultant creating a comprehensive launch playbook."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

def create_beautifully_formatted_pdf(content):
    """Create a visually appealing PDF"""
    pdf = FPDF()
    pdf.add_page()
    
    # Title Page
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(41, 128, 185)  # Blue color
    pdf.cell(0, 20, 'GTM Launch Playbook', ln=True, align='C')
    
    # Add content
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)  # Black color
    pdf.multi_cell(0, 10, content)
    
    # Save to buffer
    buffer = BytesIO()
    pdf.output(buffer, 'F')
    buffer.seek(0)
    return buffer

# Multi-step form with enhanced UI
def render_form():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    if st.session_state.step == 1:
        st.markdown('<h2 class="step-header">📌 Product & Market Fundamentals</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.form_data['productName'] = st.text_input("🏷️ Product Name")
            st.session_state.form_data['productType'] = st.selectbox("🔧 Product Type", 
                ["SaaS", "Fintech", "Healthtech", "Martech", "E-commerce", "Enterprise Software", "Other"])
        
        with col2:
            st.session_state.form_data['targetAudience'] = st.selectbox("🎯 Target Audience", 
                ["Startups", "Enterprise", "SMBs", "Developers", "Marketing Professionals", "Founders", "Other"])
            st.session_state.form_data['marketMaturity'] = st.selectbox("🌐 Market Maturity", 
                ["Emerging", "Growth", "Mature", "Saturated"])
        
        st.session_state.form_data['primaryValueProp'] = st.text_area("✨ Primary Value Proposition")
        st.session_state.form_data['secondaryBenefits'] = st.text_area("🌟 Secondary Benefits")
        
        if st.button("Next Step →"):
            st.session_state.step = 2

    elif st.session_state.step == 2:
        st.markdown('<h2 class="step-header">💰 Competitive & Financial Strategy</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.form_data['competitors'] = st.text_area("🥊 Direct Competitors")
            st.session_state.form_data['pricingModel'] = st.selectbox("💳 Pricing Model", 
                ["Freemium", "Subscription", "Tiered", "Usage-based", "One-time"])
        
        with col2:
            st.session_state.form_data['pricePoint'] = st.text_input("💲 Estimated Price Point")
            st.session_state.form_data['salesCycle'] = st.selectbox("⏱️ Sales Cycle Length", 
                ["Short (1-3 weeks)", "Medium (1-3 months)", "Long (3-6 months)"])
        
        st.session_state.form_data['launchBudget'] = st.text_input("💸 Launch Budget")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous Step"):
                st.session_state.step = 1
        with col2:
            if st.button("Next Step →"):
                st.session_state.step = 3

    elif st.session_state.step == 3:
        st.markdown('<h2 class="step-header">🌍 Execution & Expansion Strategy</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.form_data['geographicFocus'] = st.selectbox("🌐 Geographic Focus", 
                ["Local", "National", "North America", "Europe", "APAC", "Global"])
            st.session_state.form_data['industryFocus'] = st.text_input("🏢 Target Industries")
        
        with col2:
            st.session_state.form_data['teamSize'] = st.selectbox("👥 Team Size", 
                ["1-5", "6-10", "11-25", "26-50", "50+"])
            st.session_state.form_data['timelineConstraints'] = st.date_input("🗓️ Preferred Launch Date")
        
        st.session_state.form_data['technicalComplexity'] = st.text_area("🔬 Technical Complexity & Integration Requirements")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous Step"):
                st.session_state.step = 2
        with col2:
            if st.button("Generate GTM Playbook 🚀"):
                with st.spinner("Crafting your GTM Playbook..."):
                    st.session_state.playbook_generated = generate_playbook(st.session_state.form_data)
                    playbook_pdf = create_beautifully_formatted_pdf(st.session_state.playbook_generated)
                
                st.success("🎉 Playbook Generated Successfully!")
                st.download_button(
                    label="📥 Download Comprehensive GTM Playbook",
                    data=playbook_pdf,
                    file_name="GTM_Playbook.pdf",
                    mime="application/pdf"
                )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main App
def main():
    st.title("🚀 GTM Launch Playbook Generator")
    st.write("Craft a data-driven Go-To-Market strategy in minutes")
    
    render_form()

    # Optional: Display generated playbook
    if st.session_state.playbook_generated:
        st.markdown('<div class="generated-playbook">', unsafe_allow_html=True)
        st.markdown("### 📄 Generated Playbook Preview")
        st.write(st.session_state.playbook_generated)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
