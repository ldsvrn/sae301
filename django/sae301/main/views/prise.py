import time
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from ..mqtt import MQTTClient
from ..forms import ScheduleForm

global mqtt

# mqtt last will / testament
mqtt = MQTTClient("192.168.69.2", 1883, "prises")

def main(request):
    data = mqtt.last_message
    prise1 = mqtt.request_wait("prise1", 5)
    prise2 = mqtt.request_wait("prise2", 5)
    return render(request, 'main.html', {
        "prise1": {"state": prise1["state"], "temp": round(float(prise1["temp"]), 2)},
        "prise2": {"state": prise2["state"], "temp": round(float(prise2["temp"]), 2)}
        })

def set(request, prise: str, onoff: str):
    if onoff == "on":
        mqtt.publish_set(prise, True)
    elif onoff == "off":
        mqtt.publish_set(prise, False)

    time.sleep(0.1)
    return redirect('/')

def request(request, prise: str):
    mqtt.request_wait(prise)
    return redirect('/')

def schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            prise = form.cleaned_data["prise"][0] # car c'est une liste avec 1 element
            start = form.cleaned_data["start"]
            end = form.cleaned_data["end"]
            print(type(start))
            mqtt.set_schedule(prise, start, end)
            return redirect('/')
        else:
            return render(request, 'schedule.html', {"form": form})
    else:
        form = ScheduleForm()
        return render(request, 'schedule.html', {"form": form})

def schedule_reset(request, prise: str):
    mqtt.reset_schedule(prise)
    return redirect('/')