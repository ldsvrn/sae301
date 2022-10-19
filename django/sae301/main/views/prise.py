from re import A
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from ..mqtt import MQTTClient

global mqtt

mqtt = MQTTClient("broker.emqx.io", 1883, "testsae301/prises/")

def main(request):
    data = mqtt.last_message
    prise1 = mqtt.request_wait("prise1", 1)
    prise2 = mqtt.request_wait("prise2", 1)
    return render(request, 'main.html', {
        "prise1": {"state": prise1["state"], "temp": prise1["temp"]},
        "prise2": {"state": prise2["state"], "temp": prise2["temp"]}
        })

def set(request, prise: str, onoff: str):
    if onoff == "on":
        mqtt.publish_set(prise, True)
    elif onoff == "off":
        mqtt.publish_set(prise, False)

    return redirect('/')

def request(request, prise: str):
    mqtt.request_wait(prise)
    return redirect('/')