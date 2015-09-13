/**
 * Sketch to sense humidity and temperature with dht sensor.
 * 
 * Also has control of servo for treat dispener.
 */

#include "DHT.h"
#include "Servo.h"

#define DHTPIN 2

#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

Servo treat_servo;

int choice = 0;

long interval = 400;
unsigned long timer = 0;

void setup() {
  Serial.begin(9600);

  treat_servo.attach(3);
  treat_servo.write(180);

  dht.begin();
}

void get_input() {
  choice = Serial.read();
}

void sense_dht() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  // output data
  Serial.print(h);
  Serial.print(",");
  Serial.print(t);
  Serial.print(",");
  Serial.print(f);
  Serial.print(",");
  Serial.print(hic);
  Serial.print(",");
  Serial.print(hif);
  Serial.print("\n");
}

void give_treat() {
  Serial.println("dispensing treats");
  treat_servo.write(0);

  timer = millis();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  get_input();

  if (choice == 's') {
    sense_dht();
  }
  else if (choice == 't') {
    give_treat();
  }

  unsigned long currentMillis = millis();
  
  if (currentMillis - timer > interval || choice == 's') {
    treat_servo.write(180);
    choice = 'n';
  }

}
