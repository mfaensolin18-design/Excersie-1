import pandas as pd
import streamlit as st
from modules.modeling import load_or_train_model


def load_model_bundle(path="models/trained_model.joblib"):
    return load_or_train_model(path)


def make_prediction_form(bundle, choices_df=None):
    st.write("Enter the request details to estimate the likelihood of an SLA breach.")
    model = bundle["model"]
    with st.form("sla_prediction_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            request_type = st.selectbox("Request Type", ["Enrollment", "Document Request", "Technical Support", "Scholarship", "Payment"])
            priority = st.selectbox("Priority", ["Low", "Normal", "High", "Urgent"])
        with c2:
            channel = st.selectbox("Submission Channel", ["Online Form", "Email", "Walk-in"])
            days_open = st.number_input("Days Open", min_value=0, max_value=365, value=3)
        with c3:
            workload = st.number_input("Staff Workload (active requests)", min_value=0, max_value=500, value=8)
            satisfaction = st.selectbox("Satisfaction Score", [1, 2, 3, 4, 5], index=3)
        submitted = st.form_submit_button("Predict SLA Breach Risk", type="primary")

    if submitted:
        sample = pd.DataFrame([{
            "Request_Type": request_type,
            "Priority": priority,
            "Submission_Channel": channel,
            "Days_Open": days_open,
            "Staff_Workload": workload,
            "Satisfaction_Score": satisfaction,
        }])
        probability = float(model.predict_proba(sample)[0][1])
        prediction = int(probability >= 0.5)
        st.markdown("### Prediction result")
        st.metric("Estimated SLA-breach probability", f"{probability:.1%}")
        if prediction:
            st.warning("Higher estimated risk: staff review is recommended.")
        else:
            st.success("Lower estimated risk based on the entered details.")
        st.caption("This is a decision-support estimate from a synthetic training dataset, not a guarantee or an automatic service decision.")
    if bundle.get("accuracy") is not None:
        st.caption(f"Model holdout accuracy on synthetic training data: {bundle['accuracy']:.1%}")
