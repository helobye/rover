
void Charge()
{
  if(volts>peakvolt) 
  {
    ctime=millis();                                           // reset safety timer if voltage increases
    peakvolt=volts;                                           // update peak volt with new highest battery voltage
  }
  
  if(millis()-ctime>safetime || volts<peakvolt-4)
  {
    cmode=0;                                                  // charge cycle complete 
    peakvolt=0;                                               // reset peakvolt
  } 
}
