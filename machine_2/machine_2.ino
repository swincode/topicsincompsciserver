
#include <Servo.h>

#define SERVO_X_PIN 5
#define SERVO_Y_PIN 6
#define LED_PIN 9

Servo servo_x, servo_y;

#define MACHINE_TYPE "sorter"

void setup() {
  // Initialise Serial driver
  Serial.begin(9600);

  // Initialise LED
  pinMode(LED_PIN, OUTPUT);
  
  // Initialise motor controllers
  servo_x.attach(SERVO_X_PIN);
  servo_y.attach(SERVO_Y_PIN);
  
  // Set default position
  set_motor_xy_position(1);

}

void loop() {
  if (Serial.available() > 0) {
    digitalWrite(LED_PIN, HIGH);
    String command = Serial.readString();
    command.trim();
    if (command == "init") {
      Serial.write("mover\n");
    }
    if (command == "move_product") {
      set_motor_xy_position(180);
      Serial.write("complete\n");
      delay(1500);
      set_motor_xy_position(1);
    }
    digitalWrite(LED_PIN, LOW);
  }
}

void set_motor_xy_position(int pos) {
  servo_y.write(pos);
  servo_x.write(pos);
}
void set_motor_x_position(int pos) {
  servo_x.write(pos);
}

void set_motor_y_position(int pos) {
  servo_y.write(pos);
}
