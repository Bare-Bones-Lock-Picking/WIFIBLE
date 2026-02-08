# 🧠 TinyML Integration

This project includes a lightweight, embedded machine‑learning pipeline designed to classify Wi‑Fi behaviour in real time on the ESP32. The goal is not “AI magic,” but a practical, explainable model that helps identify abnormal RF activity such as deauthentication floods, probe storms, spoofing, or beacon anomalies.

The system uses existing packet‑processing logic to generate a compact set of per‑second features. These features are exported as CSV and can be used to train a tiny decision‑tree model that fits comfortably inside the ESP32’s memory.

---

## 📡 How It Works

The firmware already performs detailed Wi‑Fi analysis (beacon parsing, spoof detection, channel‑hop tracking, etc.). TinyML simply reuses this information.

### 1. Per‑packet Feature Extraction

Every captured packet updates a small rolling window:

- RSSI sum  
- Packet count  
- Beacon count  
- Probe count  
- Deauth count  

This happens inside the normal packet‑processing path, so there is **no extra overhead**.

### 2. Per‑device Anomaly Counters

The sniffer already tracks things like:

- MAC spoofing  
- Interval anomalies  
- Capability spoofing  
- Channel hopping  

These are mirrored into **per‑second “recent” counters** so the ML model sees only the last second of behaviour, not lifetime totals.

### 3. One‑second ML Window

Once per second, the firmware:

- Aggregates device‑level stats  
- Computes average RSSI  
- Generates a label (`NORMAL`, `SPOOFING`, `DEAUTH`, `PROBE_FLOOD`, etc.)  
- Prints a CSV row over serial  
- Resets the window  

This produces clean, time‑aligned training data.

---

## 📄 Example CSV Output

Each line represents one second of RF activity:

avgRSSI,pktCount,beaconCount,probeCount,deauthCount,uniqueDevices,spoofEvents,anomalyEvents,label -67.4,120,30,5,0,3,1,0,NORMAL -55.2,300,80,50,0,3,12,0,SPOOFING -70.1,140,40,10,0,3,1,0,NORMAL


This dataset can be fed directly into Python, Edge Impulse, TensorFlow Lite, or a simple decision‑tree generator.

---
## 🧪 How to Train Your TinyML Model

The sniffer can export a compact, per‑second feature vector over serial. Each row looks like:

```text
avgRSSI,pktCount,beaconCount,probeCount,deauthCount,uniqueDevices,spoofEvents,anomalyEvents,label
-67.4,120,30,5,0,3,1,0,NORMAL
-55.2,300,80,50,0,3,12,0,SPOOFING
-70.1,140,40,10,5,4,2,0,DEAUTH

### Why This Works

Decision trees love:

- clean boundaries  
- stable per‑second features  
- consistent labels  

The ESP32 can run a small tree (10–30 nodes) extremely fast with no heap allocation.

---

## ⚙️ Deploying the Model

Once trained, the model can be exported as:

- a series of `if/else` rules  
- a compact decision tree array  
- a threshold‑based classifier  

The firmware includes a simple inference hook where you can paste the generated model. The model runs once per second using the same ML window that produced the training data.

---

## 🎯 Why TinyML Helps

The sniffer already detects dozens of attack patterns using handcrafted logic. TinyML adds:

- **adaptive behaviour detection**  
- **cross‑feature correlations**  
- **environment‑specific tuning**  
- **reduced false positives**  

It doesn’t replace the rule‑based engine — it complements it.

---


