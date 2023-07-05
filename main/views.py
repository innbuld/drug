from django.shortcuts import render
from sqlite3 import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, 'main/index.html')

    if request.method == "POST":
        role = request.POST["role"]
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            if role == "doctor":
                if user.is_doctor:
                    return HttpResponseRedirect(reverse("doctor"))
                messages.error(request, "Only Doctors have access to this portal!")
                return HttpResponseRedirect(reverse("index"))

            if user.is_pharmacist:
                return HttpResponseRedirect(reverse("pharma"))
            messages.error(request, "Only Pharmacist have access to this portal!")
            return HttpResponseRedirect(reverse("index"))


        return HttpResponse("User not registered") 

@login_required
def doctor(request):
    if request.method == "GET":
        prescriptions = models.Prescription.objects.all()
        return render(request, 'main/doctor.html', {"prescriptions":prescriptions})

@login_required
def pharma(request):
    if request.method == "GET":
        prescriptions = models.Prescription.objects.all()
        return render(request, 'main/pharma.html', {"prescriptions":prescriptions})

@login_required
def prescription(request):
    if request.method == "GET":
        return render(request, 'main/prescription.html')

    if request.method == "POST":
        patient = request.POST["patient"]
        doctor_prescription = request.POST["about"]

        try:
            n_pre = models.Prescription(
                doctor = request.user,
                patient = patient,
                pres = doctor_prescription,
                dispensed = False,
                dispensed_by= request.user
            )

            n_pre.save()
        except IntegrityError:
            messages.error(request, "Unable to register prescription!")
            return HttpResponseRedirect(reverse("doctor"))

        messages.success(request, "Prescription registered successfully!")
        return HttpResponseRedirect(reverse("doctor"))


@login_required
def report(request, id):
    try:
        pre = models.Prescription.objects.get(pk=id)
    except Prescription.DoesNotExist:
        messages.error(request, "Prescription does not exist")
        return HttpResponseRedirect(reverse("doctor"))

    return render(request, 'main/report.html', {"p":pre})

@login_required
def dispense(request, id):
    try:
       pre = models.Prescription.objects.get(pk=id)
    except Prescription.DoesNotExist:
        messages.error(request, "Prescription does not exist")
        return HttpResponseRedirect(reverse("pharma"))

    pre.dispensed = True
    pre.dispensed_by = request.user
    pre.save()

    messages.success(request, "Dispenssed Successfully!")
    return HttpResponseRedirect(reverse("pharma"))

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

