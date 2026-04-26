#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "TP-Link_31CA";
const char* password = "54299979";

const char* serverUrl = "http://192.168.1.106:5000/api/sensor";

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.print("WiFi connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  float temperature = random(200, 350) / 10.0;  // 20.0 ~ 35.0
  float humidity = random(400, 800) / 10.0;     // 40.0 ~ 80.0
  int soilMoisture = random(0, 101);            // 0 ~ 100
  int light = random(0, 101);                   // 0 ~ 100

  Serial.print("Temperature: ");
  Serial.println(temperature);

  Serial.print("Humidity: ");
  Serial.println(humidity);

  Serial.print("Soil moisture: ");
  Serial.println(soilMoisture);

  Serial.print("Light: ");
  Serial.println(light);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{";
    jsonData += "\"device_id\":\"esp32_dummy\",";
    jsonData += "\"temperature\":" + String(temperature, 2) + ",";
    jsonData += "\"humidity\":" + String(humidity, 2) + ",";
    jsonData += "\"soil_moisture\":" + String(soilMoisture) + ",";
    jsonData += "\"light\":" + String(light);
    jsonData += "}";

    int responseCode = http.POST(jsonData);

    Serial.print("Send: ");
    Serial.println(jsonData);

    Serial.print("Response code: ");
    Serial.println(responseCode);

    String response = http.getString();
    Serial.println(response);

    http.end();
  } else {
    Serial.println("WiFi disconnected");
  }

  delay(5000);
}