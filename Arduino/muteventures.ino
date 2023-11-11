// include the library for LCD
#include <LiquidCrystal.h>

// LCD pins <--> Arduino pins
const int RS = 11, EN = 12, D4 = 2, D5 = 3, D6 = 4, D7 = 5;

// declare a LiquidCrystal object with the pin numbers
LiquidCrystal lcd (RS, EN, D4, D5, D6, D7);

// include the library for network
#include <Ethernet.h> // or <WiFi.h> if you are using WiFi

// declare a client object to connect to the server
EthernetClient client; // or WiFiClient client; if you are using WiFi

// the IP address and port of the server
byte server[] = {192, 168, 1, 100}; // or use a domain name, such as "example.com"
int port = 80;

void setup() {
  // set up the LCD's number of columns and rows
  lcd.begin(16, 2);

  // set up the network connection
  Ethernet.begin(mac, ip); // or WiFi.begin(ssid, pass); if you are using WiFi
}

void loop() {
  // connect to the server
  if (client.connect(server, port)) {
    // send a request to get the output text
    client.println("GET /output.txt HTTP/1.1");
    client.println("Host: 192.168.1.100"); // or use a domain name, such as "Host: example.com"
    client.println("Connection: close");
    client.println();
  }

  // read the response from the server
  while (client.available()) {
    // read a character from the server
    char c = client.read();

    // print the character to the LCD
    lcd.write(c);
  }

  // close the connection
  client.stop();
}
