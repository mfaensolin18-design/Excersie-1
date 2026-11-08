import pandas as pd
import streamlit as st


def show_eda(df: pd.DataFrame):
    if df.empty:
        st.warning("The dataset is empty.")
        return
    st.subheader("Dataset overview")
    a, b, c = st.columns(3)
    a.metric("Total records", f"{len(df):,}")
    b.metric("Total columns", len(df.columns))
    c.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

    st.markdown("### Descriptive statistics")
    st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

    if "SLA_Breached" in df.columns:
        st.markdown("### SLA breach distribution")
        counts = df["SLA_Breached"].astype(str).value_counts().rename_axis("SLA_Breached").reset_index(name="Records")
        st.bar_chart(counts.set_index("SLA_Breached"))

    for col in ["Request_Type", "Priority", "Submission_Channel"]:
        if col in df.columns:
            st.markdown(f"### Requests by {col.replace('_', ' ')}")
            st.bar_chart(df[col].astype(str).value_counts())
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        st.markdown("### Numeric feature relationships")
        st.dataframe(numeric.corr(numeric_only=True), use_container_width=True)
