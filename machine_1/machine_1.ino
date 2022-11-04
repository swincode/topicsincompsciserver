
#define LED_PIN 9
#define COM_PIN 8
#define BUTTON_PIN 7

void setup() {
  Serial.begin(9600);             // Initiliase Serial
  pinMode(LED_PIN, OUTPUT);       // Initialise Scanner LED
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);

  pinMode(COM_PIN, OUTPUT);       // Initialise communication led
  digitalWrite(COM_PIN, LOW);

}

void loop() {
  // put your main code here, to run repeatedly:
  btn.tick();
  if (Serial.available() > 0) {

    digitalWrite(COM_PIN, HIGH);
    String command = Serial.readString();
    command.trim();

    if (command == "init") {
      Serial.write("scanner\n");
    }

    if (command == "scan") {
      digitalWrite(LED_PIN, HIGH);
      delay(2000);
      digitalWrite(LED_PIN, LOW);
      Serial.write("done\n");
    }

    digitalWrite(COM_PIN, LOW);

  }
}
