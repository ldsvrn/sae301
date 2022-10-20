#include <ESP8266WiFi.h>   // Import ESP8266 WiFi library
#include <PubSubClient.h>  // Import PubSubClient library to initialize MQTT protocol
#include <stdio.h>
#include <stdlib.h>
#include <OneWire.h>            //Librairie du bus OneWire
#include <DallasTemperature.h>  //Librairie du capteur

const int button = D2;  // GPIO 8 for the button
bool ledflag = false;   // LED status flag

// Update these with values suitable for your network.
const char* ssid = "honor 9x";         //use your ssid
const char* password = "wifihonor9x";  //use your password
const char* mqtt_server = "broker.emqx.io";
const char* topic = "testsae301/prises/";

#define ONE_WIRE_BUS D3               // Pin de connexion de la DS18B20
float valTemp = 0.0;                  // Variables contenant la valeur de température.
float valTemp_T;                      // Valeurs de relevé temporaires.
#define tempsPause 30                 // Nbre de secondes de pause (3600 = 1H00)
int idxDevice = 31;                   // Index du Device à actionner
OneWire oneWire(ONE_WIRE_BUS);        // Initialisation du Bus One Wire
DallasTemperature sensors(&oneWire);  // Utilistion du bus Onewire pour les capteurs


WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (150)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
// Check for Message received on define topic for MQTT Broker
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  char payloadString[length];
  for (int i = 0; i < length; i++) {
    payloadString[i] = (char)payload[i];
  }
  String paystr(payloadString);
  Serial.println(paystr);

  // Switch on the LED if an 1 was received as first character
  if (paystr == "1") {
    Serial.println("LED ON");
    ledflag = true;
    digitalWrite(D1, HIGH);  // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  }
  if (paystr == "0") {
    Serial.println("LED OFF");
    ledflag = false;
    digitalWrite(D1, LOW);  // Turn the LED off by making the voltage HIGH
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish(topic, "CONNECTE");
      // ... and resubscribe
      client.subscribe(topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  sensors.begin();         // On initialise la bibliothèque Dallas
  pinMode(button, INPUT);  // define button as an input
  pinMode(D1, OUTPUT);     // define LED as an output
  digitalWrite(D1, LOW);   // turn output off just in case
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

float getTemperatureC() {
  // On relévé la température.
  // ------------------------
  sensors.requestTemperatures();         // On demande au capteur de lire la température
  valTemp = sensors.getTempCByIndex(0);  // On stocke la température relevé dans une variable temporaire
  Serial.print("Valeur de température relevée : ");
  Serial.println(valTemp);
  return valTemp;  
  
}

void loop() {
  if (digitalRead(button) == HIGH) {  // if button is pressed
    if (ledflag == false) {           // and the status flag is LOW
      ledflag = true;                 // make status flag HIGH
      digitalWrite(D1, HIGH);         // and turn on the LED
      snprintf (msg, MSG_BUFFER_SIZE, "{'sender': 'prise1', 'message_type': 'reply', 'state': true, 'temp': '%ld'}", getTemperatureC());
      client.publish(topic, msg);
      client.subscribe(topic);
    } else {                  // otherwise...
      ledflag = false;        // make status flag LOW
      digitalWrite(D1, LOW);  // and turn off the LED
      snprintf (msg, MSG_BUFFER_SIZE, "{'sender': 'prise1', 'message_type': 'reply', 'state': false, 'temp': '%ld'}", getTemperatureC());
      client.publish(topic, msg);
      client.subscribe(topic);
    }
    delay(500);  // wait a sec for the hardware to stabilize
  }
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
// RELEVE DE TEMPERATURE.


unsigned long now = millis();
/*if (now - lastMsg > 8000) {
    lastMsg = now;
    ++value;
    snprintf (msg, MSG_BUFFER_SIZE, "hello world #%ld", value);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish(topic, msg);
  }*/