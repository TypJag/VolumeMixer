/////////////////////////////////////
////Pins
/////////////////////////////////////
//Digital input pins used D11, D7, D4
#include <Bounce2.h>

Bounce button0 = Bounce();
Bounce button1 = Bounce();  
Bounce button2 = Bounce();

const float potPin[4] = {3, 1, 5, 4}; //Analog input pins 
float potValue[4];
float oldPotValue[4];
float sentPotValue[4];
float doubleSentPotValue[4];

/////////////////////////////////////
////Setup
/////////////////////////////////////

void setup() {
  pinMode(A4, INPUT);
  //pinMode(D11, INPUT_PULLUP);
  //pinMode(D7, INPUT_PULLUP);
  //pinMode(D4, INPUT_PULLUP);

  button0.attach(11,INPUT_PULLUP);
  button1.attach(7,INPUT_PULLUP);
  button2.attach(4,INPUT_PULLUP);// Attach the debouncer to a pin with INPUT_PULLUP mode
  button0.interval(10); // Use a debounce interval of 25 milliseconds
  button1.interval(10);
  button2.interval(10);
  
  Serial.begin(9600); //Start Serial

  for (int i = 0; i < 4; i++) { //Get pot Value and send
    getPotValue(i);
    send(i);
  }

  oldify(); //Cleanup?
}



/////////////////////////////////////
////Loop
/////////////////////////////////////

void loop() {
  button0.update();
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
  
  for (int i = 0; i < 4; i++) {
    getPotValue(i);
  } // Gets values for all pots

  for (int i = 0; i < 4; i++) {
    //Checks to make sure pot values are valid
    //Eg not same as old, not 1, not 0
    if (potValue[i] != oldPotValue[i])  { //Compare old to new
      if (potValue[i] != doubleSentPotValue[i] || potValue[i] == 0 || potValue[i] == 1){ 
        if (potValue[i] != sentPotValue[i]) {
          send(i);
        }
      }
    }
  }
  oldify();
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


void send(int l) {
  Serial.print(l);
  Serial.print(" ");
  Serial.println(potValue[l]);
  doubleSentPotValue[l] = sentPotValue[l];
  sentPotValue[l] = potValue[l];
};

void sendButton(int l) {
  Serial.print("4 ");
  Serial.println(l);
};


void oldify() {
  for (size_t i = 0; i < 4; i++) {
    oldPotValue[i] = potValue[i];
  }
};
