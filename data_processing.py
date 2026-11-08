import pandas as pd


def validate_and_clean(df: pd.DataFrame):
    """Clean common data-quality issues and return (cleaned_df, report)."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("The uploaded CSV has no records.")

    cleaned = df.copy()
    cleaned.columns = [str(c).strip() for c in cleaned.columns]
    cleaned = cleaned.dropna(how="all").dropna(axis=1, how="all")

    for col in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[col] = cleaned[col].replace(r"^\s*$", pd.NA, regex=True)

    id_candidates = ["Request_ID", "Request ID", "request_id", "RequestID", "Ticket_ID", "Ticket ID"]
    id_col = next((c for c in id_candidates if c in cleaned.columns), None)
    duplicate_ids = 0
    if id_col:
        duplicate_mask = cleaned[id_col].notna() & cleaned[id_col].duplicated(keep="first")
        duplicate_ids = int(duplicate_mask.sum())
        cleaned = cleaned.loc[~duplicate_mask].copy()

    invalid_dates = 0
    for col in cleaned.columns:
        if any(k in col.lower() for k in ("date", "time", "timestamp")):
            original = cleaned[col]
            parsed = pd.to_datetime(original, errors="coerce")
            invalid_dates += int((original.notna() & parsed.isna()).sum())
            cleaned[col] = parsed

    negative_values = 0
    for col in cleaned.columns:
        if pd.api.types.is_datetime64_any_dtype(cleaned[col]):
            continue
        if any(k in col.lower() for k in ("id", "phone", "contact")):
            continue
        if pd.api.types.is_numeric_dtype(cleaned[col]):
            numeric = pd.to_numeric(cleaned[col], errors="coerce")
            mask = numeric < 0
            negative_values += int(mask.sum())
            cleaned[col] = numeric.mask(mask)

    invalid_satisfaction = 0
    sat_col = next((c for c in cleaned.columns if c.lower().replace(" ", "_")
                    in {"satisfaction_score", "satisfaction", "satisfaction_rating"}), None)
    if sat_col:
        scores = pd.to_numeric(cleaned[sat_col], errors="coerce")
        mask = scores.notna() & ~scores.between(1, 5)
        invalid_satisfaction = int(mask.sum())
        cleaned[sat_col] = scores.mask(mask)

    report = {
        "duplicate_ids": duplicate_ids,
        "invalid_dates": invalid_dates,
        "negative_values": negative_values,
        "invalid_satisfaction": invalid_satisfaction,
    }
    return cleaned.reset_index(drop=True), report
