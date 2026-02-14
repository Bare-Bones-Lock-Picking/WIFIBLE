import csv
import random
import pandas as pd
import os

# ============================================================
# BLE FEATURE SCHEMA (39 columns)
# ============================================================

BLE_COLUMNS = [
    "avgRSSI","avgVar","advCount","uniqueDevices","rotationEvents","spamEvents",
    "impersonationEvents","appleMfgEvents","tileMfgEvents","samsungMfgEvents",
    "appleSubtypeAnomalyEvents","microsoftSubtypeAnomalyEvents",
    "samsungSubtypeAnomalyEvents","appleNameEvents","windowsNameEvents",
    "samsungNameEvents","androidNameEvents","ninebotNameEvents",
    "highRateEvents","veryHighRateEvents","highVarianceEvents","floodingEvents",
    "lowVarCloseEvents","longPresenceEvents","veryCloseEvents","closeEvents",
    "spoofingEvents","serviceUUIDAnomalyEvents","manuFloodEvents",
    "payloadSpamEvents","evilTwinEvents","samsungSpamEvents","appleSourEvents",
    "appleJuiceEvents","flipperEvents","swiftPairEvents","googleFastPairEvents",
    "samsungTelemetryEvents","label"
]

# ============================================================
# WIFI FEATURE SCHEMA (41 columns)
# ============================================================

WIFI_COLUMNS = [
    "rssiMean","rssiVar","pktCount","beaconCount","probeCount","deauthCount",
    "authCount","assocReqCount","assocRespCount","nullCount","uniqueDevices",
    "uniqueAPs","uniqueClients","spoofEvents","bssidMismatchEvents",
    "ssidImpersonationEvents","vendorIEAnomalyEvents","wpaIEAnomalyEvents",
    "rsnAnomalyEvents","htCapabilitiesAnomalyEvents","wmmAnomalyEvents",
    "beaconFloodEvents","probeFloodEvents","deauthFloodEvents","nullFloodEvents",
    "authFloodEvents","assocFloodEvents","vendorSpecificSpamEvents",
    "channelHopEvents","intervalAnomalyEvents","burstEvents","highRateEvents",
    "veryHighRateEvents","longPresenceEvents","closeRangeEvents",
    "veryCloseRangeEvents","label"
]

# ============================================================
# BLE SYNTHETIC GENERATORS
# ============================================================

def ble_normal():
    return {
        "avgRSSI": random.uniform(-90, -40),
        "avgVar": random.uniform(0.1, 1.0),
        "advCount": random.randint(20, 80),
        "uniqueDevices": random.randint(3, 15),
        "rotationEvents": 0,
        "spamEvents": 0,
        "impersonationEvents": 0,
        "appleMfgEvents": random.randint(0, 5),
        "tileMfgEvents": random.randint(0, 3),
        "samsungMfgEvents": random.randint(0, 3),
        "appleSubtypeAnomalyEvents": 0,
        "microsoftSubtypeAnomalyEvents": 0,
        "samsungSubtypeAnomalyEvents": 0,
        "appleNameEvents": random.randint(0, 3),
        "windowsNameEvents": random.randint(0, 3),
        "samsungNameEvents": random.randint(0, 3),
        "androidNameEvents": random.randint(0, 3),
        "ninebotNameEvents": random.randint(0, 2),
        "highRateEvents": 0,
        "veryHighRateEvents": 0,
        "highVarianceEvents": 0,
        "floodingEvents": 0,
        "lowVarCloseEvents": 0,
        "longPresenceEvents": 0,
        "veryCloseEvents": 0,
        "closeEvents": 0,
        "spoofingEvents": 0,
        "serviceUUIDAnomalyEvents": 0,
        "manuFloodEvents": 0,
        "payloadSpamEvents": 0,
        "evilTwinEvents": 0,
        "samsungSpamEvents": 0,
        "appleSourEvents": 0,
        "appleJuiceEvents": 0,
        "flipperEvents": 0,
        "swiftPairEvents": 0,
        "googleFastPairEvents": 0,
        "samsungTelemetryEvents": 0,
        "label": 0
    }

def ble_spam():
    w = ble_normal()
    w.update({
        "advCount": random.randint(300, 2000),
        "spamEvents": random.randint(5, 20),
        "highRateEvents": random.randint(5, 15),
        "veryHighRateEvents": random.randint(2, 8),
        "label": 1
    })
    return w

def ble_beacon_storm():
    w = ble_normal()
    w.update({
        "advCount": random.randint(500, 3000),
        "floodingEvents": random.randint(5, 20),
        "highVarianceEvents": random.randint(5, 20),
        "label": 1
    })
    return w

def ble_connectable():
    w = ble_normal()
    w.update({
        "rotationEvents": random.randint(5, 20),
        "spoofingEvents": random.randint(1, 5),
        "label": 2
    })
    return w

