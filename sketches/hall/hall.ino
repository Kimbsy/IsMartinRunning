/**
 * Sketch to measure rotation of hamster wheel with magnets attached.
 *
 * Using hall sensor (U18).
 *
 * Pins when looking at model number on sensor:
 *   left   : Vin
 *   middle : ground
 *   right  : output
 */

// declare pin constants
#define HALL_PIN 12
#define LED_PIN 13

// other constants
#define CIRCUMFERENCE 0.44

// variables
int hallState = 0;
int lastTime = 0;   // last time magnetic field was sensed
int totalTime = 0;  // total time during this run
int timeChecks = 0; // how many times magnetic field has been detected this run
int timeDiff = 0;   // time (in miliseconds) since last detection

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(HALL_PIN, INPUT);

  Serial.begin(9600);
}

void flash()
{
  digitalWrite(LED_PIN, HIGH);
  delay(100);
  digitalWrite(LED_PIN, LOW);
}

void calcTime()
{
  timeDiff = millis() - lastTime;
  lastTime = millis();

  // Serial.println(timeDiff);

  if (timeDiff < 2000)
  {
    totalTime += timeDiff;
    timeChecks++;
  }
}

void checkRunning()
{
  int raw = digitalRead(HALL_PIN);

  // Serial.println(raw);

  if (raw != hallState)
  {
    hallState = raw;

    // do timing measurements
    calcTime();

    // flash pin 13 led
    flash();
  }
}

void checkOutput()
{
  // if it's been over 2 seconds since last detection and there has been at least 4 detections, output results of this run
  if (((int)millis() - lastTime) > 2000)
  {
    if (timeChecks >= 4)
    {
      // calculate info to send out
      double averageRotationTime = (totalTime / timeChecks) * 2;
      double speed = CIRCUMFERENCE / (averageRotationTime / 1000);
      double distance = (CIRCUMFERENCE * timeChecks) / 2;

      // send it
      Serial.print(timeChecks);
      Serial.print(",");
      Serial.print(totalTime);
      Serial.print(",");
      Serial.print(averageRotationTime);
      Serial.print(",");
      Serial.print(speed);
      Serial.print(",");
      Serial.print(distance);
      Serial.print("\n");

      // reset variables
      totalTime = 0;
      timeChecks = 0;
      lastTime = millis();
    }
    else
    {
      // just reset variables
      totalTime = 0;
      timeChecks = 0;
      lastTime = millis();
    }
  }
}

void loop(){
  // try to detect change in magnetic field
  checkRunning();

  // determine whether or not to send output
  checkOutput();
}
