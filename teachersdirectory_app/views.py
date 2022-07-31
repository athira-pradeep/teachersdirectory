from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

# autheticate plugin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import csv
from django.shortcuts import HttpResponse

from .models import LoginTable, TeachersTable
from .forms import TeachersForm
import json


# Create your views here.

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def SearchData(request):
    print("search")
    if is_ajax(request=request):
        res = None
        lastname = request.POST.get('lastname')
        subjects = request.POST.get('subjects')
        print("search")
        print(lastname)
        print("subje", subjects)
        qs = TeachersTable.objects.filter(lastname__icontains=lastname,subjects__icontains=lastname)
        print("&&&&&&&&&&&", qs)
        if len(qs) > 0 and len(lastname) > 0:
            data = []
            for pos in qs:
                item = {
                    'fname': pos.firstname,
                    'lname': pos.lastname,
                    'email': pos.email,
                    'phone': pos.phone,
                    'subject': pos.subjects,
                    'roomno': pos.roomno,
                }
                data.append(item)
            res = data
        else:
            res = "Record Not Found..........."
        return JsonResponse({'data': res})
    else:
        return JsonResponse()


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def IndexPage(requets):
    context = {}
    if requets.method == "POST":
        login_id = requets.POST.get("username")
        password = requets.POST.get("password")
        user = authenticate(username=login_id, password=password)
        if user:
            login(requets, user)
            return redirect(Dashboard)
        else:
            print("not login")
            messages.info(requets, 'username or password incorrect')

    return render(requets, 'teachersdirectory_app/login.html', context)


def TeachersList(request):
    teachers_list = TeachersTable.objects.all()
    context = {
        'data_list': teachers_list,
    }

    return render(request, 'teachersdirectory_app/teachers_view.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def Dashboard(request):
    recs = TeachersTable.objects.all()
    context = {
        'data_list': recs
    }
    return render(request, 'teachersdirectory_app/teachers_list.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@login_required(login_url='login')
def Createteachers(request):
    form = TeachersForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            subjs = form['subjects'].value()
            sub = subjs.split(',')
            if len(sub) <= 5:
                form.save()
                return redirect(Dashboard)
            else:
                messages.info(request, 'Subject is more than 5 so please enter only 5 subjects')

        else:
            print("no")
    print("***")
    context = {
        'form': form
    }
    return render(request, 'teachersdirectory_app/create_teachers.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def ViewProfile(request, pk):
    obj = get_object_or_404(TeachersTable, id=pk)
    form = TeachersForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        data = form.save(commit=False)
        data.save()
        return redirect(Dashboard)
    else:
        print("not save ")
    context = {
        'form': form
    }
    return render(request, 'teachersdirectory_app/view_profile.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def BulkImporter(request):
    try:
        csvpath = (settings.MEDIA_ROOT)
        print("CSV")
        print(csvpath)
        print(os.listdir(csvpath))
        for file in os.listdir(csvpath):
            if file.endswith('.csv'):
                with open(f'{csvpath}/{file}', 'rt') as f:
                    data = csv.DictReader(f)
                    data_row = [dt for dt in data]
                    for csvdata in data_row:
                        firstname = csvdata['First Name']
                        lastname = csvdata['Last Name']
                        profile_pic = csvdata['Profile picture']
                        email = csvdata['Email Address']
                        phone = csvdata['Phone Number']
                        roomno = csvdata['Room Number']
                        subject = csvdata['Subjects taught']

                        if TeachersTable.objects.filter(email=email).exists():
                            print("already exist")
                        else:
                            sub = subject.split(',')
                            if len(sub) <= 5:
                                data = TeachersTable(firstname=firstname, lastname=lastname,
                                                     profile_pic='/profilepic/' + profile_pic,
                                                     phone=phone, roomno=roomno, subjects=subject)
                                data.save()
                            else:
                                print("Subjects more than 5 ")


            else:
                print("MEDIA")

        return redirect(Dashboard)

    except Exception as e:
        print(e)
        raise


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Logout(request):
    print(login)
    logout(request)
    return redirect(IndexPage)