def ble_impersonation():
    w = ble_normal()
    w.update({
        "impersonationEvents": random.randint(5, 20),
        "spoofingEvents": random.randint(5, 20),
        "label": 3
    })
    return w

def ble_rotation():
    w = ble_normal()
    w.update({
        "rotationEvents": random.randint(10, 50),
        "label": 2
    })
    return w

def ble_noise():
    w = ble_normal()
    if random.random() < 0.1:
        w["highRateEvents"] = random.randint(1, 3)
    if random.random() < 0.1:
        w["impersonationEvents"] = random.randint(1, 3)
    w["label"] = 0
    return w

def ble_blend():
    w = ble_normal()
    if random.random() < 0.5:
        w["spamEvents"] += random.randint(5, 20)
    if random.random() < 0.5:
        w["impersonationEvents"] += random.randint(5, 20)
    if random.random() < 0.5:
        w["rotationEvents"] += random.randint(5, 20)
    w["label"] = random.choice([1, 2, 3])
    return w

def ble_fuzz():
    w = {c: random.randint(0, 200) for c in BLE_COLUMNS if c != "label"}
    w["avgRSSI"] = random.uniform(-95, -35)
    w["avgVar"] = random.uniform(0, 5)
    w["label"] = random.randint(0, 3)
    return w

# ============================================================
# WIFI SYNTHETIC GENERATORS
# ============================================================

def wifi_normal():
    return {
        "rssiMean": random.uniform(-85, -45),
        "rssiVar": random.uniform(0.1, 1.0),
        "pktCount": random.randint(20, 80),
        "beaconCount": random.randint(5, 20),
        "probeCount": random.randint(2, 10),
        "deauthCount": 0,
        "authCount": random.randint(1, 5),
        "assocReqCount": random.randint(1, 5),
        "assocRespCount": random.randint(1, 5),
        "nullCount": random.randint(0, 5),
        "uniqueDevices": random.randint(3, 12),
        "uniqueAPs": random.randint(1, 4),
        "uniqueClients": random.randint(2, 8),
        "spoofEvents": 0,
        "bssidMismatchEvents": 0,
        "ssidImpersonationEvents": 0,
        "vendorIEAnomalyEvents": 0,
        "wpaIEAnomalyEvents": 0,
        "rsnAnomalyEvents": 0,
        "htCapabilitiesAnomalyEvents": 0,
        "wmmAnomalyEvents": 0,
        "beaconFloodEvents": 0,
        "probeFloodEvents": 0,
        "deauthFloodEvents": 0,
        "nullFloodEvents": 0,
        "authFloodEvents": 0,
        "assocFloodEvents": 0,
        "vendorSpecificSpamEvents": 0,
        "channelHopEvents": 0,
        "intervalAnomalyEvents": 0,
        "burstEvents": 0,
        "highRateEvents": 0,
        "veryHighRateEvents": 0,
        "longPresenceEvents": 0,
        "closeRangeEvents": 0,
        "veryCloseRangeEvents": 0,
        "label": 0
    }

def wifi_flood():
    w = wifi_normal()
    w.update({
        "pktCount": random.randint(500, 2000),
        "beaconCount": random.randint(200, 800),
        "probeCount": random.randint(200, 800),
        "nullCount": random.randint(100, 400),
        "beaconFloodEvents": random.randint(5, 20),
        "probeFloodEvents": random.randint(5, 20),
        "nullFloodEvents": random.randint(5, 20),
        "vendorSpecificSpamEvents": random.randint(1, 10),
        "highRateEvents": random.randint(5, 15),
        "veryHighRateEvents": random.randint(2, 8),
        "uniqueDevices": random.randint(20, 80),
        "uniqueAPs": random.randint(5, 20),
        "uniqueClients": random.randint(10, 40),
        "label": 1
    })
    return w

def wifi_beacon_storm():
    w = wifi_normal()
    w.update({
        "pktCount": random.randint(800, 2000),
        "beaconCount": random.randint(500, 1500),
        "beaconFloodEvents": random.randint(10, 30),
        "vendorIEAnomalyEvents": random.randint(5, 20),
        "uniqueAPs": random.randint(20, 60),
        "uniqueDevices": random.randint(30, 100),
        "label": 1
    })
    return w

def wifi_connectable():
    w = wifi_normal()
    w.update({
        "authCount": random.randint(20, 100),
        "assocReqCount": random.randint(20, 100),
        "assocRespCount": random.randint(20, 100),
        "ssidImpersonationEvents": random.randint(1, 5),
        "wpaIEAnomalyEvents": random.randint(1, 5),
        "rsnAnomalyEvents": random.randint(1, 5),
        "uniqueAPs": random.randint(2, 10),
        "uniqueClients": random.randint(5, 20),
        "label": 2
    })
    return w

