from django.urls import path
from rooms import views

app_name = "rooms"

urlpatterns = [path("<int:pk>", views.RoomDetail.as_view(), name="detail")]
