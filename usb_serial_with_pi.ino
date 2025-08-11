#include "HX711.h"

#define LOADCELL_DOUT_PIN  3
#define LOADCELL_SCK_PIN   2

HX711 scale;

// Start with an approximate calibration factor.
// Adjust this during calibration until you get correct grams.
float calibration_factor = 90000.0;

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 Calibration Sketch (Grams)");
  Serial.println("Make sure scale is empty. Taring...");

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  delay(1000);             // Allow time to stabilize
  scale.set_scale();       // Set scale without calibration factor for taring
  scale.tare();            // Set zero baseline

  long zero_factor = scale.read_average(); // Optional: for permanent tare value
  Serial.print("Zero factor: ");
  Serial.println(zero_factor);
}

void loop() {
  scale.set_scale(calibration_factor); // Apply the current calibration factor

  int grams = scale.get_units(10) * 453.592; // Take average of 10 readings and convert to grams

 
  Serial.println(grams); // Show one decimal point


  // Adjust calibration factor from serial input
  if (Serial.available()) {
    char key = Serial.read();
    if (key == '+' || key == 'a') {
      calibration_factor += 10;
    } else if (key == '-' || key == 'z') {
      calibration_factor -= 10;
    }
  }

  delay(500); // Reduce serial flooding
}
