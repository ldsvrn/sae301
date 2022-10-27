#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time as t
import json
from datetime import time, datetime
from dotenv import load_dotenv
import os
import smtplib, ssl
from email.message import EmailMessage
from pushbullet import Pushbullet

load_dotenv()

# ce qui me terrifie c'est que cette horreur fonctionne
# c'est la merde psk je peux pas récupérer les schedule_get dans le django
# aussi c'étais  
class MQTTNotification:
    def __init__(self, topic: str, threshold: int, email: str, password: str):
        self.client = mqtt.Client(client_id="notification")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.topic = topic
        self.threshold = threshold
        self.email = email
        self.__password = password
        self.client.connect("mqtt.louis.systems", 1883, 60)
        self.client.loop_start()
        self.send_mail = True
        self.pb = Pushbullet(os.getenv("PUSHBULLET_API"))
        self.temp = {
            "prise": "",
            "temp": 0
        }
        t.sleep(2)
        while True:
            print("sending requests")
            for i in ["prise1", "prise2"]:
                self.client.publish(self.topic, str(json.dumps(
                {
                    "sender": "notification",
                    "message_type": "request",
                    "request_for": i
                })))
                t.sleep(5)
                if float(self.temp["temp"]) > self.threshold:
                    if self.send_mail:
                        context = ssl.create_default_context()
                        port = 587 
                        smtp_server = "smtp.office365.com"
                        sender_email = "botmqtt.sae301@hotmail.com"  # Enter your address
                        print("envoi mail")
                        with smtplib.SMTP("smtp.office365.com", port) as server:
                            server.ehlo()  # Can be omitted
                            server.starttls(context=context)  # Secure the connection
                            server.ehlo()  # Can be omitted
                            server.login(sender_email, self.__password)
                            msg = EmailMessage()
                            msg["from"] = sender_email
                            msg["to"] = self.email
                            msg["subject"] = f"La température de {self.temp['prise']} a dépassé les {self.threshold}°C!!!!"
                            msg.set_content(f"ATTENTION LA TEMPÉRATURE DE LA PRISE EST DE {self.temp['temp']}°C!!!!")

                            print(f"envoi mail à {self.email}, de {sender_email} (text: {msg})")
                            #server.send_message(msg)
                            push = self.pb.push_note("Alerte température", f"{self.temp['prise']} {self.temp['temp']}°C!!!!")
                            device = self.pb.devices[0]
                            push2 = self.pb.push_sms(device, os.getenv("NUM"), f"{self.temp['prise']} {self.temp['temp']}°C!!!!")
                            self.send_mail = False
                    else:
                        print("mail déjà envoyé")
                else:
                    self.send_mail = True
            t.sleep(55)


    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)
        print("Connected with result code "+str(rc))


    def on_message(self, client, userdata, msg):
        try:
            message = json.loads(msg.payload.decode("utf-8"))
        except Exception:
            return
        
        try:
            message_type = message["message_type"]
        except KeyError:
            return
        
        # match go brrrrrr
        match message_type:
            case "reply":
                self.temp = {
                    "prise": message["sender"],
                    "temp": message["temp"]
                }


            
schedule = MQTTNotification("prises", 10, "louis2555@orange.fr", str(os.getenv("EMAIL_PASSWORD")))