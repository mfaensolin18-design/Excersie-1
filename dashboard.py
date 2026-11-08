import pandas as pd
import streamlit as st


def show_dashboard(df: pd.DataFrame):
    if df.empty:
        st.warning("No records available.")
        return
    total = len(df)
    if "SLA_Breached" in df.columns:
        breached = pd.to_numeric(df["SLA_Breached"], errors="coerce").fillna(0).astype(int)
        breach_count = int((breached == 1).sum())
        rate = breach_count / total if total else 0
    else:
        breached = None
        breach_count = 0
        rate = 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Requests", f"{total:,}")
    c2.metric("SLA Breaches", f"{breach_count:,}")
    c3.metric("Breach Rate", f"{rate:.1%}")

    if "Request_Type" in df.columns:
        st.markdown("### Workload by request type")
        st.bar_chart(df["Request_Type"].astype(str).value_counts())
    if "Priority" in df.columns:
        st.markdown("### Requests by priority")
        st.bar_chart(df["Priority"].astype(str).value_counts())

    st.markdown("### Requests for staff review")
    if breached is not None:
        flagged = df.loc[breached == 1]
        st.dataframe(flagged.head(100), use_container_width=True)
        st.caption(f"Showing up to 100 of {len(flagged)} records labeled as SLA-breached in the uploaded dataset.")
    else:
        st.info("The uploaded dataset has no SLA_Breached column, so flagged requests cannot be displayed.")
