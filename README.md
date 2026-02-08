![Alt text for the image](https://github.com/Bare-Bones-Lock-Picking/WIFIBLE/blob/main/logo/Logo-320_240.png)


# WIFIBLE (pronounce - 'WHY-fih-bull')
WIFIBLE is a real‑time RF intelligence system built on the CYD ESP32‑2432S028 touchscreen board.
It passively monitors Wi‑Fi and BLE activity, identifies devices, scores suspicious behavior, and presents results on a responsive UI. Its also aimed to be ported as a 'headless' (i.e no TFT screen) ESP32-C3 mini board.

WIFIBLE — ESP32 Wi‑Fi + BLE RF Intelligence Platform

# Overview
At its core, WIFIBLE captures 802.11 frames, extracts metadata, classifies devices, assigns unique IDs, and logs or displays threat‑relevant events.

# Core Components

### 1. Wi‑Fi Packet Sniffer
The Wi‑Fi subsystem runs in promiscuous mode and processes every captured frame:
- Extracts MAC addresses, RSSI, channel, frame type/subtype
- Tracks access points and clients separately
- Maintains per‑device state (scores, timestamps, threat reasons)
- Performs canonical MAC attribution to avoid duplicates
- Detects suspicious patterns such as:
- deauthentication floods
- rapid probe bursts
- abnormal RSSI swings
- 
Refactoring Achievements
- MAC assignment bugs
- Device indexing mismatches
- Vector copy heap corruption
- Cross‑module visibility issues
Each device is now represented by a stable canonical key, and all scoring/alert logic is tied to that key.

### 2. BLE Sniffer (NimBLE)
Running in parallel with Wi‑Fi, the BLE subsystem:
- Scans for BLE advertisements
- Extracts MAC, RSSI, payload flags
- Assigns unique BLE device IDs
- Scores suspicious behavior (rotating MACs, high‑rate bursts)
- Stores alerts per device, not in a global ring buffer
BLE alert logic is now aligned with Wi‑Fi so both behave consistently.

### 3. Unified Alert System
Both Wi‑Fi and BLE feed into a shared alert pipeline:
- Alerts have severity: INFO, WARN, CRITICAL
- Each alert stores:
- timestamp
- device index
- message text
- score contribution
- LED indicators reflect severity
- Alerts are stored per device, not globally
- Display and SD logging read from the same canonical structures
This system has evolved from a simple ring buffer into a per‑device telemetry pipeline.

### 4. Touchscreen UI (TFT_eSPI)
The UI displays two main tables:

Wi‑Fi Device Table
- MAC (color‑coded by threat level)
- Unique device ID
- Channel
- RSSI
- Score
- Threat reasons
  
BLE Device Table
- MAC
- Unique BLE ID
- RSSI
- Score
- Flags / reasons
 

### 5. CLI System
A lightweight command‑line interface provides:
- Diagnostics
- Forcing alerts
- Resetting tables
- Triggering test events
- Dumping device lists
- 
Refactoring Goals
- Use canonical device keys
- Avoid cross‑file static linkage issues
- Cleanly expose commands
- Improve HELP and STATUS output
The CLI is becoming a proper developer console.

### 6. SD Logging
The system logs:
- Alerts
- Device discoveries
- Suspicious events
- System status
- 
Logging Guarantees
- Consistent formatting
- Correct timestamps
- Non‑blocking writes
- No heap fragmentation

#### Design Philosophy
Reliability First
Every subsystem is hardened against:
- timing issues
- heap corruption
- cross‑core race conditions
- bad vector usage
- inconsistent device attribution
Maintainability
The architecture emphasizes:
- modular code
- clear boundaries
- canonical device keys
- predictable behavior
Extensibility
The long‑term vision includes:
- distributed RF intelligence
- mesh‑based threat sharing
- ML‑driven scoring
- unified telemetry pipelines
This is not a toy sniffer — it’s the foundation of a scalable security platform.

#### Current Focus Areas
Recent development has centered on:
- Fixing linker visibility issues (static vs non‑static functions)
- Finalizing canonical device attribution
- Stabilizing Wi‑Fi and BLE alert display tables
- Ensuring per‑device alert storage is bulletproof
- Cleaning up CLI commands and HELP output
- Eliminating cross‑module signature mismatches
- Hardening display rendering against timing crashes
The architecture is now solidifying into a robust, extensible system.

License
 GPL v3.0 (General Public License) 

Contributions
Actively looking for assistance to develop and maintain this project, while feature suggestions are welcome.

