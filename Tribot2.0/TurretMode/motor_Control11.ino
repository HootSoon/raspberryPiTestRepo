#include <Servo.h>

// H-Bridge motor driver pins (Arduino)
const int IN1 = 5;
const int IN2 = 4;
const int ENA = 6;
const int IN3 = 12;
const int IN4 = 10;
const int ENB = 11;

// Servo motor pins
const int SERVO1_PIN = 8;
const int SERVO2_PIN = 9;

// Motor speeds
int sp1 = 45; // Adjust as needed
int sp2 = 45; // Adjust as needed

String receivedCommand;

Servo servo1;
Servo servo2;

void setup() {
    Serial.begin(9600);

    // Motor control pins
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(ENA, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(ENB, OUTPUT);

    pinMode(LED_BUILTIN, OUTPUT);

    // Attach servos
    servo1.attach(SERVO1_PIN);
    servo2.attach(SERVO2_PIN);

    Serial.println("Setup complete. Waiting for commands...");
}

void loop() {
  digitalWrite(LED_BUILTIN,LOW);
    if (Serial.available()) {
        receivedCommand = Serial.readStringUntil('\n');
        receivedCommand.trim();
        Serial.print("Received: ");
        Serial.println(receivedCommand);
        processCommand(receivedCommand);
    }
}

void processCommand(String command) {
    if (command.startsWith("SERVO1")) {
        int angle = command.substring(7).toInt();
        servo1.write(angle);
        Serial.print("Moved SERVO1 to ");
        Serial.println(angle);
    } else if (command.startsWith("SERVO2")) {
        int angle = command.substring(7).toInt();
        servo2.write(angle);
        Serial.print("Moved SERVO2 to ");
        Serial.println(angle);
    } else{
        int xPos = command.toInt();
        if(xPos <= 310 && xPos > 0){
          turnLeft();
        }else if(xPos >= 370){
          turnRight();
          
        }else{
          stopMotors();
        }
        digitalWrite(LED_BUILTIN, HIGH);
          
        
    }
}

// Motor control functions
void moveForward() {
    Serial.println("Moving Forward");
    Motor1_Forward(sp1);
    Motor2_Forward(sp2);
    delay(1000);
    stopMotors();
}

void moveBackward() {
    Serial.println("Moving Backward");
    Motor1_Backward(sp1);
    Motor2_Backward(sp2);
    delay(1000);
    stopMotors();
}

void turnRight() {
    Serial.println("Turning Left");
    Motor1_Backward(sp1);
    Motor2_Forward(sp2);
    //delay(200);
    //stopMotors();
}

void turnLeft() {
    Serial.println("Turning Right");
    Motor1_Forward(sp1);
    Motor2_Backward(sp2);
    //delay(200);
    //stopMotors();
}

void stopMotors() {
    Serial.println("Stopping Motors");
    Motor1_Brake();
    Motor2_Brake();
}

// Motor 1 functions
void Motor1_Forward(int Speed) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, Speed);
}

void Motor1_Backward(int Speed) {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENA, Speed);
}

void Motor1_Brake() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
}

// Motor 2 functions
void Motor2_Forward(int Speed) {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, Speed);
}

void Motor2_Backward(int Speed) {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENB, Speed);
}

void Motor2_Brake() {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}
