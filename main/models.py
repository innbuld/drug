from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)

class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="p_prescription")
    patient = models.CharField(max_length=255)
    pres = models.CharField(max_length=255)
    dispensed = models.BooleanField(default=False)
    dispensed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="p_dispensed")
    date = models.DateTimeField(auto_now=True)


