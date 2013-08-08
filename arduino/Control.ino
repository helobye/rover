void Control(int data)
{  
  stime=millis();
  if((data!=7) && (data!=1))                                             // Invalid data - stop all motors
  {
    lmode=0;
    rmode=0;
    lpwm=0;
    rpwm=0;
    while(Wire.available()>0)
    {
      byte err=Wire.read();                               // clear bad data from buffer
    }
    error++;                                              // record error
  }
  else
  {
    cmode=Wire.read();
    lmode=Wire.read();
    rmode=Wire.read();
    lpwm=Wire.read();
    rpwm=Wire.read();
    Servo0.writeMicroseconds(Wire.read()*10);
    Servo1.writeMicroseconds(Wire.read()*10);
  }
  /*
  Serial.println(cmode);
  Serial.println(lmode);
  Serial.println(rmode);
  Serial.println(lpwm);
  Serial.println(rpwm);
  */
  Hbridge();
}
