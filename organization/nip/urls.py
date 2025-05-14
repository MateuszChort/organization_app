from django.urls import path

from .views import get_data_by_nip

urlpatterns = [path("<int:nip>/", get_data_by_nip, name="nip")]
