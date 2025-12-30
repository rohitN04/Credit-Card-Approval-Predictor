# 🏦 Credit Card Approval Risk Evaluator

A Machine Learning-powered web application that predicts the probability of how good/bad their chances are if they applies for a credit card using our dataset. This tool allows loan officers and customers to input applicant details (income, family status, occupation) and receive an instant predicted credit score estimate and probability for chances of approval.

## 🚀 Live Demo
[Link to your Streamlit App will go here]

## 🛠️ Features
- **Real-time Scoring:** Instant calculation of credit scores (300-850 range).
- **Risk Assessment:** Categorizes applicants as High, Medium, or Low risk.
- **Visual Feedback:** Interactive progress bars and color-coded results.
- **Factor Analysis:** Weighs multiple variables including Income Type, Family Size, and Housing situation.

## 💻 Tech Stack
- **Python** (Logic & Calculation)
- **Streamlit** (Frontend UI)
- **NumPy** (Mathematical operations)

## ⚙️ How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/rohitN04/Credit-Card-Approval-Predictor.git
   cd Credit-Card-Approval-Predictor

2. Install dependencies
   pip install -r requirements.txt

3. Run the app
   python -m streamlit run app.py

## 📊 Logic Overview
The model uses a Logistic Regression-based scorecard approach. Key risk drivers include:
Income Type: Pensioners carry higher risk weight; State servants carry lower risk.
Family Status: Single applicants typically see a slight score reduction compared to married applicants.
Family Size: Large families (5+ members) trigger higher risk adjustments due to increased financial burden.

## 📝 License
This project is open source and available under the MIT License.
