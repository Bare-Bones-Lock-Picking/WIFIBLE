# TinyML System Overview

This document explains how the TinyML subsystem works inside the project, how it integrates with the existing ESP32 architecture, and how developers can retrain or extend the BLE/Wi‑Fi machine‑learning models.

The goal of the TinyML layer is simple:

> **Use lightweight ML models to detect RF patterns that are too complex, subtle, or multi‑feature for rule‑based logic alone.**

TinyML does *not* replace the existing rule engine — it sits **on top of it**, providing an additional signal that improves detection accuracy and reduces false positives.

---

# 1. Architecture Overview

## 1.1 High‑Level Flow

Packets │ --> │ Feature Gen  │ --> │ TinyML Model   │ --> │ Threat Engine │


### RF Packets
- BLE advertisements  
- Wi‑Fi probe requests / beacons  
- Metadata extracted from ESP32 sniffers  

### Feature Generator
Each packet window is converted into a fixed‑length feature vector.

Examples (BLE):
- RSSI mean & variance  
- Advertisement interval variance  
- MAC entropy  
- Manufacturer ID patterns  

Examples (Wi‑Fi):
- SSID length  
- Beacon interval  
- Supported rates entropy  
- Vendor OUI  
- RSSI distribution  

### TinyML Model
A small `.tflite` model (typically <20 KB) runs on the ESP32 using EloquentTinyML.

### Threat Engine
The model’s output is combined with:
- rule‑based heuristics  
- device attribution  
- scoring logic  
- per‑mode thresholds  

This hybrid approach gives you:
- deterministic behavior when needed  
- ML‑based nuance when patterns are subtle  

---

# 2. Why TinyML?

Rule‑based detection is fast and predictable, but limited.

| Challenge | Rule‑Based | TinyML |
|----------|------------|--------|
| Multi‑feature interactions | ❌ Hard | ✔ Natural |
| Noisy RF environments | ❌ Fragile | ✔ Robust |
| Evolving attack patterns | ❌ Manual updates | ✔ Retrain model |
| Subtle timing anomalies | ❌ Difficult | ✔ Easy |

TinyML gives the system a “sense” of RF behavior that rules alone cannot capture.

---

# 3. Model Inputs & Outputs

## 3.1 Input Vector

Each model receives a **fixed‑length float array** representing one window of RF activity.

Example (BLE):

