#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// WiFi credentials
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// API endpoint
const char* serverName = "https://simple-smart-hub-client.netlify.app";

// GPIO pin definitions
#define FAN_PIN    23    // Blue LED
#define LIGHT_PIN  22    // White LED
#define TEMP_PIN    4    // DS18B20 data
#define PIR_PIN    15    // Motion Sensor OUT

// DS18B20 sensor setup
OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);

  // Configure I/O
  pinMode(FAN_PIN, OUTPUT);
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  sensors.begin();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // Read temperature from DS18B20
    sensors.requestTemperatures();
    float temperature = sensors.getTempCByIndex(0);

    // Read motion sensor
    int motionDetected = digitalRead(PIR_PIN);

    // Control LEDs based on sensor input
    digitalWrite(LIGHT_PIN, motionDetected);              // Turn on light if motion
    digitalWrite(FAN_PIN, temperature > 30.0 ? HIGH : LOW); // Fan if temp > 30°C

    // Send data to server
    HTTPClient http;
    http.begin(String(serverName) + "/sensors");
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"temperature\":" + String(temperature, 1) + 
                     ",\"presence\":" + (motionDetected ? "true" : "false") + "}";
    
    int responseCode = http.POST(payload);

    if (responseCode > 0) {
      Serial.println(" Data sent!");
      Serial.println("Server response: " + http.getString());
    } else {
      Serial.println("Failed to send data. HTTP code: " + String(responseCode));
    }

    http.end();
  } else {
    Serial.println(" WiFi not connected");
  }

  delay(5000); // Wait before next update
}
