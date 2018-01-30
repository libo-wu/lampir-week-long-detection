/*
Lavet based Chopped PIR sensor Arduino nano control code

By Libo Wu
Jan 2018
 */


#include <SoftwareSerial.h>
//#include "Filter.h"

/*-----( Declare Constants, Pin Numbers )-----*/ 
#define volNum        400   // the number of the array 
#define gain          1
#define led           2
//ExponentialFilter<long> FilteredTemperature(20, 0);  //Filter is used. ExponentialFilter(weight, current)
                                                     //w=20 is weight 20/100=0.2; Initial=0; current=w*new+(1-w)*current;
                                                     

SoftwareSerial BTserial(0,1); //set Bluetooth Rx=0,Tx=1

int Nsample=512;
int analogPin = A0;
int voltage=0;
int count=0;


/*---------lavet pulse and lavet_delay is to control the rotating speed
            lavet_delay should not be too small, will cause jitterring
            -----------*/
int pinA=11;
int pinB=12;
int lavet_pulse=50;
int lavet_delay=250;

int biaVolt = 540;   // bias voltage of the ADC of Arduino
int OccuVolDiff = 160*gain;     //  threshold voltage for occupant presence
int vol[volNum];
int volRead_index=0;
int PeakNum=0;
int peak2peak=0;
int IntrptNum=0;
long RawTemperature=biaVolt;
int MaxVol=biaVolt;
int MinVol=biaVolt;
int Max_index=0;
int Min_index=0;
byte OccuState=0x00; 


void setup()   /*----( SETUP: RUNS ONCE )----*/
{
   BTserial.begin(38400);
   pinMode(analogPin, INPUT);
   pinMode(pinA, OUTPUT);
   pinMode(pinB, OUTPUT);
   pinMode(led, OUTPUT);     //led setup
   delay(1000);

   //set timer2 for interrupt
    cli(); // stop interrupts
    TCCR2A = 0; // set entire TCCR2A register to 0
    TCCR2B = 0; // same for TCCR2B
    TCNT2  = 0; // initialize counter value to 0
    // set compare match register for 500 Hz increments
    OCR2A = 249; // f_oc2A=f_io/(2*N*(1+OCR2A))= 16000000 /(2*64*250)=500
    // turn on CTC mode
    TCCR2B |= (1 << WGM21);
    // Set CS22, CS21 and CS20 bits for 64 prescaler
    TCCR2B |= (1 << CS22) | (0 << CS21) | (0 << CS20);
    // enable timer compare interrupt
    TIMSK2 |= (1 << OCIE2A);
    sei(); // allow interrupts

    for (int i = 0; i < volNum - 1; i++)
    {
      vol[i] = biaVolt;
    }
}/*--(end setup )---*/

void loop()   
{
  /*----Lavet rotate---*/
  backwards();
  delay(lavet_pulse);
  halt();
  delay(lavet_delay);
  
  forwards();
  delay(lavet_pulse);
  halt();
  delay(lavet_delay);

}/* --(end main loop )-- */


ISR(TIMER2_COMPA_vect){   //update led status every n*1*volNum (ms)
   IntrptNum++;
   if(IntrptNum>=3){   //execute following code every (n+1)*1ms.
    IntrptNum=0;
    if(volRead_index<volNum-1){
       RawTemperature=analogRead(analogPin);
       //FilteredTemperature.Filter(RawTemperature);
       //vol[volRead_index]=(int)FilteredTemperature.Current();
       vol[volRead_index]=RawTemperature;
       
       BTserial.print(vol[volRead_index]);    //transmission
       BTserial.print("\n");
       
       if(vol[volRead_index]<MinVol){
        MinVol=vol[volRead_index];
        Min_index=volRead_index;
       }
       if(vol[volRead_index]>MaxVol){
        MaxVol=vol[volRead_index];
        Max_index=volRead_index;
       }
       volRead_index++;
    }
    else{
      volRead_index=0;
      peak2peak=MaxVol-MinVol;
//      BTserial.print(peak2peak);
//      BTserial.print("\t");
//      BTserial.print(Max_index-Min_index);
//      BTserial.print("\n");
    if(peak2peak>=OccuVolDiff){
      bitWrite(OccuState, 0,1);
      OccuState=OccuState<<2;   //if larger than threshold, then write OccuInfo[8] to 1   
    }
    else{
      bitWrite(OccuState, 0,0);
      OccuState=OccuState<<2;   //if larger than threshold, then write OccuInfo[8] to 1
      
//    OccuState=OccuState<<2;   //if larger than threshold, then write OccuInfo[8] to 1
//      bitWrite(OccuState, 0,0);
    }
    
    //printBits(OccuState);
    
    if(OccuState>=0x04){
      digitalWrite(led, HIGH);
    }
    else{
      digitalWrite(led, LOW);
    }
      MinVol=biaVolt;
      MaxVol=biaVolt;
    }
    
   }
}

void printBits(byte myByte){
 for(byte mask = 0x80; mask; mask >>= 1){
   if(mask  & myByte)
       BTserial.print('1');
   else
       BTserial.print('0');
 }
 BTserial.print('\n');
}

void halt() {
  digitalWrite(pinA, LOW);   
  digitalWrite(pinB, LOW);   
  //digitalWrite(LED_BUILTIN, LOW);
}

void forwards() {
  digitalWrite(pinA, HIGH);   
  digitalWrite(pinB, LOW);   
  //digitalWrite(LED_BUILTIN, HIGH);
}

void backwards() {
  digitalWrite(pinA, LOW);   
  digitalWrite(pinB, HIGH);   
  //digitalWrite(LED_BUILTIN, HIGH);
}

