import re
from django.shortcuts import render, redirect
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.http import HttpResponse
from datetime import datetime
from django.views.generic import ListView
from django.http import JsonResponse
import random, datetime, json, sys
from django.views.decorators.csrf import csrf_exempt
from .models import SensorReading



# Create your views here.
class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")

def dashboard(request):
    return render(request, "hello/dashboard.html")

def hello_there(request, name):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "hello/log_message.html", {"form": form})
    

    # original random value upload to dashboard
"""def sensor_data(request):
    # In reality, you'd fetch from your DB or ESP32
    data = {
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "temperature": round(20 + random.random()*5, 1),  # simulate
        "humidity": round(40 + random.random()*10, 1),
        "pm25": round(5 + random.random()*10, 1)
    }
    return JsonResponse(data)     
"""



@csrf_exempt
def sensor_data(request):
    print("sensor_data endpoint hit")
    sys.stdout.flush() 
    if request.method == 'POST':
        try:
            # Parse JSON data from ESP32
            data = json.loads(request.body.decode('utf-8'))

            # Extract individual values
            pm1 = data.get('pm1')
            pm25 = data.get('pm25')
            pm10 = data.get('pm10')

            # Print to Django console for debugging
            print(f"Received data -> PM1: {pm1}, PM2.5: {pm25}, PM10: {pm10}")
            print("got it")
            sys.stdout.flush()

            # (Optional) Here’s where you could save to your database model
            
            SensorReading.objects.create(pm1=pm1, pm25=pm25, pm10=pm10)

            # Send response back to ESP32
            return JsonResponse({
                'status': 'ok',
                'saved': True
            })

        except Exception as e:
            print("Error handling POST:", e)
            sys.stdout.flush()
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=400)


def latest_readings(request):
    latest = SensorReading.objects.order_by('-timestamp')[:50]  # last 50 readings
    data = [
        {'pm1': r.pm1, 'pm25': r.pm25, 'pm10': r.pm10, 'timestamp': r.timestamp.isoformat()}
        for r in latest
    ]
    return JsonResponse(data, safe=False)