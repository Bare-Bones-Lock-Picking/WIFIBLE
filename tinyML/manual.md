# Open Powershell as admin and run  

1. Run script generate_dataset.py. This generates all the csv files needed

2. Run script wifi_training.py to generate TFLite model - wifi_model.tflite

3. Run script ble_training.py to generate TFLite model – ble_model.tflite

4. Create py script below to convert .tflite file to .cpp – THEN REPEAT BY CHANGING THE 
'wifi_' SECTON TO 'ble_' AND REPEAT
------------------------------------------------------------------------------------------
import pathlib

TFLITE_PATH = "wifi_model.tflite"
CPP_PATH    = "wifi_model_data.cpp"
SYMBOL_NAME = "wifi_model_tflite"

data = pathlib.Path(TFLITE_PATH).read_bytes()

with open(CPP_PATH, "w") as f:
    f.write('#include "ble_model_data.h"\n\n')
    f.write(f"const unsigned char {SYMBOL_NAME}[] = {{\n")

    # 12 bytes per line, Option B style
    for i in range(0, len(data), 12):
        chunk = data[i:i+12]
        hex_bytes = ", ".join(f"0x{b:02x}" for b in chunk)
        f.write(f"    {hex_bytes},\n")

    f.write("};\n\n")
    f.write(f"const unsigned int {SYMBOL_NAME}_len = sizeof({SYMBOL_NAME});\n")
--------------------------------------------------------------------------------------------


