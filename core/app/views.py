import datetime
import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import AuthForm
from .forms import WebForm, StatusForm
from PIL import Image
import os
import base64
from io import BytesIO
from .main_core import get_embeddings, is_match
from django.views.decorators.csrf import csrf_exempt
from .models import Web



@login_required()
def register_user(request):
    check = request.user.is_superuser
    web_form = WebForm()
    d = {"web_form": web_form}
    if request.method == "POST":
        print("User exists")
        print(request.POST)
        web_form = WebForm(request.POST)
        try:
            if web_form.is_valid():
                print("User exists")
                ph_num = request.POST['ph_num']
                # try:
                #     print("User exists")
                #     a = Web.objects.get(ph_num=ph_num)
                # except Web.DoesNotExist:
                #     a = None
                # if a is None:
                web_form.save()
                return render(request, 'web.html', {"ph_num": ph_num})
            elif len(Web.objects.get(ph_num=request.POST.get("ph_num")).weights) == 0:
                print("Current gone")
        except ValueError:
            print("Got Value Error")
            return render(request, 'web.html', {"ph_num": request.POST.get('ph_num')})
    d = {"web_form": web_form, "check": check}
    return render(request, 'register_user.html', d)


@login_required()
def authenticate_user(request):
    check = request.user.is_superuser
    auth_form = AuthForm()
    print(check)
    d = {"auth_form": auth_form, "check": check}
    if request.method == "POST":
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            ph_num = request.POST.get('ph_num')
            d["ph_num"] = ph_num
            try:
                if len(Web.objects.get(ph_num=ph_num).weights) == 0:
                    print("Pass")
            except ValueError:
                messages.error(request, " User  not found , please register!! ")
                return redirect('authenticate_user')
            except Web.DoesNotExist:
                messages.error(request, "User  not found, please register!!")
                return redirect('authenticate_user')

            return render(request, 'web_1.html', {"ph_num": ph_num})

    return render(request, 'authenticate.html', d)


@csrf_exempt
def web(request):
    def getsize(f):
        f.seek(0)
        f.read()
        s = f.tell()
        f.seek(0)
        return s

    if request.method == "POST":
        b = request.POST.get('base64')
        num = request.POST.get('num')
        image = ContentFile(base64.b64decode(b))
        s = num + '.jpg'
        im = Image.open(image)
        tempfile_io = BytesIO()
        im.save(tempfile_io, format='JPEG')
        image_file = InMemoryUploadedFile(tempfile_io, None, s, 'image/jpeg', getsize(tempfile_io), None)
        a = Web.objects.get(ph_num=num)
        a.weights.save(s, image_file)
        print(num)

    return HttpResponse("<h1>You are not Authorized!!</h1>")


@csrf_exempt
def webAuth(request):
    match = ""

    def getsize(f):
        f.seek(0)
        f.read()
        s = f.tell()
        f.seek(0)
        return s

    if request.method == "POST":
        check = False
        b = request.POST.get('base64')
        num = request.POST.get('num')
        image = ContentFile(base64.b64decode(b))
        s = num + '.jpg'
        im = Image.open(image)
        im.save(s)
        a = Web.objects.get(ph_num=num)
        try:
            weights = get_embeddings([a.weights, s])
            check = is_match(weights[0], weights[1])
        except IndexError:
            print("Index out of range")
            check = False
        finally:
            os.remove(s)
            if check:

                print("Face Matched")
                tempfile_io = BytesIO()
                im.save(tempfile_io, format='JPEG')
                image_file = InMemoryUploadedFile(tempfile_io, None, s, 'image/jpeg', getsize(tempfile_io), None)
                a = Web.objects.get(ph_num=num)
                a.weights = ""
                a.save()
                a = Web.objects.get(ph_num=num)
                remove = 'users/' + s
                d = datetime.datetime.now()
                month = d.strftime("%b")
                date = d.strftime("%d")
                mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                if date == '01' and month != "Jan":
                    b = Web.objects.get(ph_num=num)
                    com = json.loads(b.attendance)
                    i = mon.index(month) - 1
                    mont = mon[i]
                    lst = com[str(mont)]
                    print(lst)
                    if lst[len(lst) - 1] == 2:
                        lst[len(lst) - 1] = 0
                        com[str(mont)] = lst
                        b.attendance = json.dumps(com)
                        b.save()
                a = Web.objects.get(ph_num=num)
                comp = json.loads(a.attendance)
                l = comp[str(month)]
                l[int(date) - 1] = 1
                for i in range(0, int(date) - 1):
                    if l[i] == 2:
                        l[i] = 0
                for i in range(int(date), len(l)):
                    l[i] = 2
                comp[str(month)] = l
                a.attendance = json.dumps(comp)
                os.remove(os.path.join(settings.MEDIA_ROOT, remove))
                a.weights.save(s, image_file)
                a.save()
                match = "successful"
            else:
                print("Face not matched")
                num = request.POST.get('num')
                match = "unsuccessful"

    return HttpResponse(match)


@login_required()
def home(request):
    d = datetime.datetime.now()
    mon = d.strftime("%b")
    l = abc(mon)
    form = StatusForm()
    check = request.user.is_superuser
    return render(request, "profile.html", {"form": form, "check": check, "l": l})


@login_required()
def success(request):
    check = request.user.is_superuser and "as"
    return render(request, "accept.html", {"check": check})


@login_required()
def failure(request):
    check = request.user.is_superuser and "af"
    return render(request, "failure.html", {"check": check})


@login_required()
def Success(request):
    check = request.user.is_superuser and "rs"
    return render(request, "accept.html", {"check": check})


@login_required()
def Failure(request):
    check = request.user.is_superuser and "rf"
    return render(request, "failure.html", {"check": check})


def get_white_spaces(year, month):
    mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    a = mon.index(month) + 1
    day = datetime.datetime(year, a, 1)
    day = day.strftime("%a")
    nos = week.index(day)
    return nos


def abc(month):
    mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    l = mon[:mon.index(month) + 1]
    return l


def Calender(request):
    d = datetime.datetime.now()
    month = d.strftime("%b")
    l = abc(month)
    if request.method == "POST":
        mon = request.POST.get('month')
        num = request.POST.get('number')
        try:
            a = Web.objects.get(ph_num=num)
        except Web.DoesNotExist:
            messages.error(request, "User  not found !!")
            return redirect('home')
        comp = json.loads(a.attendance)
        b = datetime.datetime.strptime(str(mon), "%b")
        c = datetime.datetime(d.year, int(b.strftime("%m")), 1)
        c = c.strftime("%B")
        nos_spaces = get_white_spaces(d.year, mon)
        lst = list(comp[str(mon)])
        if month == mon and lst.count(0) == len(lst):
            lst = [2] * len(lst)
        for i in range(nos_spaces):
            lst.insert(0, -1)

        return render(request, "calendar.html",
                      {"lst": lst, "nos": -nos_spaces, "l": l, "ph_num": num, "name": a.name, "present": lst.count(1),
                       "absent": lst.count(0), "month": c})