def wifi_impersonation():
    w = wifi_normal()
    w.update({
        "ssidImpersonationEvents": random.randint(3, 10),
        "bssidMismatchEvents": random.randint(3, 10),
        "vendorIEAnomalyEvents": random.randint(2, 8),
        "wpaIEAnomalyEvents": random.randint(2, 8),
        "rsnAnomalyEvents": random.randint(2, 8),
        "uniqueAPs": random.randint(1, 5),
        "uniqueClients": random.randint(1, 10),
        "label": 2
    })
    return w

def wifi_deauth():
    w = wifi_normal()
    w.update({
        "deauthCount": random.randint(50, 300),
        "deauthFloodEvents": random.randint(5, 20),
        "nullFloodEvents": random.randint(2, 10),
        "uniqueDevices": random.randint(5, 20),
        "label": 3
    })
    return w

def wifi_noise():
    w = wifi_normal()
    if random.random() < 0.1:
        w["highRateEvents"] = random.randint(1, 3)
    if random.random() < 0.1:
        w["vendorIEAnomalyEvents"] = random.randint(1, 2)
    if random.random() < 0.05:
        w["ssidImpersonationEvents"] = random.randint(1, 2)
    w["label"] = 0
    return w

def wifi_blend():
    w = wifi_normal()
    if random.random() < 0.5:
        f = wifi_flood()
        for k in f:
            if k != "label":
                w[k] += f[k] // 2
    if random.random() < 0.5:
        i = wifi_impersonation()
        for k in i:
            if k != "label":
                w[k] += i[k]
    if random.random() < 0.5:
        d = wifi_deauth()
        for k in d:
            if k != "label":
                w[k] += d[k]
    w["label"] = random.choice([1, 2, 3])
    return w

def wifi_fuzz():
    w = {c: random.randint(0, 200) for c in WIFI_COLUMNS if c != "label"}
    w["rssiMean"] = random.uniform(-95, -35)
    w["rssiVar"] = random.uniform(0, 5)
    w["label"] = random.randint(0, 3)
    return w

# ============================================================
# CSV WRITER
# ============================================================

def write_csv(filename, columns, generator, rows=500):
    print(f"Generating {filename}...")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for _ in range(rows):
            row = generator()
            writer.writerow([row[c] for c in columns])

# ============================================================
# MODE MAPS
# ============================================================

BLE_MODES = {
    "ble_normal.csv": ble_normal,
    "ble_spam.csv": ble_spam,
    "ble_beacon_storm.csv": ble_beacon_storm,
    "ble_connectable.csv": ble_connectable,
    "ble_impersonation.csv": ble_impersonation,
    "ble_rotation_abuse.csv": ble_rotation,
    "ble_mixed_noise.csv": ble_noise,
    "ble_attack_blend.csv": ble_blend,
    "ble_fuzz.csv": ble_fuzz,
}

WIFI_MODES = {
    "wifi_normal.csv": wifi_normal,
    "wifi_flood.csv": wifi_flood,
    "wifi_beacon_storm.csv": wifi_beacon_storm,
    "wifi_connectable.csv": wifi_connectable,
    "wifi_impersonation.csv": wifi_impersonation,
    "wifi_deauth.csv": wifi_deauth,
    "wifi_mixed_noise.csv": wifi_noise,
    "wifi_attack_blend.csv": wifi_blend,
    "wifi_fuzz.csv": wifi_fuzz,
}

# ============================================================
# MERGE FUNCTION
# ============================================================

def merge_family(prefix, mapping, columns, out_file, balance=True):
    dfs = []
    for fname in mapping.keys():
        if os.path.exists(fname):
            df = pd.read_csv(fname)
            dfs.append(df)
        else:
            print(f"[{prefix}] Missing {fname}")

    if not dfs:
        print(f"[{prefix}] No files found")
        return

    if balance:
        min_len = min(len(df) for df in dfs)
        dfs = [df.sample(min_len, random_state=42) for df in dfs]

    merged = pd.concat(dfs, ignore_index=True)
    merged = merged.sample(frac=1, random_state=42).reset_index(drop=True)
    merged.to_csv(out_file, index=False)
    print(f"[{prefix}] Saved {out_file}")

# ============================================================
# MAIN EXECUTION
# ============================================================

# Generate BLE CSVs
for filename, gen in BLE_MODES.items():
    write_csv(filename, BLE_COLUMNS, gen)

# Generate Wi-Fi CSVs
for filename, gen in WIFI_MODES.items():
    write_csv(filename, WIFI_COLUMNS, gen)

# Merge BLE
merge_family("BLE", BLE_MODES, BLE_COLUMNS, "ble_training_dataset.csv")

# Merge Wi-Fi
merge_family("WIFI", WIFI_MODES, WIFI_COLUMNS, "wifi_training_dataset.csv")

print("All BLE + Wi-Fi datasets generated and merged successfully.")