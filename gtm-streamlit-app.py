import streamlit as st
import openai
import os
from fpdf import FPDF
import base64
from io import BytesIO
from datetime import date

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

# Initialize session state properly - only set defaults if not already in session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'productName': '',
        'productType': 'SaaS',
        'targetAudience': 'Startups',
        'marketMaturity': 'Emerging',
        'primaryValueProp': '',
        'secondaryBenefits': '',
        'competitors': '',
        'pricingModel': 'Freemium',
        'pricePoint': '',
        'salesCycle': 'Short (1-3 weeks)',
        'launchBudget': '',
        'geographicFocus': 'Local',
        'industryFocus': '',
        'teamSize': '1-5',
        'timelineConstraints': None,
        'technicalComplexity': ''
    }
if 'playbook_generated' not in st.session_state:
    st.session_state.playbook_generated = ""
if 'pdf_buffer' not in st.session_state:
    st.session_state.pdf_buffer = None

# Navigation functions
def go_to_next_step():
    st.session_state.step += 1

def go_to_previous_step():
    st.session_state.step -= 1

# OpenAI API Key Configuration
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    if 'OPENAI_API_KEY' not in st.session_state:
        st.session_state.OPENAI_API_KEY = None
    
    if not st.session_state.OPENAI_API_KEY:
        api_key = st.text_input("OpenAI API Key is missing. Please enter your API key:", type="password")
        if api_key:
            st.session_state.OPENAI_API_KEY = api_key
    
    openai_api_key = st.session_state.OPENAI_API_KEY

def generate_playbook(form_data):
    """Enhanced playbook generation with detailed prompt"""
    if not openai_api_key:
        return "Error: OpenAI API Key is missing. Please provide it to generate the playbook."
    
    openai.api_key = openai_api_key
    
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
    - Industry Focus: {form_data.get('industryFocus', 'N/A')}
    - Team Size: {form_data.get('teamSize', 'N/A')}
    - Technical Complexity: {form_data.get('technicalComplexity', 'N/A')}

    Format the content with clear sections, each with a headline and 2-3 lines of explanatory notes below it. Make sure it's well-organized for PDF formatting.
    
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
    
    try:
        client = openai.OpenAI(api_key=openai_api_key)
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a world-class GTM strategy consultant creating a comprehensive launch playbook. Format your response with clear section headings and brief explanatory notes."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating playbook: {str(e)}"

@st.cache_data
def create_beautifully_formatted_pdf(content, form_data):
    """Create a visually appealing PDF with enhanced formatting - with caching"""
    class PDF(FPDF):
        def header(self):
            # Logo (placeholder)
            self.set_font('Arial', 'B', 15)
            self.set_text_color(41, 128, 185)  # Blue color
            self.cell(0, 10, 'GTM LAUNCH PLAYBOOK', 0, 1, 'R')
            self.ln(5)
            
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
            
        def chapter_title(self, title):
            self.set_font('Arial', 'B', 16)
            self.set_fill_color(41, 128, 185)  # Blue background
            self.set_text_color(255, 255, 255)  # White text
            self.cell(0, 10, title, 0, 1, 'L', 1)
            self.ln(4)
            
        def section_title(self, title):
            self.set_font('Arial', 'B', 14)
            self.set_text_color(41, 128, 185)  # Blue text
            self.cell(0, 8, title, 0, 1, 'L')
            self.ln(2)
            
        def body_text(self, text):
            self.set_font('Arial', '', 11)
            self.set_text_color(0)
            self.multi_cell(0, 6, text)
            self.ln(3)
            
        def note_box(self, text):
            self.set_font('Arial', 'I', 10)
            self.set_text_color(80, 80, 80)  # Dark gray
            self.set_draw_color(200, 200, 200)  # Light gray border
            self.set_fill_color(245, 245, 245)  # Very light gray background
            self.multi_cell(0, 6, text, 1, 'L', 1)
            self.ln(4)
            
        def info_box(self, title, content):
            self.set_draw_color(41, 128, 185)  # Blue border
            self.set_fill_color(235, 245, 251)  # Light blue background
            self.rect(10, self.get_y(), 190, 30, 'DF')
            
            # Title
            self.set_font('Arial', 'B', 12)
            self.set_text_color(41, 128, 185)
            self.set_xy(15, self.get_y() + 5)
            self.cell(0, 5, title, 0, 1)
            
            # Content
            self.set_font('Arial', '', 10)
            self.set_text_color(80, 80, 80)
            self.set_xy(15, self.get_y() + 2)
            self.multi_cell(180, 5, content, 0)
            self.ln(5)
            
    # Create PDF instance
    pdf = PDF()
    pdf.add_page()
    
    # Cover Page
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(41, 128, 185)  # Blue color
    pdf.cell(0, 40, '', 0, 1)  # Add space
    pdf.cell(0, 20, 'GO-TO-MARKET', 0, 1, 'C')
    pdf.cell(0, 20, 'LAUNCH PLAYBOOK', 0, 1, 'C')
    
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(80, 80, 80)  # Dark gray
    pdf.cell(0, 15, f"For: {form_data.get('productName', 'Your Product')}", 0, 1, 'C')
    
    # Add current date
    today = date.today().strftime("%B %d, %Y")
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Generated on: {today}", 0, 1, 'C')
    
    # Add a border around the cover page
    pdf.set_draw_color(41, 128, 185)  # Blue border
    pdf.rect(10, 10, 190, 277, 'D')  # Draw border
    
    # Product Overview Page
    pdf.add_page()
    pdf.chapter_title('PRODUCT OVERVIEW')
    
    # Summary box
    pdf.info_box("EXECUTIVE SUMMARY", 
                f"Product: {form_data.get('productName', 'N/A')} | Type: {form_data.get('productType', 'N/A')} | Target: {form_data.get('targetAudience', 'N/A')}")
    
    # Main content
    sections = content.split('\n\n')
    for section in sections:
        if section.strip():
            if section.startswith('#'):  # Section title
                title = section.strip('#').strip()
                pdf.section_title(title)
            elif section.startswith('>'):  # Note
                note = section.strip('>').strip()
                pdf.note_box(note)
            else:
                # Check if this might be a subsection
                lines = section.split('\n')
                if len(lines) > 0 and any(l.startswith('##') for l in lines):
                    for line in lines:
                        if line.startswith('##'):
                            subtitle = line.strip('#').strip()
                            pdf.set_font('Arial', 'B', 12)
                            pdf.set_text_color(60, 60, 60)
                            pdf.cell(0, 6, subtitle, 0, 1)
                        else:
                            pdf.set_font('Arial', '', 11)
                            pdf.set_text_color(0)
                            pdf.multi_cell(0, 6, line)
                else:
                    pdf.body_text(section)
    
    # Save to buffer
    buffer = BytesIO()
    pdf.output(buffer, 'F')
    buffer.seek(0)
    return buffer

