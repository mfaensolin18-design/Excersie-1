from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from modules.sample_data import create_sample_dataset

FEATURES = ["Request_Type", "Priority", "Submission_Channel", "Days_Open", "Staff_Workload", "Satisfaction_Score"]
CATEGORICAL = ["Request_Type", "Priority", "Submission_Channel"]
NUMERIC = ["Days_Open", "Staff_Workload", "Satisfaction_Score"]


def train_and_save_model(path="models/trained_model.joblib"):
    data = create_sample_dataset(1000, seed=42)
    X = data[FEATURES]
    y = data["SLA_Breached"].astype(int)

    preprocessor = ColumnTransformer([
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]), CATEGORICAL),
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
        ]), NUMERIC),
    ])
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", DecisionTreeClassifier(max_depth=5, min_samples_leaf=8, random_state=42)),
    ])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.2, random_state=42, stratify=y
    )
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES, "accuracy": accuracy}, path)
    return {"model": model, "features": FEATURES, "accuracy": accuracy}


def load_or_train_model(path="models/trained_model.joblib"):
    path_obj = Path(path)
    if path_obj.exists():
        try:
            bundle = joblib.load(path_obj)
            if isinstance(bundle, dict) and "model" in bundle:
                return bundle
        except Exception:
            # Rebuild the model if a saved artifact is incompatible with this environment.
            pass
    return train_and_save_model(path)
