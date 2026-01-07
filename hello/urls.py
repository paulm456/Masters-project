from django.urls import path
from . import views
from hello.models import LogMessage


home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="hello/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/sensor/", views.sensor_data, name="sensor_data"),
    path("log/", views.log_message, name="log"),
    path('api/latest-readings/', views.latest_readings, name='latest_readings'),


]

