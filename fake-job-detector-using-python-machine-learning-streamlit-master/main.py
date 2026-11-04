import streamlit as st
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Fake Job Detector",
    page_icon="🔍",
    layout="wide"
)

# Title of Description
st.title("Fake Job Detector for Call Center/Scam Jobs")
st.markdown("Paste a job post below to analyze whether it is a fake job or not")

# Initialize session state for model and vectorizer
if 'model' not in st.session_state:
    st.session_state.model = None
if 'vectorizer' not in st.session_state:
    st.session_state.vectorizer = None

# Load or create a simple model
def load_model():
    """ Create or load a simple ML model for demonstration purpose"""
    sample_scam_texts = [
        "We are looking for a call center agent to work from home. No experience required. Apply now!",
        "Earn $5000 per week by working from home. Limited spots available. Sign up today!",
        "Congratulations! You've been selected for a high-paying job. Click here to claim your offer.",
        "Work from home and make money fast! No skills needed. Join our team now.",
        "Get rich quick! Work from home and earn thousands of dollars. Apply immediately." 
    ]

    sample_legit_texts = [
        "We are hiring a Customer Support Representative to manage incoming calls and emails.",
        "Full-time Software Engineer position required 3 years experience with Python and SQL.",
        "Seeking an experienced HR Manager to oversee talent acquisition and employee relations.",
        "Join our team as an Accountant. Bachelor degree in Finance required.",
        "Marketing Specialist needed for lead generation campaign. Flexible hybrid schedule."
    ]
    
    # Combine and label
    texts = sample_scam_texts + sample_legit_texts
    labels = [1] * len(sample_scam_texts) + [0] * len(sample_legit_texts)
    vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
    x = vectorizer.fit_transform(texts)
    model = LogisticRegression()
    model.fit(x, labels)
    return model, vectorizer     

# Rule-based detection function
def detect_urgency(text):
    '''Detects urgency in the job post text based on certain keywords and phrases.'''
    urgency_keywords = ['urgent', 'immediate', 'act now', 'limited time', 'do not miss out']
    matches = []
    for keywords in urgency_keywords:
        if re.search(rf'\b{keywords}\b', text, re.IGNORECASE):
            matches.append(keywords)
    return matches

def detect_salary_language(text):
    '''Detects salary-related language in the job post text based on certain keywords and phrases.'''
    salary_patterns = [
        r'\$\d{3,5}\s*(weekly|daily|hourly)', 
        r'earn\s+\$\d{3,}\s*(easily|quickly|fast)', 
        r'high\s+salary\s*(income|salary|payment)', 
        r'make\s+money\s+fast', 
        r'get\s+rich\s+quick', 
        r'guaranteed\s+(income|salary)', 
    ]

    matches = []
    for pattern in salary_patterns:
        found = re.findall(pattern, text, re.IGNORECASE)
        if found:
            matches.extend(found)
    return matches

def detect_contact_methods(text):
    '''Detects contact methods in the job post text based on certain keywords and phrases.'''
    contact_patterns = [
        r'WhatsApp', 
        r'Telegram', 
        r'@[\w]+', 
        r'\+\d{10,}', 
        r'cash\s*app',
        r'PayPal\s*me', 
        r'direct\s*message', 
        r'DM\s*us', 
        r'message\s*us\s*on', 
    ]
    matches = []
    for pattern in contact_patterns:
        found = re.findall(pattern, text, re.IGNORECASE)
        if found:
            matches.extend(found)
    return matches

def detect_grammar_issuess(text):
    """Detect poor grammar and excessive punctuation."""
    issues = []

    # Excessive capitalization
    if re.search(r'[A-Z]{4,}', text):
        issues.append("Excessive capitalization")

    # Multiple exclamation marks
    if re.search(r'!{2,}', text):
        issues.append("Multiple exclamation marks")
    
    # Poor sentence structure
    lines = text.split('\n')
    short_line = [l for l in lines if len(l.split()) < 3 and len(l) > 10]
    if len(short_line) > 3:
        issues.append("Poor sentence structure")
    
    # Missing professional language
    professional_terms = ['professional', 'experience', 'qualifications', 'skills', 'responsibilities']
    if not any(term in text.lower() for term in professional_terms):
        issues.append("Missing professional language")
    return issues

def detect_too_good_to_be_true(text):
    """Detects offers that seem too good to be true."""
    patterns = [
        r'no\s+resume',
        r'no\s+experience', 
        r'work\s+from\s+home', 
        r'instant\s+hiring', 
        r'guaranteed\s+job', 
    ]
    matches = []
    for pattern in patterns:
        found = re.findall(pattern, text, re.IGNORECASE)
        if found:
            matches.extend(found)
    return matches

