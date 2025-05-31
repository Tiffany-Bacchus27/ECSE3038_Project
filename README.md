ECSE3038_Project: Simple Smart Hub

Overview

The Simple Smart Hub is an IoT project designed to control appliances (a fan and a light) based on environmental conditions such as temperature, presence, and user-defined time settings. The system integrates an ESP32 microcontroller, a FastAPI backend, and a web interface to manage and visualize sensor data. This project was developed as part of the ECSE3038 course, showcasing IoT system design and integration.

ECSE3038_Project/
├── api/
│   ├── app.py              # FastAPI backend server
│   └── requirements.txt    # Python dependencies
├── embedded/
│   ├── platformio.ini      # PlatformIO configuration for ESP32
│   ├── wokwi.toml          # Wokwi simulation configuration
│   └── src/
│       └── main.cpp        # ESP32 firmware code
├── README.md               # Project documentation
└── .gitignore              # Git ignore file

Setup Instructions

Prerequisites
VSCode: Install Visual Studio Code.
Extensions:
Wokwi Simulator (for ESP32 simulation).
PlatformIO IDE (for embedded development).
Python: Python 3.8+ for the FastAPI backend.
Git: For version control.

Components
ESP32: Central microcontroller running the firmware.
DS18B20: Temperature sensor connected to GPIO4.
PIR sensor for presence detection on GPIO15.
LEDs: Simulate the fan (GPIO23, blue LED) and light (GPIO22, white LED).