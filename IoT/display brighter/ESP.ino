#include <ESP8266WiFi.h>
#include <stdlib.h>

const int espPin = 14;
const int RPiPin = 12;
const int sigPin = 13;
const int detPin = A0;

const char* ssid = "AndroidECE";
const char* password = "ece433_221"; 
const char* host = "192.168.43.193"; // IP address of the RPi

unsigned int tcpPort = 4120;

void setup() {
  Serial.begin(115200);
  pinMode(espPin, OUTPUT);
  pinMode(RPiPin, OUTPUT);
  pinMode(sigPin, OUTPUT);
  pinMode(detPin, INPUT);

  Serial.printf("Connecting to %s ", ssid); // connect to mobile hotspot; doing this on the phone!
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println(" connected");
}
 
void loop() {
  int currValue;
  String sendReading;
  int count = 0;
  WiFiClient client;

  for (int i = 0; i < 10; i++) { // 2 seconds, 10 blinks
    digitalWrite(sigPin, HIGH);
    delay(100);
    digitalWrite(sigPin, LOW);
    delay(100);
  }
  
  Serial.printf("\n Connecting to %s ...", host);
  
  if (client.connect(host, tcpPort)) { // connect to RPi
    Serial.println("connected. Signal LED will now stay on. Sending after 2 seconds.");
    
    digitalWrite(sigPin, HIGH);
    delay(2000); // 2 second wait

    if (client.connected()) {
      
      while(!client.available()) {
        if (client.available()) {
          String perms = client.readStringUntil('\n');
          Serial.println(perms);
          break;
        }
      }
      
      // 120 seconds, so 152 values will be sent in total due to delay in TCP connection/
      for (int i = 0; i < 152; i++) {
        currValue = analogRead(detPin); 
        sendReading = String(currValue);
        client.print(sendReading); // send the reading from sensor to RPi
        Serial.print("Sent sensor value #"); 
        Serial.print(i);
        Serial.print(" to RPi: ");
        Serial.println(currValue);
        delay(250);
        count++;

        if (client.available() && (count % 8 == 0))
        {
          String line = client.readStringUntil('\n'); // if it says "RPi" then turn on RPi LED, else turn on ESP LED
          Serial.println(line);
    
          if (line.equals("RPi")) { // turn on RPi LED
            digitalWrite(RPiPin, HIGH);
            digitalWrite(espPin, LOW);  
          }
    
          else { // turn on ESP LED
            digitalWrite(RPiPin, LOW);
            digitalWrite(espPin, HIGH);
          }
        }
      }
    }

    client.print("");
    client.stop();
    Serial.println("\n[Disconnected]. 2 minutes have elapsed.");
    digitalWrite(sigPin, LOW);
    digitalWrite(RPiPin, LOW);
    digitalWrite(espPin, LOW);
  }

  else {
    Serial.println("connection failed!");
    client.stop();
  }

  delay(10000);
}
