import pandas as pd
import numpy as np
import joblib
import os
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.preprocessing import LabelEncoder

def parse_situation(code: str) -> dict:
    """
    Situation code is a 4-digit string: XYZW
    X = away goalie (1=in net), Y = away skaters, Z = home skaters, W = home goalie
    e.g. 1551 = 5v5, 1451 = home power play, 1541 = away power play
    """
    code = str(code)
    if len(code) != 4:
        return {"away_skaters": 5, "home_skaters": 5, "is_power_play": 0, "is_shorthanded": 0}
    away = int(code[1])
    home = int(code[2])
    return {
        "away_skaters": away,
        "home_skaters": home,
        "is_power_play": int(away != home),
        "is_shorthanded": int(away < home),
    }

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    # Parse situation codes
    situation = df["situation_code"].apply(parse_situation).apply(pd.Series)
    df = pd.concat([df, situation], axis=1)

    # Encode shot type
    le = LabelEncoder()
    df["shot_type_enc"] = le.fit_transform(df["shot_type"].fillna("unknown"))

    # Is shot from high-danger area (slot): close + low angle
    df["is_slot"] = ((df["distance"] < 20) & (df["angle"] < 45)).astype(int)

    # Period bucket: regulation vs overtime
    df["is_overtime"] = (df["period"] > 3).astype(int)

    return df, le

def train():
    print("Loading data...")
    df = pd.read_csv("data/shots_combined.csv")
    print(f"  {len(df):,} shots, {df['is_goal'].mean():.1%} goal rate")

    df, le = build_features(df)

    features = [
        "distance",
        "angle",
        "shot_type_enc",
        "is_power_play",
        "is_shorthanded",
        "away_skaters",
        "home_skaters",
        "is_slot",
        "is_overtime",
        "period",
    ]

    X = df[features]
    y = df["is_goal"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\nTraining on {len(X_train):,} shots, testing on {len(X_test):,}...")

    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=(y == 0).sum() / (y == 1).sum(),  # handle class imbalance
        random_state=42,
        eval_metric="logloss",
    )

    model.fit(X_train, y_train)

    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"\nROC-AUC: {auc:.4f}  (NHL team models are typically 0.76–0.80)")

    print("\nFeature importances:")
    for feat, imp in sorted(zip(features, model.feature_importances_), key=lambda x: -x[1]):
        print(f"  {feat:<20} {imp:.4f}")

    # Save model + encoder
    os.makedirs("model", exist_ok=True)
    joblib.dump(model, "model/xg_model.joblib")
    joblib.dump(le, "model/shot_type_encoder.joblib")
    joblib.dump(features, "model/feature_names.joblib")
    print("\nModel saved to model/")

if __name__ == "__main__":
    train()