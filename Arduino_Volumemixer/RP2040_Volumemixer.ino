/////////////////////////////////////
////This is a Arduino program used to read values from a few pots,
////the state of a few buttons and send the read information over
////serial to a python script. The python script uses the read
////information to change volume of programs runing on the
////computer. The buttons is used as media controls.
////Uses bounce2 https://github.com/thomasfredericks/Bounce2
////By Axel Andersson 2020
/////////////////////////////////////

/////////////////////////////////////
////The informations sent over serial if structured as such
////X Y where X is the channel information used to determine which
////programs volume should be changed. Y is in this chase the volume
////in the format 0.5 eg 1 0.5 would be channel 1 at 50% volume
////A special case is if X = 0 it indicates that a button
////has been pressed and Y is now which button.
/////////////////////////////////////

/////////////////////////////////////
////Pins
/////////////////////////////////////
//Digital input pins used GPIO18, GPIO20, GPIO24
#include <Bounce2.h>

Bounce button0 = Bounce();
Bounce button1 = Bounce();
Bounce button2 = Bounce();

const float potPin[4] = {26, 27, 28, 29}; //Analog input pins GPIO26-29
float potValue[4]; //Current potvalues
float oldPotValue[4] = {0,0,0,0}; //Previus potvalues

/////////////////////////////////////
////Setup
/////////////////////////////////////

void setup() {
  pinMode(26, INPUT);
  pinMode(27, INPUT);
  pinMode(28, INPUT);
  pinMode(29, INPUT);
  //pinMode(D11, INPUT_PULLUP);
  //pinMode(D7, INPUT_PULLUP);
  //pinMode(D4, INPUT_PULLUP);

  button0.attach(18,INPUT_PULLUP);
  button1.attach(20,INPUT_PULLUP);
  button2.attach(24,INPUT_PULLUP);// Attach the debouncer to a pin with INPUT_PULLUP mode
  button0.interval(10); // Use a debounce interval of 25 milliseconds
  button1.interval(10);
  button2.interval(10);

  Serial.begin(9600); //Start Serial
}

/////////////////////////////////////
////Loop
/////////////////////////////////////

void loop() {

  updateButtons();

  for (int i = 0; i < 4; i++) {
    getPotValue(i);
    //Checks to make sure pot values are valid
    //Eg not same as old, not 1, not 0
    if (potValue[i] != oldPotValue[i])  { //Compare old to new and new to 1 and 0
       sendPotValue(i);
    }
  } // Gets values for all pots

  delay(60);
}

/////////////////////////////////////
////Functions
/////////////////////////////////////


void getPotValue(int i) {
  static float potValueExp;
//  potValue[i] = (float( constrain(map(analogRead(potPin[i]), 0, 1023, 0, 102), 0, 100))/100);

  //read analog signal and map to value between 0-100
  potValueExp = float(constrain(map(analogRead(potPin[i]), 0, 1023, 102, 0), 0, 100));
  potValue[i] = ((0.01*potValueExp*potValueExp)/100);
};

void updateButtons() {
  button0.update(); //updates the buttons states
  button1.update();
  button2.update();
  if (button0.fell()) {
    sendButton(0);
  }
  if (button1.fell()) {
    sendButton(1);
  }
  if (button2.fell()) {
    sendButton(2);
  }
};

void sendPotValue(int l) { //Sends potValues over serial to python script
  Serial.print(l+1);
  Serial.print(" ");
  Serial.println(potValue[l]);
  oldPotValue[l] = potValue[l];
};

void sendButton(int l) {
  Serial.print("0 ");
  Serial.println(l);
};
