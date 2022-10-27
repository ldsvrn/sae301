#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time as t
import json
from datetime import time, datetime

# ce qui me terrifie c'est que cette horreur fonctionne
# c'est la merde psk je peux pas récupérer les schedule_get dans le django
# aussi c'étais  
class MQTTScheduler:
    def __init__(self, topic: str):
        self.client = mqtt.Client(client_id="scheduler")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.topic = topic
        self.client.connect("mqtt.louis.systems", 1883, 60)
        self.client.loop_start()
        # honnetement je sais pas comment faire autrement que d'utiliser 2 dictionnaires
        # c'est pas vraiment optimal, mais ça marche
        self.schedule_prise1 = {}
        self.schedule_prise2 = {}
        while True:
            now = datetime.now()
            now = time(now.hour, now.minute)
            # alors la yolo
            if self.schedule_prise1 != {}:
                if time.fromisoformat(self.schedule_prise1["start"]) <= now < time.fromisoformat(self.schedule_prise1["end"]):
                    self.client.publish("prises", json.dumps(
                        {
                            "sender": "scheduler",
                            "message_type": "set",
                            "prise": "prise1",
                            "state": True
                        }))
                    print("prise1 on")
                else: # si le dictionnaire est vide, on envoie un message pour faire l'inverse de l'état actuel
                    self.client.publish("prises", json.dumps(
                        {
                            "sender": "scheduler",
                            "message_type": "set",
                            "prise": "prise1",
                            "state": False
                        }))
                    print("prise1 off")
            if self.schedule_prise2 != {}:
                if time.fromisoformat(self.schedule_prise2["start"]) <= now < time.fromisoformat(self.schedule_prise2["end"]):
                    self.client.publish("prises", json.dumps(
                        {
                            "sender": "scheduler",
                            "message_type": "set",
                            "prise": "prise2",
                            "state": True
                        }))
                    print("prise2 on")
                else:
                    self.client.publish("prises", json.dumps(
                        {
                            "sender": "scheduler",
                            "message_type": "set",
                            "prise": "prise2",
                            "state": False
                        }))
                    print("prise2 off")
            t.sleep(10)


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
            case "schedule":
                match message["prise"]:
                    case "prise1":
                        self.schedule_prise1 = message
                        print(self.schedule_prise1)
                    case "prise2":
                        self.schedule_prise2 = message
                        print(self.schedule_prise2)
            case "schedule_reset":
                match message["prise"]:
                    case "prise1":
                        self.schedule_prise1 = {}
                    case "prise2":
                        self.schedule_prise2 = {}
                    case "all":
                        self.schedule_prise1 = {}
                        self.schedule_prise2 = {}
            # techniquement ça marche mais pas le temps de l'implémenter
            case "schedule_request":
                client.publish(self.topic, json.dumps(
                {
                    "sender": "scheduler",
                    "message_type": "schedule_reply",
                    "prise1": self.schedule_prise1,
                    "prise2": self.schedule_prise2
                }))
            

schedule = MQTTScheduler("schedule")