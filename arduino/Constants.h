//=================================== BATTERY CHARGER SETTINGS ======================================================================

#define batvolt            487     // This is the nominal battery voltage reading. Peak charge can only occur above this voltage.
#define lowvolt            410     // If the battery voltage falls to this level then recharging is required
//#define safetime        600000     // If the battery voltage does not change in this number of milliseconds then stop charging.



//=================================== H BRIDGE SETTINGS =============================================================================

#define lmaxamps           800     // set overload current for left motor 
#define rmaxamps           800     // set overload current for right motor 
#define overloadtime       100     // time in mS before motor is re-enabled after overload occurs



//=================================== SERVO SETTINGS ================================================================================
// DServo0 = L/R. 1500uS = Center. 2200uS = Furthest Left. 700uS = Furthest Right.
// DServo1 = Front/Back. 2200uS = Forward. 700uS = Backward.


#define DServo0           1450     // default position for servo0 on "power up" - 1500uS is center position on most servos
#define DServo1           1100     // default position for servo1 on "power up" - 1500uS is center position on most servos
#define DServo2           1500     // default position for servo2 on "power up" - 1500uS is center position on most servos
#define DServo3           1500     // default position for servo3 on "power up" - 1500uS is center position on most servos
#define DServo4           1500     // default position for servo4 on "power up" - 1500uS is center position on most servos
#define DServo5           1500     // default position for servo5 on "power up" - 1500uS is center position on most servos
#define DServo6           1500     // default position for servo6 on "power up" - 1500uS is center position on most servos



