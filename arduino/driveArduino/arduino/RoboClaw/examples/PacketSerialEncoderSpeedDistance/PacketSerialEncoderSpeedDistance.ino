//Arduino Mega and Leonardo chips only support some pins for receiving data back from the RoboClaw
//This is because only some pins of these boards support PCINT interrupts or are UART receivers.
//Mega: 0,10,11,12,13,14,15,17,19,50,51,52,53,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15
//Leonardo: 0,8,9,10,11

//Arduino Due currently does not support SoftwareSerial. Only hardware uarts can be used, pins 0/1, 14/15, 16/17 or 18/19.

//Includes required to use Roboclaw library
#include "BMSerial.h"
#include "RoboClaw.h"

//Roboclaw Address
#define address 0x80

//Velocity PID coefficients
#define Kp 1.0
#define Ki 0.5
#define Kd 0.25
#define qpps 44000

//Definte terminal for display. Use hardware serial pins 0 and 1
BMSerial terminal(0,1);

//Setup communcaitions with roboclaw. Use pins 10 and 11 with 10ms timeout
RoboClaw roboclaw(10,11,10000);

void setup() {
  //Open terminal and roboclaw serial ports
  terminal.begin(57600);
  roboclaw.begin(38400);
  
  //Set PID Coefficients
  roboclaw.SetM1VelocityPID(address,Kd,Kp,Ki,qpps);
  roboclaw.SetM2VelocityPID(address,Kd,Kp,Ki,qpps);  
}

void displayspeed(void)
{
  uint8_t status1,status2,status3,status4;
  bool valid1,valid2,valid3,valid4;
  
  uint32_t enc1 = roboclaw.ReadEncM1(address, &status1, &valid1);
  uint32_t enc2 = roboclaw.ReadEncM2(address, &status2, &valid2);
  uint32_t speed1 = roboclaw.ReadSpeedM1(address, &status3, &valid3);
  uint32_t speed2 = roboclaw.ReadSpeedM2(address, &status4, &valid4);

  if(valid1){
    terminal.print("Encoder1:");
    terminal.print(enc1,DEC);
    terminal.print(" ");
    terminal.print(status1,HEX);
    terminal.print(" ");
  }
  if(valid2){
    terminal.print("Encoder2:");
    terminal.print(enc2,DEC);
    terminal.print(" ");
    terminal.print(status2,HEX);
    terminal.print(" ");
  }
  if(valid3){
    terminal.print("Speed1:");
    terminal.print(speed1,DEC);
    terminal.print(" ");
  }
  if(valid4){
    terminal.print("Speed2:");
    terminal.print(speed2,DEC);
    terminal.print(" ");
  }
  terminal.println();
}

void loop() {
  uint8_t depth1,depth2;

  roboclaw.SpeedDistanceM1(address,12000,48000);
  do{
    displayspeed();
    roboclaw.ReadBuffers(address,depth1,depth2);
  }while(depth1);	//Loop until distance command has completed

  roboclaw.SpeedDistanceM1(address,-12000,48000);
  do{
    displayspeed();
    roboclaw.ReadBuffers(address,depth1,depth2);
  }while(depth1);	//Loop until distance command has completed
  
}
