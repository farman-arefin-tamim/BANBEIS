#define PH_PIN 32  // GPIO32 (D32) where the pH sensor is connected

float voltage, pHValue;
const float VREF = 3.3;      // ESP32 ADC reference voltage
const int ADC_RES = 4096;    // 12-bit ADC resolution
float offset = 17.625;          // Adjust after calibration
float slope = -7.43;          // Adjust after calibration

void setup() {
  Serial.begin(115200);
  pinMode(PH_PIN, INPUT);
  Serial.println("Start pH Sensor Calibration");
}

void loop() {
  int analogValue = analogRead(PH_PIN);  // Read raw analog value
  voltage = (analogValue * VREF) / ADC_RES;  // Convert to voltage
  pHValue = slope * voltage + offset;  // Calculate pH based on slope and offset
  
  Serial.print("Analog Value: ");
  Serial.println(analogValue);
  Serial.print("Voltage: ");
  Serial.println(voltage, 2);
  Serial.print("pH Value (Calibrated): ");
  Serial.println(pHValue, 2);
  
  delay(1000);  // Delay for readability
}
