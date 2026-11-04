### 🔍 Fake Job Detector using Machine Learning

An AI-powered web application that analyzes job postings and predicts whether they are legitimate or potentially fraudulent. The application combines Machine Learning 

-**Streamlit**
- **Logistic Regression** 
- **TF-IDF**

with rule-based NLP techniques to identify suspicious job advertisements.


---
## Table of Contents

- <a href="#About the Project">About the Project</a>
- <a href="#Features">Features</a>
- <a href="#Technologies Used">Technologies Used</a>
- <a href="#Machine Learning Model">Machine Learning Model</a>
- <a href="#Project Structure">Project Structure</a>
- <a href="#WorkFlow">WorkFlow</a>
- <a href="#Installation">Installation</a>
- <a href="#Scam Indicators">Scam Indicators</a>
- <a href="#Future Improvements">Future Improvements</a>
- <a href="#Author">Author</a>

---
<h2><a class="anchor" id="About the Project"></a>About the Project</h2>

Fake job postings are becoming increasingly common on job portals, social media, and messaging platforms. These scams often use unrealistic salary promises, urgent hiring messages, and unofficial communication channels to attract job seekers.

The Fake Job Detector helps users analyze job descriptions and estimate whether a job post is Legitimate or Potentially Fraudulent. The application combines Machine Learning (TF-IDF + Logistic Regression) with rule-based detection techniques to identify common scam indicators and provide a detailed risk assessment.

---
<h2><a class="anchor" id="Features"></a>Features</h2>

- Machine Learning-based scam detection
- TF-IDF text vectorization
- Logistic Regression classifier
- Rule-based scam analysis
- Scam probability score
- Detailed explanation of detected issues
- Interactive Streamlit web interface
- Job Scam Awareness Guide
- Safety recommendations for job seekers

---
<h2><a class="anchor" id="Technologies Used"></a>Technologies Used</h2>

- Programming Language
  - Python
- Machine Learning
  - Scikit-learn
  - Logistic Regression
  - TF-IDF Vectorizer
- Libraries
  - Streamlit
  - Pandas
  - NumPy
  -  Joblib
  - Regular Expressions (Regex)

--- 
<h2><a class="anchor" id="Project Structure"></a>Project Structure</h2>

Fake-Job-Detector/ │ ├── app.py ├── requirements.txt ├── README.md ├── render.yaml ├── .gitignore ├── LICENSE │ ├── assets/ │ └── screenshots/ ├── home.png ├── result.png └── guide.png        

--- 
<h2><a class="anchor" id="Installation"></a>Installation</h2>\

The detector checks for:

- Urgent Hiring Language
- Unrealistic Salary Offers
- WhatsApp / Telegram Contact
- Poor Grammar
- Excessive Capital Letters
- "No Experience Required" Scams
- Missing Professional Information

--- 
<h2><a class="anchor" id="WorkFlow"></a>WorkFlow</h2>

- User pastes a job description.
- The text is converted into numerical features using TF-IDF Vectorization.
- A Logistic Regression model predicts the likelihood of the post being fraudulent.
- Rule-based algorithms analyze:
  - Urgency language
  - Salary claims
  - Contact methods
  - Grammar quality
  - Unrealistic promises
- All indicators are combined to calculate a Scam Probability Score.
- The application displays:
  - Risk Level
  - Detected Red Flags
  - Detailed Explanation
  - Safety Recommendations

---

--- 
<h2><a class="anchor" id="Installation"></a>Installation</h2>

- Clone the Repository
  git clone https://github.com/your-username/Fake-Job-Detector.git
- Navigate to the Project
  cd Fake-Job-Detector
- Install Dependencies
  pip install -r requirements.txt
- Run the Application
  streamlit run app.py


--- 
<h2><a class="anchor" id="Future Improvements"></a>Future Improvements</h2>

- Deep Learning using BERT
- Real-world training dataset
- Company verification API
- Resume Matching System
- OCR support for image-based job posts
- Fake company website detection
- Explainable AI (XAI)
- Multi-language support

----
## Author

Ram Krishna
- Email: ramkrishna000888@gmail.com
- Linkeddin: https://www.linkedin.com/in/ramkrishna000/