def calculate_scam_score(red_flags):
    """Calculate scam probability based on red flags."""
    base_score = 0
    weights = {
        'urgency': 15,
        'salary': 20,
        'contact': 25,
        'grammer': 10,
        'too_good': 20,
        'ml_prediction': 10   
    }

    for flag_type, flag_list in red_flags.items():
        if flag_type != 'score' and flag_list:
            if flag_type == 'ml_prediction':
                base_score += flag_list[0] * weights[flag_type]
            else:
                base_score += min(len(flag_list) * 5, weights[flag_type])
    return min(100, int(base_score))

def analyze_job_post(text):
    """ Analyze job post and return red flags"""
    if not text or len(text.strip()) < 20:
        return None
    red_flags = {
        'urgency': detect_urgency(text),
        'salary': detect_salary_language(text),
        'contact': detect_contact_methods(text),
        'grammer': detect_grammar_issuess(text),
        'too_good': detect_too_good_to_be_true(text),
        'ml_prediction': []
    }

    if st.session_state.model and st.session_state.vectorizer:
        try:
            transformed = st.session_state.vectorizer.transform([text])
            prediction = st.session_state.model.predict_proba(transformed)[0][1]
            red_flags['ml_prediction'] = [prediction]
        except Exception:
            red_flags['ml_prediction'] = [0.5]

    red_flags['score'] = calculate_scam_score(red_flags)
    return red_flags

def generate_explanation(red_flags):
    """Generate explanation based on red flags"""
    explanations = []
    if red_flags['urgency']:
        explanations.append(f"❌ **Urgency detected**: The post uses urgent language ({', '.join(red_flags['urgency'][:3])}). Legitimate jobs rarely pressure applicants.")
    if red_flags['salary']:
        explanations.append(f"❌ **Unrealistic salary**: Mentions unrealistic earnings ({', '.join(map(str, red_flags['salary'][:3]))}). Scams often promise high pay for little work.")
    if red_flags['contact']:
        explanations.append(f"❌ **Suspicious contact method**: Uses informal channels ({', '.join(red_flags['contact'][:3])}). Legitimate companies use professional communication.")
    if red_flags['grammer']:
        explanations.append(f"❌ **Language issues**: Shows signs of poor professionalism ({', '.join(red_flags['grammer'])}). Professional job posts are well-written.")
    if red_flags['too_good']:
        explanations.append(f"❌ **Too good to be true**: Promises unrealistic benefits ({', '.join(red_flags['too_good'][:3])}). Be wary of offers requiring no experience for high pay.")
    if red_flags.get('ml_prediction', [0])[0] > 0.7:
        explanations.append(f"❌ **AI detection**: Our machine learning model identified patterns consistent with scam job posts.")
    if not explanations:
        explanations.append("✅ No major red flags detected.")
    return explanations

# Load this model 
if st.session_state.model is None:
    with st.spinner("Loading detection model..."):
        st.session_state.model, st.session_state.vectorizer = load_model()

# Create tabs
tab1, tab2, tab3 = st.tabs(["Analyze Job Post", "Red Flag Guide", "About"])

with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        job_text = st.text_area(
            "Paste the job post here :",
            height=300,
            placeholder="Example : Urgent Hiring!!! Work from home and earn $5000 weekly. No experience needed. WhatsApp us at +1234567890 for immediate start..."
        )

    with col2:
        st.markdown("### What to look for:")
        st.markdown("""
        - Urgent hiring language
        - Unrealistic salary promises
        - Contact via WhatsApp/Telegram
        - Poor grammar & excessive punctuation
        - 'Too good to be true' offers
        - Lack of company details
        """)

    # Analyse button 
    if st.button("Analyze job post..."):
        if job_text:
            red_flags = analyze_job_post(job_text)
            if red_flags:
                st.subheader("Analysis Results")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    score = red_flags['score']
                    if score < 30:
                        st.metric("Scam Probability", f"{score}%", delta="Low Risk", delta_color="normal")
                    elif score < 70:
                        st.metric("Scam Probability", f"{score}%", delta="Medium Risk", delta_color="off")
                    else:
                        st.metric("Scam Probability", f"{score}%", delta="High Risk", delta_color="inverse")

                with col2:
                    st.metric("Red Flags Found", len([v for k, v in red_flags.items() if k != 'score' and v]))
                with col3:
                    urgency_count = len(red_flags['urgency'])
                    st.metric("Urgency Indicators", urgency_count)
                with col4:
                    contact_count = len(red_flags['contact'])
                    st.metric("Suspicious Contact", contact_count)
                
                st.progress(red_flags['score'] / 100)
                st.subheader("Detailed Breakdown")

                explanations = generate_explanation(red_flags)
                for explanation in explanations:
                    st.info(explanation)

                with st.expander("View specific detected issues"):
                    for flag_type, flag_list in red_flags.items():
                        if flag_type != 'score' and flag_list and flag_type != 'ml_prediction':
                            st.write(f"**{flag_type.title()}**:")
                            for item in flag_list[:5]:
                                st.write(f"- {item}")

                st.subheader("Recommendations")

                if red_flags['score'] > 70:
                    st.error("**High Risk Detection** - This job post shows multiple scam indicators:")
                    st.markdown("""
                    1. **DO NOT** share personal information
                    2. **DO NOT** pay any "registration" or "training" fees
                    3. **DO NOT** contact through suspicious channels
                    4. Research the company on official platforms
                    5. Report suspicious posts to authorities
                    """)
                elif red_flags['score'] > 30:
                    st.warning("**CAUTION ADVISED** - Verify this opportunity carefully:")
                    st.markdown("""
                    1. Research the company's official website
                    2. Check employee reviews on LinkedIn
                    3. Ensure communication is through professional channels
                    4. Never pay money to get a job
                    5. Trust your instincts
                    """)
                else:
                    st.success("**LOW RISK** - This appears legitimate, but always verify:")
                    st.markdown("""
                    1. Still research the company
                    2. Ensure a proper interview process
                    3. Verify job offer through official channels
                    4. Read the contract carefully
                    """)
            else:
                st.error("Please enter a longer job post for analysis.")
        else:
            st.warning("Please paste a job post to analyze.")