def generate_playbook_flow():
    """Handle the playbook generation workflow"""
    with st.spinner("Crafting your GTM Playbook..."):
        st.session_state.playbook_generated = generate_playbook(st.session_state.form_data)
        if not st.session_state.playbook_generated.startswith("Error"):
            st.session_state.pdf_buffer = create_beautifully_formatted_pdf(
                st.session_state.playbook_generated, 
                st.session_state.form_data
            )
    
    if st.session_state.playbook_generated.startswith("Error"):
        st.error(st.session_state.playbook_generated)
    else:
        st.success("🎉 Playbook Generated Successfully!")
        if st.session_state.pdf_buffer:
            st.download_button(
                label="📥 Download Comprehensive GTM Playbook",
                data=st.session_state.pdf_buffer,
                file_name=f"{st.session_state.form_data.get('productName', 'GTM')}_Playbook.pdf",
                mime="application/pdf"
            )

# Multi-step form with enhanced UI
def render_form():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    if st.session_state.step == 1:
        st.markdown('<h2 class="step-header">📌 Product & Market Fundamentals</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input(
                "🏷️ Product Name", 
                value=st.session_state.form_data['productName'],
                key="product_name_input"
            )
            st.session_state.form_data['productName'] = product_name
            
            product_type = st.selectbox(
                "🔧 Product Type", 
                ["SaaS", "Fintech", "Healthtech", "Martech", "E-commerce", "Enterprise Software", "Other"],
                index=["SaaS", "Fintech", "Healthtech", "Martech", "E-commerce", "Enterprise Software", "Other"].index(
                    st.session_state.form_data['productType']
                ),
                key="product_type_select"
            )
            st.session_state.form_data['productType'] = product_type
        
        with col2:
            target_audience = st.selectbox(
                "🎯 Target Audience", 
                ["Startups", "Enterprise", "SMBs", "Developers", "Marketing Professionals", "Founders", "Other"],
                index=["Startups", "Enterprise", "SMBs", "Developers", "Marketing Professionals", "Founders", "Other"].index(
                    st.session_state.form_data['targetAudience']
                ),
                key="target_audience_select"
            )
            st.session_state.form_data['targetAudience'] = target_audience
            
            market_maturity = st.selectbox(
                "🌐 Market Maturity", 
                ["Emerging", "Growth", "Mature", "Saturated"],
                index=["Emerging", "Growth", "Mature", "Saturated"].index(
                    st.session_state.form_data['marketMaturity']
                ),
                key="market_maturity_select"
            )
            st.session_state.form_data['marketMaturity'] = market_maturity
        
        primary_value_prop = st.text_area(
            "✨ Primary Value Proposition", 
            value=st.session_state.form_data['primaryValueProp'],
            key="primary_value_prop_textarea"
        )
        st.session_state.form_data['primaryValueProp'] = primary_value_prop
        
        secondary_benefits = st.text_area(
            "🌟 Secondary Benefits", 
            value=st.session_state.form_data['secondaryBenefits'],
            key="secondary_benefits_textarea"
        )
        st.session_state.form_data['secondaryBenefits'] = secondary_benefits
        
        if st.button("Next Step →", key="next_step_1"):
            go_to_next_step()
            st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<h2 class="step-header">💰 Competitive & Financial Strategy</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            competitors = st.text_area(
                "🥊 Direct Competitors", 
                value=st.session_state.form_data['competitors'],
                key="competitors_textarea"
            )
            st.session_state.form_data['competitors'] = competitors
            
            pricing_model = st.selectbox(
                "💳 Pricing Model", 
                ["Freemium", "Subscription", "Tiered", "Usage-based", "One-time"],
                index=["Freemium", "Subscription", "Tiered", "Usage-based", "One-time"].index(
                    st.session_state.form_data['pricingModel']
                ),
                key="pricing_model_select"
            )
            st.session_state.form_data['pricingModel'] = pricing_model
        
        with col2:
            price_point = st.text_input(
                "💲 Estimated Price Point", 
                value=st.session_state.form_data['pricePoint'],
                key="price_point_input"
            )
            st.session_state.form_data['pricePoint'] = price_point
            
            sales_cycle = st.selectbox(
                "⏱️ Sales Cycle Length", 
                ["Short (1-3 weeks)", "Medium (1-3 months)", "Long (3-6 months)"],
                index=["Short (1-3 weeks)", "Medium (1-3 months)", "Long (3-6 months)"].index(
                    st.session_state.form_data['salesCycle']
                ),
                key="sales_cycle_select"
            )
            st.session_state.form_data['salesCycle'] = sales_cycle
        
        launch_budget = st.text_input(
            "💸 Launch Budget", 
            value=st.session_state.form_data['launchBudget'],
            key="launch_budget_input"
        )
        st.session_state.form_data['launchBudget'] = launch_budget
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous Step", key="prev_step_2"):
                go_to_previous_step()
                st.rerun()
        with col2:
            if st.button("Next Step →", key="next_step_2"):
                go_to_next_step()
                st.rerun()

    elif st.session_state.step == 3:
        st.markdown('<h2 class="step-header">🌍 Execution & Expansion Strategy</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            geographic_focus = st.selectbox(
                "🌐 Geographic Focus", 
                ["Local", "National", "North America", "Europe", "APAC", "Global"],
                index=["Local", "National", "North America", "Europe", "APAC", "Global"].index(
                    st.session_state.form_data['geographicFocus']
                ),
                key="geographic_focus_select"
            )
            st.session_state.form_data['geographicFocus'] = geographic_focus
            
            industry_focus = st.text_input(
                "🏢 Target Industries", 
                value=st.session_state.form_data['industryFocus'],
                key="industry_focus_input"
            )
            st.session_state.form_data['industryFocus'] = industry_focus
        
        with col2:
            team_size = st.selectbox(
                "👥 Team Size", 
                ["1-5", "6-10", "11-25", "26-50", "50+"],
                index=["1-5", "6-10", "11-25", "26-50", "50+"].index(
                    st.session_state.form_data['teamSize']
                ),
                key="team_size_select"
            )
            st.session_state.form_data['teamSize'] = team_size
            
            timeline_date = st.date_input(
                "🗓️ Preferred Launch Date", 
                value=st.session_state.form_data['timelineConstraints'] if st.session_state.form_data['timelineConstraints'] else None,
                key="timeline_date_input"
            )
            st.session_state.form_data['timelineConstraints'] = timeline_date
        
        technical_complexity = st.text_area(
            "🔬 Technical Complexity & Integration Requirements", 
            value=st.session_state.form_data['technicalComplexity'],
            key="technical_complexity_textarea"
        )
        st.session_state.form_data['technicalComplexity'] = technical_complexity
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous Step", key="prev_step_3"):
                go_to_previous_step()
                st.rerun()
        with col2:
            if st.button("Generate GTM Playbook 🚀", key="generate_playbook"):
                generate_playbook_flow()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main App
def main():
    st.title("🚀 GTM Launch Playbook Generator")
    st.write("Craft a data-driven Go-To-Market strategy in minutes")
    
    # Progress bar for the form steps
    progress_placeholder = st.empty()
    with progress_placeholder.container():
        progress = st.progress(st.session_state.step / 3)
        step_text = f"Step {st.session_state.step} of 3"
        st.caption(step_text)
    
    render_form()

    # Optional: Display generated playbook
    if st.session_state.playbook_generated and not st.session_state.playbook_generated.startswith("Error"):
        st.markdown('<div class="generated-playbook">', unsafe_allow_html=True)
        st.markdown("### 📄 Generated Playbook Preview")
        st.write(st.session_state.playbook_generated)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
