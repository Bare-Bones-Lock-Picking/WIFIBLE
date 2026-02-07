# WiFi/BLE Security Scanner – Serial CLI Manual

## Overview

The device includes a compact, non‑blocking command‑line interface (CLI) accessible over the serial port.  
Commands are grouped into functional categories:

| Category | Meaning |
|---------|---------|
| **W**   | Wi‑Fi detection controls |
| **B**   | BLE detection controls |
| **S**   | System controls |
| **E**   | Echo mode |
| **H**   | Help |
| **ST**  | Status summary |

Multiple commands may be entered on a single line.  
Separators are optional — the parser accepts:

- spaces  
- commas  
- no separators at all  

### Examples

```
W1 W2- B1
W1,W2-,B3
W1W2-B1S1
```

After processing a line, the device prints:

```
OK
```

Some commands (like `ST` or `H`) print a short one‑line response.

---

## Wi‑Fi Commands (W)

| Command | Description |
|---------|-------------|
| `W1`  | Enable Wi‑Fi beacon flood detection |
| `W1-` | Disable Wi‑Fi beacon flood detection |
| `W2`  | Enable Wi‑Fi spoofing detection |
| `W2-` | Disable Wi‑Fi spoofing detection |
| `W3`  | Enable Wi‑Fi interval anomaly detection |
| `W3-` | Disable Wi‑Fi interval anomaly detection |
| `W4`  | Enable Wi‑Fi vendor IE anomaly detection |
| `W4-` | Disable Wi‑Fi vendor IE anomaly detection |

### Examples

```
W1 W2-       # Enable beacon flood, disable spoofing
W1W2W3W4     # Enable all Wi‑Fi detection
W1-W2-W3-W4- # Disable all Wi‑Fi detection
```

---

## BLE Commands (B)

| Command | Description |
|---------|-------------|
| `B1`  | Enable BLE spam detection |
| `B1-` | Disable BLE spam detection |
| `B2`  | Enable BLE rotation detection |
| `B2-` | Disable BLE rotation detection |
| `B3`  | Enable BLE impersonation detection |
| `B3-` | Disable BLE impersonation detection |

### Examples

```
B1- B2- B3-  # Disable all BLE detection
B1B2B3       # Enable all BLE detection
```

---

## System Commands (S)

| Command | Description |
|---------|-------------|
| `S1`  | Enable debug logs |
| `S1-` | Disable debug logs |
| `S2`  | Reboot the device |

### Examples

```
S1 S2   # Enable debug logs and reboot
S1-     # Disable debug logs
```

---

## Status Command

### `ST`

Prints a compact one‑line summary of all Wi‑Fi, BLE, and system flags.

**Example output**

```
W:1101 B:101 S:10
```

**Bit order**

- **Wi‑Fi:** beacon flood, spoofing, interval anomalies, vendor IE  
- **BLE:** spam, rotation, impersonation  
- **System:** debug logs, LEDs (if used)

---

## Help Command

### `H`

Prints a compact list of available commands:

```
W1/2/3/4, B1/2/3, S1/2, ST, E1
```

---

## Echo Mode (E)

| Command | Description |
|---------|-------------|
| `E1`  | Enable echo mode |
| `E1-` | Disable echo mode |

### Example

Input:
```
E1
W1 W2-
```

Output:
```
W1 W2-
OK
```

---

## Combining Commands

You can combine multiple commands in a single line.

**With spaces**
```
W1 W2- B1 S1
```

**With commas**
```
W1,W2-,B1,S1
```

**With no separators**
```
W1W2-B1S1
```

All forms are valid.

---

## Behavior and Safety Notes

- The CLI is **non‑blocking** and safe to use with the TFT display.  
- Commands are processed with **no dynamic memory allocation**.  
- Unknown commands are ignored silently.  
- After processing a line, the device prints `OK` unless a command prints its own response.  
- The CLI does **not** interfere with Wi‑Fi/BLE sniffing or display updates.
