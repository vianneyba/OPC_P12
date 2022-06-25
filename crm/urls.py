from django.urls import path
from rest_framework.routers import DefaultRouter
from crm import views

router = DefaultRouter()
router.register(r"clients", views.ClientViewSet, basename="client")
router.register(r"contracts", views.ContractViewSet, basename="contract")
router.register(r"events", views.EventViewSet, basename="event")
router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = [

]
urlpatterns += router.urls