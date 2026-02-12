# 📡 BLE‑ML Windowing & TinyML Classifier

A high‑resolution BLE behavioral analysis and TinyML classification pipeline for ESP32‑based RF intelligence nodes.  
This system captures BLE advertisement patterns, aggregates them into fixed‑duration feature windows, and classifies each window as:

- `0` — NORMAL  
- `1` — SPAM  
- `2` — ROTATION_ABUSE  
- `3` — IMPERSONATION

The output is TinyML‑ready CSV suitable for training decision trees, random forests, or TFLite Micro models.

---

## ✨ Features

- High‑speed BLE advertisement capture (NimBLE‑Arduino)
- 1‑second ML feature windows
- 38 engineered BLE anomaly features
- Real‑time classification
- CSV logging for TinyML training
- Attack‑scenario dataset generation
- Python training pipeline included

---

## 📁 CSV Schema

Each row represents one BLE ML window.

### Label meanings

| Label | Meaning        |
|-------|----------------|
| 0     | NORMAL         |
| 1     | SPAM           |
| 2     | ROTATION_ABUSE |
| 3     | IMPERSONATION  |

---

## 📦 Data Collection

Collect separate CSV files for each scenario:


Recommended:

- 2–10 minutes per scenario  
- 1 row per second  
- Repeat each attack 3× at different distances  

---

## 🧪 BLE Attack Scenarios

### 1. BLE Spam Flood (label = 1)

- 50–200 advertisements/sec  
- Random MACs  
- Random manufacturer data  
- Random service UUIDs  

### 2. MAC Rotation Abuse (label = 2)

- iPhone/Android with privacy mode  
- ESP32 rotating MAC every 1–3 seconds  

### 3. Impersonation / Spoofing (label = 3)

- Fake Apple/Samsung/Tile/AirTag  
- Matching manufacturer IDs  
- Matching UUIDs  
- Matching names  

### 4. Beacon Storm (label = 1)

- Multiple ESP32 iBeacon/Eddystone beacons  

### 5. Connectable Abuse (label = 1)

- Rapid connectable toggling  
- Malformed GATT  
- Empty service tables  

---

## 🧰 BLE Attack Generator (ESP32, NimBLE‑Arduino)

```cpp
#include <NimBLEDevice.h>

NimBLEAdvertising *pAdv;

void setup() {
    Serial.begin(115200);
    NimBLEDevice::init("BLE_ATTACK_GEN");

    pAdv = NimBLEDevice::getAdvertising();

    NimBLEAdvertisementData adv;
    adv.setName("SPAM_DEV");
    adv.setManufacturerData(std::string("\x4C\x00\x01\x02\x03\x04", 6)); // fake Apple-ish
    pAdv->setAdvertisementData(adv);

    pAdv->setMinInterval(0x0020);
    pAdv->setMaxInterval(0x0020);
    pAdv->start();
}

void loop() {
    static uint32_t last = 0;
    if (millis() - last > 1000) {
        last = millis();
        uint8_t mac[6];
        for (int i = 0; i < 6; i++) mac[i] = random(0, 256);
        esp_base_mac_addr_set(mac);
        Serial.println("Rotated MAC");
    }
}



import glob
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load all BLE CSVs
files = glob.glob("data/ble/*.csv")
dfs = [pd.read_csv(f) for f in files]
data = pd.concat(dfs, ignore_index=True)

# Features / labels
feature_cols = [c for c in data.columns if c != "label"]
X = data[feature_cols].values.astype(np.float32)
y = data["label"].values.astype(np.int32)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Small tree (TinyML‑friendly)
clf = DecisionTreeClassifier(max_depth=6, min_samples_leaf=10, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save artifacts
joblib.dump(clf, "artifacts/ble_tree.joblib")
with open("artifacts/ble_features.txt", "w") as f:
    f.write("\n".join(feature_cols))


import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import classification_report, confusion_matrix

LABELS = ["NORMAL", "SPAM", "ROTATION_ABUSE", "IMPERSONATION"]

clf = joblib.load("artifacts/ble_tree.joblib")
features = [l.strip() for l in open("artifacts/ble_features.txt")]

def evaluate(csv_path):
    df = pd.read_csv(csv_path)
    X = df[features].values.astype(np.float32)
    y = df["label"].values.astype(np.int32)
    y_pred = clf.predict(X)

    print(confusion_matrix(y, y_pred))
    print(classification_report(y, y_pred, target_names=LABELS))

if __name__ == "__main__":
    evaluate("data/ble/all_ble.csv")


