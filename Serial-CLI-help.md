# WiFi/BLE Security Scanner – Serial CLI Manual

## Overview

The device includes a compact, non‑blocking command‑line interface (CLI) accessible over the serial port.  
Commands are grouped into functional categories:

| Category | Meaning |
|---------|---------|
| **W**   | Wi‑Fi detection controls |
| **B**   | BLE detection controls |
| **A**   | Alert visibility controls |
| **S**   | System controls |
| **E**   | Echo mode |
| **H**   | Help |
| **ST**  | Status summary |

Multiple commands may be entered on a single line.  
Separators are optional — the parser accepts:

- spaces  
- commas  
- no separators at all

---

# System Status (`ST`)

Displays a full snapshot of all system feature flags, alert settings, and runtime options.


### WiFi Feature Flags
- **BeaconFlood** – Detect excessive beacon frames  
- **Spoofing** – Detect MAC spoofing attempts  
- **Interval** – Detect abnormal beacon/probe intervals  
- **VendorIE** – Detect malformed or suspicious vendor IEs  
- **PurgeVerbose** – Show logs for purged WiFi devices  

### BLE Feature Flags
- **Spam** – Detect BLE advertisement spam  
- **Rotation** – Detect rotating MAC patterns  
- **Impersonation** – Detect BLE identity spoofing  
- **PurgeVerbose** – Show logs for purged BLE devices  

### Alert Flags
- **INFO**  
- **WARN**  
- **CRITICAL**  
- **ALL** – Master toggle for all alert levels  

### System Flags
- **DebugLogs** – Enable/disable verbose system logging  
- **LEDs** – Master LED enable/disable  
- **LED on Alerts** – Flash LED when alerts occur  
- **EchoMode** – Echo CLI input back to the terminal  

---

# Help (`H`)

Displays the full command reference.


---

# WiFi Commands

| Command | Description |
|--------|-------------|
| `W1`   | Enable beacon‑flood detection |
| `W1-`  | Disable beacon‑flood detection |
| `W2`   | Enable spoofing detection |
| `W2-`  | Disable spoofing detection |
| `W3`   | Enable interval anomaly detection |
| `W3-`  | Disable interval anomaly detection |
| `W4`   | Enable vendor‑IE anomaly detection |
| `W4-`  | Disable vendor‑IE anomaly detection |
| `W5`   | Enable probe‑flood detection |
| `W5-`  | Disable probe‑flood detection |
| `W6`   | Enable null‑flood detection |
| `W6-`  | Disable null‑flood detection |
| `RW<n>` | Show raw WiFi payload history for device index n |
| `CW`   | Clear WiFi raw‑packet history |
| `LW`   | List WiFi devices |
| `PW`   | Toggle verbose logging for purged WiFi devices |

---

# BLE Commands

| Command | Description |
|--------|-------------|
| `B1`   | Enable BLE spam detection |
| `B1-`  | Disable BLE spam detection |
| `B2`   | Enable BLE rotation detection |
| `B2-`  | Disable BLE rotation detection |
| `B3`   | Enable BLE impersonation detection |
| `B3-`  | Disable BLE impersonation detection |
| `RB<n>` | Show raw BLE payload history for device index n |
| `CB`   | Clear BLE raw‑packet history |
| `LB`   | List BLE devices |
| `PB`   | Toggle verbose logging for purged BLE devices |

---

# Alert Commands

| Command | Description |
|--------|-------------|
| `AI` | Toggle INFO alerts |
| `AW` | Toggle WARN alerts |
| `AC` | Toggle CRITICAL alerts |
| `AA` | Toggle ALL alerts |

---

# System Commands

| Command | Description |
|--------|-------------|
| `S1`   | Enable debug logs |
| `S1-`  | Disable debug logs |
| `S2`   | Reboot device |
| `E1`   | Enable echo mode |
| `E1-`  | Disable echo mode |

---

# Information / Export Commands

| Command | Description |
|--------|-------------|
| `ST` | Show system status |
| `HF` | Show detailed feature‑flag help |
| `JF` | Export all feature flags as JSON |
| `LT` | Toggle LED‑on‑alerts mode |

