// --------------------------------------------------------- Code to drive dual "H" bridges --------------------------------------
void Hbridge()
{
  if ((millis()-leftoverload)>overloadtime)             
  {
    switch (lmode)                                     // if left motor has not overloaded recently
    {
    case 2:                                               // left motor forward
      analogWrite(LmotorA,0);
      analogWrite(LmotorB,lpwm);
      break;

    case 1:                                               // left motor brake
      analogWrite(LmotorA,lpwm);
      analogWrite(LmotorB,lpwm);
      break;

    case 0:                                               // left motor reverse
      analogWrite(LmotorA,lpwm);
      analogWrite(LmotorB,0);
      break;
    }
  }

  if ((millis()-rightoverload)>overloadtime)
  {
    switch (rmode)                                    // if right motor has not overloaded recently
    {
    case 2:                                               // right motor forward
      analogWrite(RmotorA,0);
      analogWrite(RmotorB,rpwm);
      break;

    case 1:                                               // right motor brake
      analogWrite(RmotorA,rpwm);
      analogWrite(RmotorB,rpwm);
      break;

    case 0:                                               // right motor reverse
      analogWrite(RmotorA,rpwm);
      analogWrite(RmotorB,0);
      break;
    }
  } 
}

