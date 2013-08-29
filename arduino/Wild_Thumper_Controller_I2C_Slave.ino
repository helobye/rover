#include <Servo.h>
#include <Wire.h>
#include "IOpins.h"
#include "Constants.h"


//-------------------------------------------------------------- define global variables --------------------------------------------

unsigned int volts;
unsigned int lamps;
unsigned int ramps;

unsigned int peakvolt;
unsigned long ctime;
unsigned long stime;

unsigned long leftoverload;
unsigned long rightoverload;

byte cmode=1;                                                 // 0=Flat battery  1=Charged battery 2=battery needs recharging
byte lmode=1;                                                 // 0=reverse, 1=brake, 2=forward
byte rmode=1;                                                 // 0=reverse, 1=brake, 2=forward
byte lpwm;                                                    // PWM value for left  motor speed / brake
byte rpwm;                                                    // PWM value for right motor speed / brake
int data;
int error;
int servo[7];

//-------------------------------------------------------------- define servos ------------------------------------------------------


Servo Servo0;                                                 // define servos
Servo Servo1;                                                 // define servos
Servo Servo2;                                                 // define servos
Servo Servo3;                                                 // define servos
Servo Servo4;                                                 // define servos
Servo Servo5;                                                 // define servos
Servo Servo6;                                                 // define servos


void setup()
{
  //Serial.begin(115200);
  //------------------------------------------------------------ Initialize I/O pins ------------------------------------------------
  
  //pinMode(Charger,OUTPUT);                                    // change Charger pin to output
  //digitalWrite(Charger,1);                                    // disable current regulator to charge battery
  Wire.begin(4);                                              // set controller as I2C slave #1
  Wire.onReceive(Control);                                    // Data from Master should be motor speeds
  Wire.onRequest(Sensors);                                    // Send sensor readings on request
  
  
  //------------------------------------------------------------ Initialize Servos ----------------------------------------------------

  Servo0.attach(S0);                                          // attach servo to I/O pin
  Servo1.attach(S1);                                          // attach servo to I/O pin
  Servo2.attach(S2);                                          // attach servo to I/O pin
  Servo3.attach(S3);                                          // attach servo to I/O pin
  Servo4.attach(S4);                                          // attach servo to I/O pin
  Servo5.attach(S5);                                          // attach servo to I/O pin
  Servo6.attach(S6);                                          // attach servo to I/O pin

  //------------------------------------------------------------ Set servos to default position ---------------------------------------

  Servo0.writeMicroseconds(DServo0);                          // set servo to default position
  Servo1.writeMicroseconds(DServo1);                          // set servo to default position
  Servo2.writeMicroseconds(DServo2);                          // set servo to default position
  Servo3.writeMicroseconds(DServo3);                          // set servo to default position
  Servo4.writeMicroseconds(DServo4);                          // set servo to default position
  Servo5.writeMicroseconds(DServo5);                          // set servo to default position
  Servo6.writeMicroseconds(DServo6);                          // set servo to default position

}


void loop()
{
  if(millis()-stime>200)
  {
    if(lpwm>0) lpwm--;
    if(lpwm<0) lpwm++;
    if(rpwm>0) rpwm--;
    if(rpwm<0) rpwm++;
    Hbridge();
    delay(2);
  }
  
  //------------------------------------------------------------ Check battery voltage and current draw of motors ---------------------

  volts=analogRead(Battery);                                  // read the battery voltage
  lamps=analogRead(LmotorC);                                  // read left motor current draw
  ramps=analogRead(RmotorC);                                  // read right motor current draw
  
  if(volts<lowvolt && cmode==1) cmode=2;                      // if battery voltage falls below nominal then battery needs charging

  if (lamps>lmaxamps)                                         // is left motor current exceeding safe limit
  {
    analogWrite (LmotorA,0);                                  // turn off motors
    analogWrite (LmotorB,0);                                  // turn off motors
    leftoverload=millis();                                    // record time of overload
  }

  if (ramps>rmaxamps)                                         // is right motor current exceeding safe limit
  {
    analogWrite (RmotorA,0);                                  // turn off motors
    analogWrite (RmotorB,0);                                  // turn off motors
    rightoverload=millis();                                   // record time of overload
  }
}
