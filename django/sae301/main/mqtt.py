from email import message
import paho.mqtt.client as mqtt
import random
import json
import datetime

class MQTTClient:
    def __init__(self, brocker, port, topic) -> None:
        self.brocker = brocker
        self.port = port
        self.topic = topic
        self.clientid = "sae301-" + str(random.randint(0, 1000))
        self.client = mqtt.Client(client_id=f"client-{self.clientid}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.brocker, self.port, 60)
        self.placeholder={ # permet eventuellement de savoir si la prise n'a pas répondu"
                "sender": "placeholder",
                "message_type": "placeholder",
                "prise": "placeholder",
                "state": "placeholder",
                "temp": "placeholder",
                "timestamp": datetime.datetime.fromtimestamp(0)
            }

        self.__last_message = self.placeholder
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg):
        try:
            message = json.loads(msg.payload.decode("utf-8"))
        except Exception:
            message = self.placeholder # pour éviter une erreur si le premier payload n'est pas un json
        
        # On récupère uniquement les reply, on rajoute un timestamp
        # recréation d'un dico parceque il voulait pas modifier message
        # on ignore les erreurs, elles ne sont pas importantes ici
        try:
            if message["message_type"] == "reply":
                self.__last_message = {
                    "sender": message["sender"],
                    "message_type": message["message_type"], # = reply
                    "state": message["state"],
                    "temp": message["temp"],
                    "timestamp": datetime.datetime.now()
                }
        except Exception:
            pass
        
    # a changer si la librarie arduino ne peux pas listen sur le topic et répondre quand il faut
    def publish_request(self, request_for):
        self.client.publish(self.topic, str(json.dumps(
            {
                "sender": self.clientid,
                "message_type": "request",
                "request_for": request_for
            })))
    
    def publish_set(self, prise: str, state: bool):
        self.client.publish(self.topic, str(json.dumps(
            {
                "sender": self.clientid,
                "message_type": "set",
                "prise": prise,
                "state": state
            })))

    def request_wait(self, prise: str, timeout: int = 5):
        self.publish_request(prise)
        start = datetime.datetime.now()
        # code dégueu permettant d'attendre la réponse de la prise pendant x secondes (timeout)
        # ignore les messages qui sont vieux de 5 secondes
        while self.__last_message["sender"] != prise or datetime.datetime.now() - self.__last_message["timestamp"] > datetime.timedelta(seconds=5):
            if datetime.datetime.now() - start > datetime.timedelta(seconds=timeout):
                return self.placeholder
                
        return self.__last_message

    def set_schedule(self, prise: str, state: bool, start: datetime.datetime, end: datetime.datetime):
        pass

    def close(self):
        self.client.loop_stop()

    @property
    def last_message(self):
        return self.__last_message