with tab2:
    st.header("Red Flag Guide for Job Seekers")
    st.subheader("Common Scam Tactics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚨 Urgency & Pressure
        - "Hiring immediately"
        - "Limited time offer"
        - "Must start today"
        - "Quick hiring process"

        ### 📞 Unprofessional Contact
        - WhatsApp/Telegram interviews
        - Generic email addresses
        - No company phone number
        - Direct message only
        """)
    with col2:
        st.markdown("""
        ### ❗ Poor Presentation
        - Bad grammar/spelling
        - Excessive punctuation!!!
        - ALL CAPS TEXT
        - Lack of company details

        ### ❓ Vague Requirements
        - No specific skills needed
        - "Anyone can do it"
        - No interview process
        - No background check

        ### 💳 Requests for Money
        - "Training Fee"
        - "Registration cost"
        - "Equipment cost"
        - "Background check fee"
        """)
        
    st.subheader("Legitimate Job Indicators")
    st.markdown("""
    - ✅ Clear company information and website
    - ✅ Professional email address
    - ✅ Structured interview process
    - ✅ Realistic salary range
    - ✅ Specific job requirements
    - ✅ Professional communication
    - ✅ No requests for money
    """)

    st.subheader("Safety Checklist")
    checklist = st.columns(2)

    with checklist[0]:
        st.checkbox("Company has official website")
        st.checkbox("Job posted on reputable platform")
        st.checkbox("Professional email/contact provided")
        st.checkbox("Realistic job requirements")

    with checklist[1]:
        st.checkbox("No money requested upfront")
        st.checkbox("Clear interview Process")
        st.checkbox("Physical address verifiable")
        st.checkbox("Employee reviews available")

with tab3:
    st.header("About Fake Job Detector")
    st.markdown("""
    ### How It Works
    This tool uses a combination of techniques to identify potential scam posts:

    1. **Rule-based Detection**: Identifies specific patterns and keywords commonly used in scams.
    2. **Machine Learning**: Analyzes text patterns using a trained classifier.
    3. **Heuristic Analysis**: Checks for multiple scam indicators.

    ### Detection Methods

    - **Salary-Language Tricks**: Identifies unrealistic earnings promises
    - **Grammar & Urgency Analysis**: Detects poor writing and pressure tactics
    - **Contact Method Verification**: Flags suspicious communication channels
    - **Too-Good-To-Be-True Detection**: Identifies unrealistic offers

    ### Technology Stack

    - **Python** with Natural Language Processing (NLP)
    - **Regex Patterns** for rule-based detection
    - **Machine Learning Classifier** (Logistic Regression)
    - **Streamlit** for web interface

    ### Important Disclaimer

    This tool provides **risk assessment only** and is not 100% accurate. Always:

    - Conduct your own research
    - Verify through official channels
    - Never share sensitive information
    - Report suspicious posts to authorities

    ### For Employers

    If you're a legitimate employer and your posts are flagged:

    1. Use professional language in job descriptions
    2. Provide clear company information
    3. Use official communication channels
    4. Avoid excessive urgency language
    """)

    st.info(" **Note**: This is a demonstration tool. For production use, the model should be trained on a large, real-world dataset of scam and legitimate job posts.")

    # Footer
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🔍 Use this tool as a first line of defense against job scams. Always verify opportunities through official sources.</p>
            <p><small>Note: This tool is for educational purposes. Accuracy may vary.</small></p>
        </div>
        """,
        unsafe_allow_html=True
    )