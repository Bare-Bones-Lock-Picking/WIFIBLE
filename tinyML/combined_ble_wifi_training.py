import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

wifi_df = pd.read_csv("wifi_training_dataset.csv")
ble_df  = pd.read_csv("ble_training_dataset.csv")

print("Wi-Fi shape:", wifi_df.shape)
print("BLE shape:", ble_df.shape)

def train_and_analyze(df, name):
    X = df.drop(columns=["label"]).values
    y = df["label"].values
    feature_names = df.drop(columns=["label"]).columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print(f"\n=== {name} ===")
    print("Accuracy:", clf.score(X_test, y_test))
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"{name} Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.show()

    importances = clf.feature_importances_
    idx = np.argsort(importances)[::-1][:15]
    plt.figure(figsize=(8,5))
    plt.barh(np.array(feature_names)[idx][::-1], importances[idx][::-1])
    plt.title(f"{name} Top 15 Feature Importances")
    plt.tight_layout()
    plt.show()

    return clf, feature_names, importances

wifi_clf, wifi_features, wifi_importances = train_and_analyze(wifi_df, "Wi-Fi")
ble_clf,  ble_features,  ble_importances  = train_and_analyze(ble_df,  "BLE")