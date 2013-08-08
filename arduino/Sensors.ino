void Sensors()
{
  //Servo0.writeMicroseconds(random(7-8)*100);
  //Wire.write(1);
  /*Wire.write(error);                            // report number of transmission errors
  Wire.write(cmode);                            // report battery status: 0=Charging  1=Good  2=Requires charging
  Wire.write(byte(volts/4));                    // 8 most significant bits of battery voltage
  Wire.write(byte(lamps/4));                    // 8 most significant bits of left motor amps
  Wire.write(byte(ramps/4));                    // 8 most significant bits of right motor amps
  ++index;
  if (index >= 5) {
    index = 0;
  }
  */
  uint8_t buffer[5];
  buffer[0] = error;
  buffer[1] = cmode;
  buffer[2] = byte(volts/4);
  buffer[3] = byte(lamps/4);
  buffer[4] = byte(ramps/4);
  Wire.write(buffer, 5);
}
