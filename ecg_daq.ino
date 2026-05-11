void setup() {
  Serial.begin(115200);
}

void loop() {
  int valor_sensor = analogRead(A0);
  float voltaje = valor_sensor * (5.0 / 1023.0);
  Serial.println(voltaje);
  delay(4); 
}