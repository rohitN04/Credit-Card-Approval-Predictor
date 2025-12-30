import streamlit as st
import numpy as np

class CC_approval_pred():
    def __init__(self):
        self.user_data = None
        self.credit_score = None
        self.prob_good = None

    def calculate_score(self):
        
        log_odds = 0.2983

        log_odds += self.user_data.get('AMT_INCOME_TOTAL', 0) * -0.00000035
        log_odds += self.user_data.get('YEARS_EMPLOYED', 0) * 0.001810

        adults = 1 # The applicant
        if self.user_data.get('FAMILY_STATUS') in ['Married', 'Civil marriage']:
            adults += 1
            
        total_size = adults + self.user_data.get('CNT_CHILDREN', 0)
        
        # Determine the Bin
        if total_size <= 1:
            fam_bin = 'Singleton'
        elif total_size <= 4:
            fam_bin = 'Small'
        else:
            fam_bin = 'Large'
            
        # Apply Weight for the Bin
        family_size_weights = {
            'Large': 0.6830,      # High Risk
            'Singleton': -0.4090, # Low Risk (Safety factor)
            'Small': 0.0228       # Neutral
        }
        log_odds += family_size_weights.get(fam_bin, 0)

        income_weights = {
            'Pensioner': 1.685,          # Very High Risk
            'State servant': -0.721,     # Very Safe
            'Working': -0.342,
            'Commercial associate': -0.300,
            'Student': -0.023
        }
        log_odds += income_weights.get(self.user_data.get('INCOME_TYPE'), 0)
        
        # Education
        edu_weights = {
            'Lower secondary': 0.441,    # Risky
            'Incomplete higher': 0.142,
            'Secondary / secondary special': -0.134,
            'Higher education': -0.069,
            'Academic degree': -0.083
        }
        log_odds += edu_weights.get(self.user_data.get('EDUCATION_TYPE'), 0)
        
        # Family Status
        family_status_weights = {
            'Widow': 0.827,              # High Risk
            'Single': 0.252,
            'Separated': -0.208,
            'Married': -0.273,           # Safe
            'Civil marriage': -0.300
        }
        log_odds += family_status_weights.get(self.user_data.get('FAMILY_STATUS'), 0)
        
        # Housing
        housing_weights = {
            'Municipal apartment': 0.517, # Risky
            'Office apartment': 0.384,
            'House / apartment': -0.101,  # Safe
            'Co-op apartment': -0.075,
            'Rented apartment': -0.055,
            'With parents': -0.372        # Very Safe
        }
        log_odds += housing_weights.get(self.user_data.get('HOUSING_TYPE'), 0)
        
        # Occupation (Selected)
        job_weights = {
            'Low-skill Laborers': 0.606,  # High Risk
            'High skill tech staff': 0.554,
            'Drivers': 0.460,
            'IT staff': 0.462,            # Surprisingly Risky in this model
            'Security staff': 0.394,
            'Core staff': 0.240,
            'Laborers': 0.061,
            'Accountants': 0.056,
            'Managers': 0.051,
            'Sales staff': -0.131,
            'Realty agents': -0.189,
            'Cooking staff': -0.387,
            'Cleaning staff': -0.465,
            'Medicine staff': -0.548,
            'Private service staff': -0.663
        }
        log_odds += job_weights.get(self.user_data.get('OCCUPATION_TYPE'), 0)
        
        # Age Group
        age_weights = {
            'young_adults': 0.224, # Riskiest
            'adult': 0.051,
            'mid_age': 0.010,
            'senior': 0.010        # Neutral
        }
        log_odds += age_weights.get(self.user_data.get('AGE_GROUP'), 0)

        prob_bad = 1 / (1 + np.exp(-log_odds))

        prob_good = 1 - prob_bad

        credit_score = 300 + (prob_good*550)
        if credit_score > 850:
            credit_score = 850
        self.credit_score = int(credit_score)
        self.prob_good = prob_good
        return self.credit_score, self.prob_good

    def app_setup(self):
        # page setup
        st.set_page_config(page_title = "Credit Card Application Predictor", page_icon="🏦")
        st.title("🏦 Credit Card Application Predictor")
        st.write("Enter applicant details below to calculate their creditworthiness.")

        # input form
        with st.form("Score Form"):
            st.subheader("Applicant Details")
            col1, col2 = st.columns(2)

            with col1:
                income = st.number_input("Total Annual Income", value=100000, step=5000)
                years_emp = st.number_input("Years Employed", value=5.0, step=0.5)
                occupation = st.selectbox("Occupation", [
                    'Laborers', 'Core staff', 'Sales staff', 'Managers', 'Drivers', 
                    'High skill tech staff', 'Medicine staff', 'Accountants'
                ])
                education = st.selectbox("Education", [
                    'Secondary / secondary special', 'Higher education', 
                    'Incomplete higher', 'Lower secondary'
                ])
            with col2:
                children = st.number_input("Children Count", min_value=0, value=0)
                family_status = st.selectbox("Family Status", [
                    'Married', 'Single / not married', 'Civil marriage', 'Widow', 'Separated'
                ])
                housing = st.selectbox("Housing Type", [
                    'House / apartment', 'With parents', 'Municipal apartment', 
                    'Rented apartment', 'Office apartment'
                ])
                income_type = st.selectbox("Income Type", [
                    'Working', 'Commercial associate', 'Pensioner', 'State servant'
                ])
            age_group = st.radio("Age Group", ["young_adults", "adult", "mid_age", "senior"], horizontal=True)

            submitted = st.form_submit_button("Calculate Probs", type="primary")

        if submitted:
            self.user_data = {
                'AMT_INCOME_TOTAL': income,
                'YEARS_EMPLOYED': years_emp,
                'CNT_CHILDREN': children,
                'FAMILY_STATUS': family_status,
                'INCOME_TYPE': income_type,
                'HOUSING_TYPE': housing,
                'EDUCATION_TYPE': education,
                'OCCUPATION_TYPE': occupation,
                'AGE_GROUP': age_group
            }

            score, prob = self.calculate_score()

            st.divider()

            res_col1, res_col2, res_col3 = st.columns([1, 2, 1])

            if score > 720:
                st.success(f"✅ Low Risk ({prob:.1%} Approval Chance)")
            elif score >= 600:
                st.warning(f"⚠️ Medium Risk ({prob:.1%} Approval Chance)")
            else:
                st.error(f"🛑 High Risk ({prob:.1%} Approval Chance)")
                
            st.progress(prob)

if __name__ == "__main__":
    app = CC_approval_pred()
    app.app_setup()
