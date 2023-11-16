#include <WiFi.h>
#include <WiFiUdp.h>
WiFiUDP udp;

char packetBuffer[255];
unsigned int localPort = 9999;
char *serverip = "192.168.1.37";
unsigned int serverport = 1069;

const char *ssid = "bigdickraspberry";
const char *password = "12345678";

// Joystick variables
int D35;
int D34;
int identifier;
int identifier2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(34, INPUT);
  pinMode(35, INPUT);
 	// Connect to Wifi network.
 	WiFi.begin(ssid, password);
 	while (WiFi.status() != WL_CONNECTED) {
    // pinMode(22, INPUT_PULLDOWN);
 		delay(500); Serial.print(F("."));
 	}
 	udp.begin(localPort);
 	Serial.printf("UDP Client : %s:%i \n", WiFi.localIP().toString().c_str(), localPort);
}


void loop() {
  // put your main code here, to run repeatedly:
  // Read joystick inputs and apply deadzone
    readJoystick();

    // Send joystick data to server
    sendJoystickData();

    // Check for receiving packets
    receivePackets();

    // Small delay to prevent spamming
    delay(90);
}
void readJoystick() {
    // Read the analog values and apply deadzone
    if (analogRead(34)>2048){
    D34 = 2*abs((analogRead(34)/40.96)-50);
    identifier = 1; //positive
  }
  else{
    D34 = 2*abs((analogRead(34)/40.96)-50);
    identifier = 2; //negative
  }
  if (analogRead(35)>2048){
    D35 = 2*abs((analogRead(35)/40.96)-50);
    identifier2 = 1; //positive
  }
  else{
    D35 = 2*abs((analogRead(35)/40.96)-50);
    identifier2 = 2; //negative
  }

  if(D34<=10){
    D34 = 0;
  }
  if(D35<=10){
    D35 = 0;
  }
    Serial.print("Reading from D34: ");  // Print label for D34 reading
  Serial.println(D34);         // Print value from D34 and move to a new line
  Serial.print("D34 Identifier");  // Print label for D34 reading
  Serial.println(identifier);         // Print value from D34 and move to a new line

  Serial.print("Reading from D35: ");  // Print label for D35 reading
  Serial.println(D35);         // Print value from D35 and move to a new line
  Serial.print("D35 Identifier");  // Print label for D34 reading
  Serial.println(identifier2);         // Print value from D34 and move to a new line

  delay(90);  // Wait for 1 second before taking the next set of readings
}

void sendJoystickData() {
    char message[100];
    sprintf(message, "[%d, %d, %d, %d]", D35, D34, identifier, identifier2);

    udp.beginPacket(serverip, serverport);
    udp.write((unsigned char *)message, strlen(message));
    udp.endPacket();
}

void receivePackets() {
    char packetBuffer[255];
    int packetSize = udp.parsePacket();
    if (packetSize) {
        Serial.print("Received packet from : ");
        Serial.println(udp.remoteIP());
        int len = udp.read(packetBuffer, 255);
        if (len > 0) {
            packetBuffer[len] = 0;
        }
        Serial.printf("Data: %s\n", packetBuffer);
    }
}
