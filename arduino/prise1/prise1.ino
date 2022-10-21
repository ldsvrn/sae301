#include <ESP8266WiFi.h>     // Import ESP8266 WiFi library
#include <PubSubClient.h>    // Import PubSubClient library to initialize MQTT protocol
#include <stdio.h>
#include <stdlib.h>
#include <OneWire.h>                        //Librairie du bus OneWire
#include <DallasTemperature.h>    //Librairie du capteur
#include <ArduinoJson.h>

const int button = D2;    // GPIO 8 for the button
bool ledflag = false;     // LED status flag

// Update these with values suitable for your network.
const char* ssid = "honor 9x";                 //use your ssid
const char* password = "wifihonor9x";    //use your password
const char* mqtt_server = "mqtt.louis.systems";
const char* topic = "prises";

#define ONE_WIRE_BUS D3                            // Pin de connexion de la DS18B20
float valTemp = 0.0;                                    // Variables contenant la valeur de température.
float valTemp_T;                                // Valeurs de relevé temporaires.
#define tempsPause 30                           // Nbre de secondes de pause (3600 = 1H00)
int idxDevice = 31;                             // Index du Device à actionner
OneWire oneWire(ONE_WIRE_BUS);                  // Initialisation du Bus One Wire
DallasTemperature sensors(&oneWire);            // Utilistion du bus Onewire pour les capteurs


WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (150)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void sendReply();
float getTemperatureC();

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

DynamicJsonDocument doc(1024);
// Check for Message received on define topic for MQTT Broker
void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    
    deserializeJson(doc, payload);

    const char* message_type = doc["message_type"];
    if (strcmp(message_type,"request") == 0 ) {
        if (doc["request_for"] == "prise1"){
            sendReply();
        }
    }

    if (strcmp(message_type,"set") == 0 ) {
        if (doc["prise"] == "prise1" || doc["prise"] == "all"){
            bool state = doc["state"];
            ledflag = state;
            Serial.println(state);
        }
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
            //client.publish(topic, "CONNECTE");
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
    sensors.begin();                 // On initialise la bibliothèque Dallas
    pinMode(button, INPUT);    // define button as an input
    pinMode(D1, OUTPUT);         // define LED as an output
    digitalWrite(D1, LOW);     // turn output off just in case
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
}

float getTemperatureC() {
    sensors.requestTemperatures();
    return sensors.getTempCByIndex(0);
}

void sendReply() {
    if (ledflag) {
        sprintf(msg, "{\"sender\": \"prise1\", \"message_type\": \"reply\", \"state\": true, \"temp\": \"%f\"}", getTemperatureC());
    } else {
        sprintf(msg, "{\"sender\": \"prise1\", \"message_type\": \"reply\", \"state\": false, \"temp\": \"%f\"}", getTemperatureC());
    }
    client.publish(topic, msg);
    //client.subscribe(topic);
}

void loop() {
    if (digitalRead(button) == HIGH) {    // if button is pressed
        ledflag = !ledflag;
        sendReply();
        delay(500);
    }
    
    if (ledflag) {
        digitalWrite(D1, HIGH);
    } else {
        digitalWrite(D1, LOW);
    }

    if (!client.connected()) {
        reconnect();
    }
    client.loop();
}