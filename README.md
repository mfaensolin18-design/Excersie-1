# Student Service Request Monitoring System

A Streamlit decision-support application for reviewing student service requests and estimating possible SLA breaches.

## Features
- CSV upload, validation, and cleaning
- Exploratory data analysis
- Decision Tree SLA-breach risk prediction
- Workload dashboard
- System design overview

## Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The Decision Tree model is trained automatically the first time the Prediction or Dashboard model is requested. It uses generated synthetic training data and saves the model under `models/trained_model.joblib`.

## Deploy to Streamlit Community Cloud
1. Extract this ZIP.
2. Upload the contents to the root of a GitHub repository.
3. In Streamlit Community Cloud, create an app and select `app.py` as the main file.
4. Deploy. Ensure `requirements.txt`, `app.py`, and the `modules/` folder are committed.

## Dataset
A 400-row synthetic sample dataset is included at `data/student_service_requests_synthetic.csv`.

Expected columns:
- `Request_ID`
- `Request_Date`
- `Request_Type`
- `Priority`
- `Submission_Channel`
- `Days_Open`
- `Staff_Workload`
- `Satisfaction_Score`
- `SLA_Breached`

## Important note
This project uses synthetic data for demonstration. Model predictions are estimates only and must not automatically approve, deny, or prioritize student services without staff review.
