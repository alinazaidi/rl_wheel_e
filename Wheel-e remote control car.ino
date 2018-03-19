#Arduino Code for making wheel-e work like a remote control car, using 
#app on android phone which sends bluetooth signals to arduino. 
#Wheel-e will stop if the sonar sensors detects an obstracle in front of car.



#include <NewPing.h>

#define TRIGGER_PIN  3  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     4  // Arduino pin tied to echo pin on the ultrasonic sensor. //9 
#define MAX_DISTANCE 200
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); 


int motor_left[] = {9,8}; //Motor connected to 8 and 9//
int motor_right[] = {10, 11}; ////Motor connected to 10 and 11//
int pwmR = 5;
int pwmL = 6;
int PWMright = 255;//255
int PWMleft =  244;//244
int PWMrightSlow = 180;//180
int PWMleftSlow =  180;//180
int input='0';
boolean stop_motion= false; 

void setup() {
  // put your setup code here, to run once:
pinMode(pwmL, OUTPUT);
pinMode(pwmR, OUTPUT);
int i;
for(i=0; i<2; i++){
  pinMode(motor_left[i], OUTPUT);
  pinMode(motor_right[i], OUTPUT);}  
Serial.begin(9600);
}
void loop() {
 stop_motion = false;
 delay(50);
 if( Serial.available()>0){
   input = Serial.read();
  }
 if(sonar.ping_cm()<=15 and sonar.ping_cm()>0){
    Serial.println(sonar.ping_cm());
    stop_motion = true;
    delay(50);
  }
 if(input == '1'){
  if(stop_motion == true){
    drive_stop();
  }
  else
    drive_forward();
  }  
 else if(input == '2'){
   drive_backward();
  }
 else if(input == '3'){
   drive_right();
  }
 else if(input == '4'){
   drive_left();
  }
 else if(input == '0'){
   drive_stop();
  }
}

void drive_forward(){  // forward //
  analogWrite(pwmL, PWMleft); 
  digitalWrite(motor_left[0], HIGH); //rotates left motor in forward//
  digitalWrite(motor_left[1], LOW); 
  analogWrite(pwmR,PWMright);
  digitalWrite(motor_right[0], HIGH); //rotates right motor in forward//
  digitalWrite(motor_right[1], LOW);
}
void drive_backward(){  // forward //
  analogWrite(pwmL, PWMleft);
  digitalWrite(motor_left[1], HIGH); //rotates left motor in backward//
  digitalWrite(motor_left[0], LOW);
  analogWrite(pwmR,PWMright);
  digitalWrite(motor_right[1], HIGH); //rotates right motor in backward//
  digitalWrite(motor_right[0], LOW); 
}
void drive_left(){ // left //
  analogWrite(pwmL, PWMleftSlow);
  digitalWrite(motor_left[0], LOW);  //rotates left motor in backward//
  digitalWrite(motor_left[1], HIGH);
  analogWrite(pwmR,PWMrightSlow);
  digitalWrite(motor_right[0], HIGH); //rotates right motor in forward//
  digitalWrite(motor_right[1], LOW);
}
void drive_right(){ // right //
  analogWrite(pwmL, PWMleftSlow);
  digitalWrite(motor_left[1], LOW);  //rotates left motor in forward//
  digitalWrite(motor_left[0], HIGH);
  analogWrite(pwmR,PWMrightSlow);
  digitalWrite(motor_right[1], HIGH); //rotates right motor in backward//
  digitalWrite(motor_right[0], LOW);
}
void drive_stop(){  // stop //
  analogWrite(pwmL,0);
  digitalWrite(motor_left[0], LOW);
  digitalWrite(motor_left[1], LOW);
  analogWrite(pwmR,0);
  digitalWrite(motor_right[0], LOW);
  digitalWrite(motor_right[1], LOW);
}
