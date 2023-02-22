import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
import xgboost as xgb
from xgboost import plot_importance

st.set_page_config(
    page_title="Credit Sentry",
    page_icon="🧊",
    layout="wide"
)
class creditRisk:
    def __init__(self):
        st.title('Credit :red[Sentry]')
        st.caption("Assessing creditworthiness is like peering into a crystal ball - it takes a mix of financial savvy and intuition to predict a borrower's repayment behavior.")

    def get_data(self):

        self.age = st.slider(
            "**Age**",
            18, 90
        )

        st.write('\n')

        self.income = st.number_input(
            "**Annual(yearly) Income**"
        )

        st.write('\n')

        self.home_ownership = st.radio("**Home Ownership Status**",
        ('RENT', 'OWN', 'MORTGAGE', 'OTHER')
        )

        st.write('\n')

        self.employment_len = st.slider(
            "**Employment Length(in years)**",
            0, 50
        )

        st.write('\n')

        self.loan_intent = st.radio(
            "**Loan Purpose / Intent**",
            ('PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT',
            'DEBTCONSOLIDATION')
        )

        st.write('\n')

        self.loan_grade = st.radio(
            "**Loan Grade**",
            ('A', 'B', 'C', 'D', 'E', 'F', 'G')
        )

        st.write('\n')

        self.amount = st.number_input(
            "**Loan Amount**"
        )

        st.write('\n')

        self.interest_rate = st.slider(
            "**Rate of Interest**",
            0.00, 100.00
        )

        st.write('\n')

        self.percent_income = st.slider(
            "**Debt-to-Income Ratio**",
            0.00, 1.00
        )

        if st.button('More info'):

            st.write("Debt-to-Income Ratio: Percentage of a borrower's income that is used to pay for their monthly debts, including the loan they are applying for.") 

        st.write('\n')

        self.hist_default = st.radio(
            "**Any Historical Default?**",
            ('Yes', 'No')
        )

        st.write('\n')

        self.cred_hist_len = st.slider(
            "**Credit History Length**",
            0, 30
        )

    def pre_process(self):
        #Ordinal encoding
        ordinal_map1 = {'A':7, 'B':6, 'C':5, 'D':4, 'E':3, 'F':2, 'G':1}
        self.loan_grade_encoded = ordinal_map1[self.loan_grade]

        ordinal_map2 = {'Yes':1, 'No':0}
        self.hist_default_endcoded = ordinal_map2[self.hist_default]

        #One-hot encoding
        home_ownership_labels = np.array(['MORTGAGE', 'OTHER', 'OWN', 'RENT'])
        loan_intent_labels = np.array(['DEBTCONSOLIDATION', 'EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL',  'VENTURE', 
            ])

        home_ownership_index = np.where(home_ownership_labels == self.home_ownership)[0][0]
        loan_intent_index = np.where(loan_intent_labels == self.loan_intent)[0][0]

        self.home_ownership_encoded = np.zeros(len(home_ownership_labels))
        self.home_ownership_encoded[home_ownership_index] = 1

        self.loan_intent_encoded = np.zeros(len(loan_intent_labels))
        self.loan_intent_encoded[loan_intent_index] = 1
        
        self.one_hot_encoded = np.concatenate((self.home_ownership_encoded, self.loan_intent_encoded))

        self.processed_data = np.concatenate((
            (np.array([self.age, self.income, self.employment_len])),
            (np.array([self.loan_grade_encoded, self.amount, self.interest_rate, self.percent_income, self.hist_default_endcoded, self.cred_hist_len])),
            self.one_hot_encoded
        ))

        self.processed_data = self.processed_data.reshape(1,-1)

    def load_model(self):
        self.model = load('assets/model.pkl')
  
    def predict_CRA(self):
        self.y_hat = self.model.predict(self.processed_data)

        if self.y_hat[0] == 0:
            st.subheader(':green[Not Default] ✅')
        else:
            st.subheader(':red[Default] ❌')
        
        

def main():
    data = creditRisk()
    data.get_data()
    data.pre_process()
    data.load_model()

    if st.button('Submit'):
        data.predict_CRA()
    else:
        st.write('Enter the details and press submit!')

main()
