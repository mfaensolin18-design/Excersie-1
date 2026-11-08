import streamlit as st


def show_system_design():
    st.subheader("System purpose")
    st.write(
        "The Student Service Request Monitoring System organizes request records, "
        "summarizes service workload, and estimates possible SLA-breach risk to "
        "support staff review."
    )
    st.subheader("Actors")
    st.markdown("- **Student:** submits a service request and may provide satisfaction feedback.\n"
                "- **Student-services staff:** reviews requests and follows up on delayed cases.\n"
                "- **System administrator:** maintains data, model files, and application settings.")
    st.subheader("Functional requirements")
    st.markdown("1. Upload a CSV dataset.\n"
                "2. Validate and clean common data-quality issues.\n"
                "3. Display descriptive statistics and charts.\n"
                "4. Estimate SLA-breach probability using a Decision Tree model.\n"
                "5. Display workload summaries and records marked for follow-up.")
    st.subheader("Basic workflow")
    st.code("Upload CSV → Validate/Clean → Analyze Data → Predict Risk → Staff Review → Follow-up")
    st.warning("Predictions are advisory only. Authorized staff must review the request and make service decisions.")
