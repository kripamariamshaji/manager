from django. contrib import messages
from unicodedata import name
from django.shortcuts import render
from django.shortcuts import render, redirect
from trainingapp.models import *
from datetime import datetime,date
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from io import BytesIO
from django.core.files import File
from django.conf import settings
import qrcode
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate , login , logout
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def Tlogin(request):
    des = designation.objects.get(designation_name='manager')
    des1 = designation.objects.get(designation_name='trainer')
    des2 = designation.objects.get(designation_name='trainee')
    des3 = designation.objects.get(designation_name='accounts')

    if request.method == 'POST':
        
        email  = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
                request.session['SAdm_id'] = user.id
                return redirect( 'Admin_Dashboard')
        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'], designation_id=des.id).exists():
                member = user_registration.objects.get(
                email=request.POST['email'], password=request.POST['password'])
                request.session['m_designation_id'] = member.designation_id
                request.session['m_fullname'] = member.fullname
                request.session['m_id'] = member.id
                return render(request, 'dashsec.html', {'member': member})
        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'], designation_id=des1.id).exists():
                member = user_registration.objects.get(
                email=request.POST['email'], password=request.POST['password'])
                request.session['tr_designation_id'] = member.designation_id
                request.session['tr_fullname'] = member.fullname
                request.session['tr_team_id'] = member.team_id
                request.session['tr_id'] = member.id
                return render(request, 'tr_sec.html', {'member': member})
        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'], designation_id=des2.id).exists():
                member = user_registration.objects.get(
                email=request.POST['email'], password=request.POST['password'])
                request.session['te_designation_id'] = member.designation_id
                request.session['te_fullname'] = member.fullname
                request.session['te_id'] = member.id
                request.session['te_team_id'] = member.team_id
                return render(request, 'traineesec.html', {'member': member})
        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'], designation_id=des3.id).exists():
                member = user_registration.objects.get(
                email=request.POST['email'], password=request.POST['password'])
                request.session['acc_designation_id'] = member.designation_id
                request.session['acc_fullname'] = member.fullname
                request.session['acc_id'] = member.id
                return render(request, 'accountsec.html', {'member': member})
        elif request.method == 'POST':
                username = request.POST.get('email', None)
                password = request.POST.get('password', None)                    
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('Admin_Dashboard')
        else:
                context = {'msg': 'Invalid username or password'}
                return render(request, 'login.html', context)
    return render(request,'login.html')       



    
        # if request.method == 'POST':
        #     username = request.POST.get('email', None)
        #     password = request.POST.get('password', None)
        #     user = authenticate(email=username, password=password)
        #     if user:
        #         login(request, user)
        #         return redirect('Admin_Dashboard')
        #     else:
        #           context = {'msg': 'Invalid username or password'}
        #           return render(request, 'login.html',context)
        # if request.method == 'POST':
        #     email  = request.POST['email']
        #     password = request.POST['password']
        #     user = authenticate(email=email, password=password)
        #     if user is not None:
        #             request.session['SAdm_id'] = user.id
        #             return redirect('Admin_Dashboard')

        #     else:
        #         context = {'msg': 'Invalid username or password'}
        #         return render(request, 'login.html', context)
    

def manager_logout(request):
    if 'm_id' in request.session:  
        request.session.flush()
        return redirect('Tlogin')
    else:
        return redirect('Tlogin') 

def Admin_logout(request):
    auth.logout(request)
    return redirect('Tlogin')

def index(request):
    return render(request,'software_training/training/index.html')
    
def Trainings(request):
    return render(request,'software_training/training/training.html')

#******************Manager*****************************

def Manager_Dashboard(request):
    if 'm_id' in request.session:
        
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
       
        mem = user_registration.objects.filter(id=m_id)
        
        
        return render(request, 'software_training/training/manager/manager_Dashboard.html', {'mem': mem ,})
    else:
        return redirect('/')
    
def Manager_trainer(request):
    
    if request.session.has_key('m_id'):
        m_id = request.session['m_id']
        
        mem = user_registration.objects.filter(id=m_id)
        des = designation.objects.get(designation_name='trainer')
        vars = user_registration.objects.filter(designation_id=des.id).all().order_by('-id')
        return render(request,'software_training/training/manager/manager_trainer.html', {'vars': vars, 'mem': mem})
    else:
        return redirect('/')
    
def manager_team(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id) .filter(fullname=m_fullname)
        d = user_registration.objects.get(id=id)
        return render(request, 'software_training/training/manager/manager_team.html', {'d': d, 'mem': mem})
    return redirect('/')

def manager_current_team(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        d = user_registration.objects.get(id=id)
        tm = create_team.objects.filter(create_team_trainer=d.fullname).filter(create_team_status=0).order_by('-id')
        des = designation.objects.get(designation_name='trainer')
        cut = user_registration.objects.filter(designation_id=des.id)
        vars = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)
        return render(request, 'software_training/training/manager/manager_current_team.html', {'vars': vars, 'des': des, 'tm': tm, 'cut': cut, 'mem': mem})
    else:
        return redirect('/')

def Manager_current_task(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        mem = user_registration.objects.filter(id=m_id)
        d = create_team.objects.get(id=id)
        return render(request,'software_training/training/manager/manager_current_task.html',{'d': d, 'mem': mem})
    else:
        return redirect('/')

def manager_current_assigned(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        d = create_team.objects.get(id=id)
        vars = topic.objects.filter(topic_team_id=d.id).order_by('-id')
        return render(request, 'software_training/training/manager/manager_current_assigned.html', {'vars': vars, 'mem': mem})
    else:
        return redirect('/')
    
def manager_current_trainees(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        d = create_team.objects.get(id=id)
        des = designation.objects.get(designation_name='trainee')
        vars = user_registration.objects.filter(team=d.id,designation_id=des.id).order_by('-id')
        return render(request, 'software_training/training/manager/manager_current_trainees.html', {'vars': vars, 'mem': mem})
    else:
        return redirect('/')

def manager_current_empdetails(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        vars = user_registration.objects.get(id=id)
        tre = create_team.objects.get(id=vars.team_id)
        labels = []
        data = []
        queryset = user_registration.objects.filter(id=vars.id)
        for i in queryset:
            labels=[i.workperformance,i.attitude,i.creativity]
            data=[i.workperformance,i.attitude,i.creativity]
        return render(request, 'software_training/training/manager/manager_current_empdetails.html', {'vars': vars, 'tre': tre, 'mem': mem ,'labels': labels,'data': data})
    else:
        return redirect('/')

def manager_current_attendance(request,id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        vars = user_registration.objects.get(id=id)
        return render(request, 'software_training/training/manager/manager_current_attendance.html', {'vars':vars,'mem': mem})
    else:
        return redirect('/')

def manager_current_attendance_list(request,id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        vars = user_registration.objects.get(id=id)
        if request.method == 'POST':
            std = request.POST['startdate']
            edd = request.POST['enddate']
            user=vars
            atten = attendance.objects.filter(attendance_date__gte=std,attendance_date__lte=edd,attendance_user_id=user)
        return render(request,'software_training/training/manager/manager_current_attendance_list.html',{'mem':mem,'vars': vars, 'atten':atten})
    else:
        return redirect('/')

def manager_current_task_list(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        d = user_registration.objects.get(id=id)
        tsk = trainer_task.objects.filter(trainer_task_user_id=d.id).order_by('-id')
        return render(request, 'software_training/training/manager/manager_current_task_list.html', {'tsk': tsk, 'mem': mem})
    else:
        return redirect('/')
    
def manager_current_task_details(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        d = user_registration.objects.get(id=id)
        tsk = trainer_task.objects.get(id=d.id)
        return render(request, 'software_training/training/manager/manager_current_task_details.html', {'tsk': tsk, 'mem': mem})
    else:
        return redirect('/')

def manager_previous_team(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        d = user_registration.objects.get(id=id)
        tm = create_team.objects.filter(create_team_trainer = d.fullname).filter(create_team_status = '1')
        des = designation.objects.get(designation_name='trainer')
        cut = user_registration.objects.filter(designation_id=des.id)
        vars = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)
        return render(request, 'software_training/training/manager/manager_previous_team.html', {'vars': vars, 'des': des, 'tm': tm, 'cut': cut, 'mem': mem})
    else:
        return redirect('/')

def Manager_previous_task(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        d = create_team.objects.get(id=id)
        return render(request, 'software_training/training/manager/manager_previous_task.html', {'d': d, 'mem': mem})
    else:
        return redirect('/')

def manager_previous_assigned(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        d = create_team.objects.get(id=id)
        vars = topic.objects.filter(topic_team_id=d.id)
        return render(request, 'software_training/training/manager/manager_previous_assigned.html', {'vars': vars, 'mem': mem})
    else:
        return redirect('/')

def manager_previous_trainees(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        d = create_team.objects.get(id=id)
        des = designation.objects.get(designation_name='trainee')
        vars = user_registration.objects.filter(
            team_id=d.id).filter(designation_id=des.id).order_by('-id')
        return render(request, 'software_training/training/manager/manager_previous_trainees.html', {'vars': vars, 'mem': mem})
    else:
        return redirect('/')

def manager_previous_empdetails(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        vars = user_registration.objects.get(id=id)
        tre = create_team.objects.get(id=vars.team_id)
        labels = []
        data = []
        queryset = user_registration.objects.filter(id=vars.id)
        for i in queryset:
            labels=[i.workperformance,i.attitude,i.creativity]
            data=[i.workperformance,i.attitude,i.creativity]
        return render(request, 'software_training/training/manager/manager_previous_empdetails.html', {'vars': vars, 'tre': tre, 'mem': mem ,'labels': labels,'data': data})
    else:
        return redirect('/')

def manager_previous_attendance(request,id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        vars = user_registration.objects.get(id=id)
        return render(request, 'software_training/training/manager/manager_previous_attendance.html',{'mem':mem, 'vars':vars})
    else:
        return redirect('/')

def manager_previous_attendance_list(request,id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        vars = user_registration.objects.get(id=id)
        if request.method == 'POST':
            std = request.POST['startdate']
            edd = request.POST['enddate']
            user=vars
            atten = attendance.objects.filter(attendance_date__gte=std,attendance_date__lte=edd,attendance_user_id=user)
        return render(request, 'software_training/training/manager/manager_previous_attendance_list.html',{'mem':mem,'vars': vars, 'atten':atten})
    else:
        return redirect('/')

def manager_previous_task_list(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)
        d = user_registration.objects.get(id=id)
        tsk = trainer_task.objects.filter(trainer_task_user=d.id)
        return render(request, 'software_training/training/manager/manager_previous_task_list.html', {'tsk': tsk, 'mem': mem})
    else:
        return redirect('/')

def manager_previous_task_details(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)
        tsk = trainer_task.objects.get(id=id)
        return render(request, 'software_training/training/manager/manager_previous_task_details.html', {'tsk': tsk, 'mem': mem})
    else:
        return redirect('/')

def manager_trainee(request):
    if request.session.has_key('m_id'):
        m_id = request.session['m_id']
        
        mem = user_registration.objects.filter(id=m_id)
        des = designation.objects.get(designation_name='trainee')
        tre = user_registration.objects.filter(designation_id=des.id).all().order_by('-id')
        return render(request,'software_training/training/manager/manager_trainee.html', {'tre': tre, 'mem': mem})
    else:
       return render(request,'software_training/training/manager/manager_trainee.html')
    
    

def Manager_trainees_details(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            usernametm1 = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id) .filter(fullname=m_fullname)
        vars= user_registration.objects.get(id=id) 
        tre = create_team.objects.get(id=vars.team.id)
        labels = []
        data = []
        queryset = user_registration.objects.filter(id=vars.id)
        for i in queryset:
            labels=[i.workperformance,i.attitude,i.creativity]
            data=[i.workperformance,i.attitude,i.creativity]  
        return render(request,'software_training/training/manager/Manager_trainees_details.html',{'mem':mem,'vars':vars,'tre':tre ,'labels': labels,'data': data})
    else:
        return redirect('/')

def Manager_trainees_attendance(request , id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            usernametm1 = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id) .filter(fullname=m_fullname)
        vars= user_registration.objects.get(id=id)
        if request.method == 'POST':
            std = request.POST['startdate']
            edd = request.POST['enddate']
            user=vars
            atten = attendance.objects.filter(attendance_date__gte=std,attendance_date__lte=edd,attendance_user_id=user)
        return render(request,'software_training/training/manager/Manager_trainees_attendance.html',{'mem':mem,'vars':vars, 'atten':atten})
    else:
        return redirect('/')
    

def Manager_reported_issues(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            usernametm1 = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id) .filter(fullname=m_fullname)
        return render(request, 'software_training/training/manager/manager_reported_issues.html', {'mem': mem})
    else:
        return redirect('/')
    

def manager_trainerreportissue(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id) .filter(fullname=m_fullname)
        return render(request, 'software_training/training/manager/manager_trainerreportissue.html', {'mem': mem})
    else:
        return redirect('/')
    
def manager_trainer_unsolvedissue(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id) .filter(fullname=m_fullname)
        des = designation.objects.get(designation_name='trainer')
        cut = reported_issue.objects.filter(reported_issue_reported_to_id=m_id,reported_issue_designation_id_id=des.id,reported_issue_issuestatus=0).order_by('-id')
        a=cut.count()
        context = {'cut': cut, 'vars': vars, 'mem': mem,'a':a}
        return render(request,'software_training/training/manager/manager_trainer_unsolvedissue.html',context)
    else:
        return redirect('/')

def savetmreplaytrnr(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id) .filter(fullname=m_fullname)
        vars = reported_issue.objects.get(id=id)
        if request.method == 'POST':
            vars.reported_issue_reply = request.POST['review']
            vars.reported_issue_issuestatus = 1
            vars.save()
        return redirect('manager_trainerreportissue')
    else:
        return redirect('/')

def manager_trainer_solvedissue(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id) .filter(fullname=m_fullname)
        des = designation.objects.get(designation_name='trainer')
        print(des.id)
        cut = reported_issue.objects.filter(reported_issue_reported_to_id=m_id).filter(reported_issue_designation_id_id=des.id).filter(reported_issue_issuestatus=1).order_by('-id')
        context = {'cut': cut, 'vars': vars, 'mem': mem}
        return render(request,'software_training/training/manager/manager_trainer_solvedissue.html',context)
    else:
        return redirect('/')

def manager_traineereportissue(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        return render(request,'software_training/training/manager/manager_traineereportissue.html', {'mem': mem})
    else:
        return redirect('/')
    
def manager_trainee_unsolvedissue(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id) .filter(fullname=m_fullname)
        des = designation.objects.get(designation_name='trainee')
        cut = reported_issue.objects.filter(reported_issue_reported_to_id=m_id).filter(reported_issue_designation_id_id=des.id).filter(reported_issue_issuestatus=0).order_by('-id')
        context = {'cut': cut, 'vars': vars, 'mem': mem}
        return render(request,'software_training/training/manager/manager_trainee_unsolvedissue.html', context)
    else:
        return redirect('/')

def savetmreplytrns(request, id):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id) .filter(fullname=m_fullname)
        vars = reported_issue.objects.get(id=id)
        if request.method == 'POST':
            vars.reported_issue_reply = request.POST['review']
            vars.reported_issue_issuestatus = 1
            vars.save()
        return redirect('manager_traineereportissue')
    else:
        return redirect('/')

def manager_trainee_solvedissue(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        else:
            m_id = "dummy"
        mem = user_registration.objects.all()
        des = designation.objects.get(designation_name='trainee')
        print(des.id)
        cut = reported_issue.objects.filter(reported_issue_reported_to_id=m_id).filter(reported_issue_designation_id_id=des.id).filter(reported_issue_issuestatus=1).order_by('-id')
        context = {'cut': cut, 'vars': vars, 'mem': mem}
        return render(request,'software_training/training/manager/manager_trainee_solvedissue.html',context)
    else:
        return redirect('/')

def manager_report_issue(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        des = designation.objects.get(designation_name='Admin')
        des1 = designation.objects.get(designation_name='manager')
        ree = user_registration.objects.get(designation_id=des.id)
        if request.method == 'POST':
            vars = reported_issue()
            vars.reported_issue_issue = request.POST['issue']
            vars.reported_issue_issuestatus = 0
            vars.reported_issue_reporter_id = m_id
            vars.reported_issue_designation_id_id = des1.id
            vars.reported_issue_reported_to = ree
            vars.reported_issue_reported_date = datetime.now()
            vars.save()
            return redirect('Manager_reported_issues')
        return render(request, 'software_training/training/manager/manager_report_issue.html', {'mem': mem})
    else:
        return redirect('/')

def manager_reported_issue(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        cut = reported_issue.objects.filter(reported_issue_reporter=m_id).order_by('-id')
        context = {'cut': cut, 'vars': vars, 'mem': mem}
        return render(request,'software_training/training/manager/manager_reported_issue.html', context)
    else:
        return redirect('/')





def Manager_attendance(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        
        else:
            m_id = "dummy"
    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)        
        return render(request, 'software_training/training/manager/manager_attendance.html',{'mem':mem})
    else:
        return redirect('/')
  

def manager_trainee_attendance(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        
        else:
            m_id = "dummy"    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)    
        des = designation.objects.get(designation_name='trainee')
        vars = user_registration.objects.filter(designation_id=des.id)        
        return render(request, 'software_training/training/manager/manager_trainee_attendance.html',{'mem':mem, 'vars':vars})
    else:
        return redirect('/')
    

def manager_trainer_attendance(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']        
        else:
            m_id = "dummy"
    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)    
        des = designation.objects.get(designation_name='trainer')
        vars = user_registration.objects.filter(designation_id=des.id)        
        return render(request, 'software_training/training/manager/manager_trainer_attendance.html',{'mem':mem, 'vars':vars})
    else:
        return redirect('/')    

def manager_trainer_attendance_table(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        
        else:
            m_id = "dummy"
    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)
        if request.method == 'POST':
            start=request.POST['startdate']
            end=request.POST['enddate']
            user = request.POST['trainer']
            attend=attendance.objects.filter(attendance_date__gte=start,attendance_date__lte=end,attendance_user_id=user)
        return render(request, 'software_training/training/manager/manager_trainer_attendance_table.html',{'mem':mem,'vars':attend})
    else:
        return redirect('/')
    

def manager_trainee_attendance_table(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        
        else:
            m_id = "dummy"
    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname) 
        if request.method == 'POST':
            start=request.POST['startdate']
            end=request.POST['enddate']
            user = request.POST['trainee']
            attend=attendance.objects.filter(attendance_date__gte=start,attendance_date__lte=end,attendance_user_id=user)
        return render(request, 'software_training/training/manager/manager_trainee_attendance_table.html',{'mem':mem,'vars':attend})
    else:
        return redirect('/')
   
def manager_applyleave(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']        
        else:
            m_id = "dummy"
    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)
        return render(request, 'software_training/training/manager/manager_applyleave.html',{'mem':mem})
    else:
        return redirect('/')

    

def manager_applyleavsub(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']        
        else:
            m_id = "dummy"
    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)        
        des1 = designation.objects.get(designation_name='manager')
        cut = user_registration.objects.get(id=m_id)      
        if request.method == 'POST':
            vars = leave()
            vars.leave_from_date = request.POST['from']
            vars.leave_to_date = request.POST['to']
            vars.leave_reason = request.POST['reason']
            vars.leave_status = request.POST['haful']
            vars.leave_leaveapproved_status = 0
            vars.leave_user = cut
            vars.leave_designation_id = des1.id     
            vars.save()
            return redirect('manager_applyleave') 
        return render(request,'software_training/training/manager/manager_applyleavsub.html', {'mem': mem})
    else:
        return redirect('/')
  

def manager_requestedleave(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']        
        else:
            m_id = "dummy"
    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)
        des = designation.objects.get(designation_name='manager')
        print(des.id)
        cut = leave.objects.filter(leave_designation_id=des.id).order_by('-id')
        context = {'cut': cut, 'vars': vars, 'mem': mem}
        return render(request,'software_training/training/manager/manager_requestedleave.html', context)

    else:
        return redirect('/')



def manager_trainer_leave(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']        
        else:
            m_id = "dummy"
    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname) 
        return render(request, 'software_training/training/manager/manager_trainer_leave.html',{'mem':mem})
    else:
        return redirect('/')


def manager_trainers_leavelist(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']        
        else:
            m_id = "dummy"    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname) 
        mem = user_registration.objects.filter(designation_id=m_id) .filter(fullname=m_fullname)
        des = designation.objects.get(designation_name='trainer')
        cut = leave.objects.filter(leave_designation_id=des.id).filter(leave_leaveapproved_status=0).order_by('-id') 
        context = {'cut': cut, 'vars': vars, 'mem': mem}
        return render(request,'software_training/training/manager/manager_trainers_leavelist.html', context)
    else:
        return redirect('/')

def approvedstatus(request,id):
    a=leave.objects.get(id=id)
    a.leave_leaveapproved_status=1
    a.save()
    return redirect('manager_trainers_leavelist')

def Leave_rejected(request,id):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']        
        else:
            m_fullname = "dummy"    
        vars = leave.objects.get(id=id) 
        if request.method == 'POST':
            vars.leave_rejected_reason = request.POST['review']            
            vars.leave_leaveapproved_status = 2  
            vars.save()
        return redirect('manager_trainers_leavelist')
    else:
        return redirect('/')
   
def manager_trainer_leavestatus(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        mem = user_registration.objects.filter(
            designation_id=m_id) .filter(fullname=m_fullname)    
        des = designation.objects.get(designation_name='trainer')
        n = leave.objects.filter(leave_designation_id=des.id).order_by('-id') 
        return render(request, 'software_training/training/manager/manager_trainer_leavestatus.html', {'mem': mem ,'n': n})
    else:
        return redirect('/')

    

def manager_trainee_leave(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']        
        else:
            m_id = "dummy"    
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)
        return render(request, 'software_training/training/manager/manager_trainee_leave.html',{'mem':mem})
    else:
        return redirect('/')
    

def manager_trainee_leavelist(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_fullname = "dummy"    
        mem = user_registration.objects.filter(
            designation_id=m_id) .filter(fullname=m_fullname)        
        des = designation.objects.get(designation_name='trainee')       
        cut = leave.objects.filter(leave_designation_id=des.id).filter(leave_leaveapproved_status=0).order_by('-id')
        context = {'cut': cut, 'vars': vars, 'mem': mem}
        return render(request,'software_training/training/manager/manager_trainee_leavelist.html', context)
    else:
        return redirect('/')
    
def approvedstatus_trainee(request,id):
    a=leave.objects.get(id=id)
    a.leave_leaveapproved_status=1
    a.save()
    return redirect('manager_trainee_leavelist')

def Leave_rejected_trainee(request,id):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']        
        else:
            m_fullname = "dummy"
    
        vars = leave.objects.get(id=id) 
        if request.method == 'POST':      
            vars.leave_rejected_reason = request.POST['review']            
            vars.leave_leaveapproved_status = 2    
            vars.save()
        return redirect('manager_trainee_leavelist')
    else:
        return redirect('/')
    

def manager_trainee_leavestatus(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        mem = user_registration.objects.filter(
            designation_id=m_id) .filter(fullname=m_fullname)    
        des = designation.objects.get(designation_name='trainee')
        n = leave.objects.filter(leave_designation_id=des.id).order_by('-id')       
    
        return render(request, 'software_training/training/manager/manager_trainee_leavestatus.html', {'mem': mem ,'n': n})
    else:
        return redirect('/')


def manager_new_team(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_id = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        var = create_team.objects.all().order_by('-id')
        des = designation.objects.get(designation_name='trainer')
        var1 = user_registration.objects.filter(designation_id=des.id)
        return render(request, 'software_training/training/manager/manager_new_team.html', {'mem': mem, 'var': var, 'var1': var1})
    else:
        return redirect('/')
    
def manager_new_teamcreate(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
        des = designation.objects.get(designation_name='trainer')
        var = user_registration.objects.filter(designation_id=des.id)
        return render(request, 'software_training/training/manager/manager_new_teamcreate.html', {'mem': mem, 'var': var})
    else:
        return redirect('/')
def manager_newteamadd(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_fullname = "dummy"
    if request.method == 'POST':
        team = request.POST['team']
        trainer = request.POST.get('trainer')
        try:
            des = designation.objects.get(designation_name='trainer')
            var = user_registration.objects.filter(designation_id=des.id)
            user= create_team.objects.get(create_team_name=team)
            mem = user_registration.objects.filter(designation_id=m_designation_id) .filter(fullname=m_fullname)
            context = {'msg': 'Team already exists!!!....  Try another name','mem':mem,'var': var}
            return render(request, 'software_training/training/manager/manager_new_teamcreate.html',context)
        except :
            user= create_team(create_team_name=team, create_team_trainer=trainer, create_team_progress=0)
            user.save()
            return redirect('manager_new_team')

def manager_teamupdate(request,id):
    if 'm_id' in request.session:
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_fullname = "dummy"
    if request.method == 'POST':
        # tid = request.GET.get('tid')
        abc = create_team.objects.get(id=id)
        abc.create_team_name = request.POST.get('teams')
        abc.create_team_trainer = request.POST.get('trainer')
        abc.save()
        return redirect('manager_new_team')
    else:
        pass


def manager_teamdelete(request,id):
    if 'm_id' in request.session:
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_fullname = "dummy"
    var = create_team.objects.get(id=id)
    
    var.delete()
    return redirect("manager_new_team")



def manager_submit(request,id):
    if 'm_id' in request.session:
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_fullname = "dummy"
   
    if request.method == 'POST':
        var1 = create_team.objects.get(id=id)
        var1.create_team_status = 1        
        var1.save()
    return redirect("manager_new_team")
    
def manager_newtrainees(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id).filter(fullname=m_fullname)        
        categ = category.objects.all()
        des = course.objects.all()
        team = create_team.objects.all()
        mem1 = designation.objects.get(designation_name="trainee")
        memm = user_registration.objects.filter(designation_id=mem1).order_by('-id')
        return render(request, 'software_training/training/manager/manager_newtrainees.html', {'mem': mem,'des': des, 'memm': memm,  'team': team,  'categ': categ})
    else:
        return redirect('/')

def manager_newtraineeesteam(request,id):
    if 'm_id' in request.session:
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(
            designation_id=m_designation_id).filter(fullname=m_fullname)        
        register = user_registration()
        des = designation.objects.all()        
        team = create_team.objects.all()
        mem1 = designation.objects.get(designation_name="trainee")
        memm = user_registration.objects.filter(designation_id=mem1)        
        if request.method == 'POST':
            register = user_registration.objects.get(id=id)            
            register.team =create_team.objects.get(id=int(request.POST['team']))
            register.category =category.objects.get(id=int(request.POST['categ']))
            register.course =course.objects.get(id=int(request.POST['cou']))
            register.save()
            return redirect('manager_newtrainees')
        return render(request, 'software_training/training/manager/manager_newtrainees.html', {'memm': memm, 'des': des, 'team': team, })
    else:
        return redirect('/')

@csrf_exempt
def manager_newtrainees_categ(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname)
    
    cou = request.GET.get('cou')     
    cour = course.objects.filter(course_category=cou)   

    return render(request, 'software_training/training/manager/manager_newtrainees_categ.html', {'cour': cour})

def manager_changepassword(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id,id=m_id).filter(fullname=m_fullname)  
        mem = user_registration.objects.filter(id=m_id)    
        if request.method == 'POST':
            abc = user_registration.objects.get(id=m_id)    
            oldps = request.POST['currentPassword']
            newps = request.POST['newPassword']
            cmps = request.POST.get('confirmPassword')
            if oldps != newps:
                if newps == cmps:
                    abc.password = request.POST.get('confirmPassword')
                    abc.save()
                    return render(request, 'software_training/training/manager/manager_Dashboard.html', {'mem': mem,})
            elif oldps == newps:
                messages.add_message(request, messages.INFO, 'Current and New password same')
            else:
                messages.info(request, 'Incorrect password same')    
            return render(request, 'software_training/training/manager/manager_changepassword.html', {'mem': mem,})    
        return render(request, 'software_training/training/manager/manager_changepassword.html', {'mem': mem,})
    else:
        return redirect('/')

def manager_accountedit(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        else:
            m_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id,id=m_id).filter(fullname=m_fullname)  
        return render(request, 'software_training/training/manager/manager_accountedit.html', {'mem': mem})
    else:
        return redirect('/')

def manager_imagechange(request,id):  
    if request.method == 'POST':
        abc = user_registration.objects.get(id=id)
        abc.photo = request.FILES['filename']        
        abc.save()
        return redirect('manager_accountedit')
    return render(request, 'software_training/training/manager/manager_accountedit.html')

def manager_paymentlist(request):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_id = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname).filter(id=m_id)
        acc=acntspayslip.objects.filter(acntspayslip_user_id=m_id).all().order_by('-id')
        
        return render(request, 'software_training/training/manager/manager_paymentlist.html', {'acc': acc,'mem':mem})
    else:
        return redirect('/')

def manager_payment_viewslip(request,id,tid):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_id = "dummy"        
        mem= user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname).filter(id=m_id)
        user = user_registration.objects.get(id=tid)
        acc = acntspayslip.objects.get(id=id)
        names = acntspayslip.objects.all()  
        return render(request, 'software_training/training/manager/manager_payment_viewslip.html', {'mem': mem,'user':user,'acc':acc})
    else:
        return redirect('/')




def manager_payment_pdf(request,id,tid):
    date = datetime.now()   
    acc = acntspayslip.objects.get(id=id)
    user = user_registration.objects.get(id=tid)
    template_path = 'software_training/training/manager/manager_payment_pdf.html'
    context = {'acc': acc,'user':user,
    'media_url':settings.MEDIA_URL,
    'date':date
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] = 'filename="certificate.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def manager_payment_print(request,id,tid):
    if 'm_id' in request.session:
        if request.session.has_key('m_id'):
            m_id = request.session['m_id']
        if request.session.has_key('m_fullname'):
            m_fullname = request.session['m_fullname']
        if request.session.has_key('m_designation_id'):
            m_designation_id = request.session['m_designation_id']
        else:
            m_id = "dummy"
        mem = user_registration.objects.filter(designation_id=m_designation_id).filter(fullname=m_fullname).filter(id=m_id)
        z = user_registration.objects.filter(id=m_id)   
        user = user_registration.objects.get(id=tid)
        acc = acntspayslip.objects.get(id=id)       
        
        return render(request, 'software_training/training/manager/manager_payment_print.html', {'z': z,'user':user,'acc':acc,'mem': mem})
    else:
        return redirect('/')
    
#******************Trainer*****************************
def trainer_dashboard(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
           tr_id = request.session['tr_id']
        z = user_registration.objects.filter(id=tr_id)
        return render(request,'software_training/training/trainer/trainer_dashboard.html',{'z': z})
    else:
        return redirect('/')
        
def trainer_imagechange(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
           tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id).filter(fullname=tr_fullname)
        return render(request,'software_training/training/trainer/trainer_imagechange.html',{'z':z})
    else:
        return redirect('/')
        
def trainerimagechange(request,id):
    if request.method == 'POST':
        abc = user_registration.objects.get(id=id)
        abc.photo = request.FILES['filename']
        abc.save()
        return redirect('trainer_imagechange')
    return render(request, 'trainer_imagechange.html') 

def trainer_passwordchange(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
           tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id).filter(fullname=tr_fullname)
        if request.method=='POST':
            abc = user_registration.objects.get(id=tr_id)
            oldps = request.POST['currentPassword']
            newps = request.POST['newPassword']
            cmps = request.POST.get('confirmPassword')
            if oldps != newps:
                if newps == cmps:
                    abc.password = request.POST.get('confirmPassword')
                    abc.save()
                    return render(request, 'software_training/training/trainer/trainer_dashboard.html', {'z':z})
    
            elif oldps == newps:
                messages.add_message(request, messages.INFO, 'Current and New password same')
            else:
                messages.info(request, 'Incorrect password same')
            return render(request,'software_training/training/trainer/trainer_passwordchange.html',{'z':z})
        return render(request,'software_training/training/trainer/trainer_passwordchange.html',{'z':z})
    else:
        return redirect('/')
        
def trainer_logout(request):
    if 'tr_id' in request.session:
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/') 
    

def trainer_topic(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        return render(request,'software_training/training/trainer/trainer_topic.html',{'z': z})
    else:
        return redirect('/')

def trainer_addtopic(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
           tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        crt = create_team.objects.filter(create_team_trainer=tr_fullname,create_team_status=0)
        mem = topic()
        if request.method == 'POST':
            mem.topic_team_id = request.POST['select']
            mem.topic_topic = request.POST['topic']
            mem.topic_startdate = request.POST['start']
            mem.topic_enddate = request.POST['end']
            mem.topic_status = 0
            mem.topic_trainer_id = tr_id 
            mem.save()
            return render(request,'software_training/training/trainer/trainer_addtopic.html',{'crt':crt,'mem': mem,'z':z})
        return render(request,'software_training/training/trainer/trainer_addtopic.html',{'crt':crt,'mem': mem,'z':z})
    else:
        return redirect('/')

def trainer_viewtopic(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
    
        z = user_registration.objects.filter(id=tr_id)
        mem = topic.objects.filter(topic_trainer=tr_id).order_by('-id')
        return render(request,'software_training/training/trainer/trainer_viewtopic.html',{'mem':mem,'z':z})
    else:
        return redirect('/')

def trainer_team(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
    
        z = user_registration.objects.filter(id=tr_id)
        return render(request,'software_training/training/trainer/trainer_team.html',{'z':z})
    else:
        return redirect('/')

def trainer_currentteam(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
           tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id).filter(fullname=tr_fullname)
        tm = create_team.objects.filter(create_team_trainer=tr_fullname).filter(create_team_status=0).order_by('-id')
        return render(request,'software_training/training/trainer/trainer_current_team_list.html',{'z':z,'tm':tm})
    else:
        return redirect('/')
def attenperform(request,id):
    if request.method == 'POST':
        abc = create_team.objects.get(id=id)
        abc.create_team_progress = request.POST['sele']
        abc.save()
    return redirect('trainer_currentteam')

def trainer_currenttrainees(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        d = create_team.objects.get(id=id)
        des = designation.objects.get(designation_name='trainee')
        mem = user_registration.objects.filter(
            designation_id=des.id).filter(team_id=d).order_by('-id')
        return render(request,'software_training/training/trainer/trainer_current_trainees_list.html',{'z':z,'mem':mem})
    else:
        return redirect('/')

def trainer_currenttraineesdetails(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
    
        z = user_registration.objects.filter(id=tr_id)
        mem = user_registration.objects.get(id=id)
        tre = create_team.objects.get(id=mem.team.id)
        labels = []
        data = []
        queryset = user_registration.objects.filter(id=mem.id)
        for i in queryset:
            labels = [i.workperformance,i.attitude,i.creativity]
            data = [i.workperformance,i.attitude,i.creativity]
        return render(request,'software_training/training/trainer/trainer_current_tainees_details.html', {'mem': mem, 'tre': tre, 'z': z ,'labels': labels,'data': data,})
    else:
        return redirect('/')

def trainer_currentattentable(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        mem = user_registration.objects.get(id=id)
        if request.method == 'POST':
            std = request.POST['startdate']
            edd = request.POST['enddate']
            user=mem
            atten = attendance.objects.filter(attendance_date__gte=std,attendance_date__lte=edd,attendance_user=user).order_by('-id')
        return render(request,'software_training/training/trainer/trainer_current_atten_table.html',{'mem': mem, 'z': z,'atten':atten})
    else:
        return redirect('/')

def trainer_currentperform(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        mem = user_registration.objects.get(id=id)
        if request.method == 'POST':
            mem.attitude = request.POST['sele1']
            mem.creativity = request.POST['sele2']
            mem.workperformance = request.POST['sele3']
            mem.save()
            return render(request,'software_training/training/trainer/trainer_current_perform.html',{'mem': mem, 'z': z})
        return render(request,'software_training/training/trainer/trainer_current_perform.html',{'mem': mem, 'z': z})
    else:
        return redirect('/')

def trainer_currentattenadd(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
    
        z = user_registration.objects.filter(id=tr_id)
        mem = user_registration.objects.get(id=id)
        atten = attendance()
        if request.method == 'POST':
            atten.attendance_date = request.POST['date']
            atten.attendance_user  = mem
            atten.attendance_status = request.POST['pres']
            atten.save()
            return render(request,'software_training/training/trainer/trainer_current_atten_add.html',{'mem': mem, 'atten': atten, 'z': z})
        return render(request,'software_training/training/trainer/trainer_current_atten_add.html',{'mem': mem, 'z': z})
    else:
        return redirect('/')

def trainer_previousteam(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
           tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id).filter(fullname=tr_fullname)
        tm = create_team.objects.filter(create_team_trainer=tr_fullname).filter(create_team_status = 1).order_by('-id')
        return render(request,'software_training/training/trainer/trainer_previous_team_list.html',{'z':z,'tm':tm})
    else:
        return redirect('/')

def trainer_previoustrainees(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        d = create_team.objects.get(id=id)
        des = designation.objects.get(designation_name='trainee')
        mem = user_registration.objects.filter(designation_id=des.id).filter(team_id=d)
        return render(request,'software_training/training/trainer/trainer_previous_trainess_list.html',{'z':z,'mem':mem})
    else:
        return redirect('/')

def trainer_previoustraineesdetails(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        mem = user_registration.objects.get(id=id)
        tre = create_team.objects.get(id=mem.team_id)
        labels = []
        data = []
        queryset = user_registration.objects.filter(id=id)
        for i in queryset:
            labels = [i.workperformance,i.attitude,i.creativity]
            data = [i.workperformance,i.attitude,i.creativity]
        print(data)
        return render(request,'software_training/training/trainer/trainer_previous_trainees_details.html',{'mem': mem, 'tre': tre, 'z': z ,'labels': labels,'data': data,})
    else:
        return redirect('/')

def trainer_previousattentable(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        mem = user_registration.objects.get(id=id)
        att = attendance.objects.filter( attendance_user=mem.id).order_by('-id')
        return render(request,'software_training/training/trainer/trainer_previous_atten_table.html',{'z':z,'att':att})
    else:
        return redirect('/')

def trainer_previousperfomtable(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        num = user_registration.objects.get(id=id)
        return render(request,'software_training/training/trainer/trainer_previous_performtable.html',{'z':z,'num':num})
    else:
        return redirect('/')

def trainer_current_attendance(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        mem = user_registration.objects.get(id=id)
        return render(request,'software_training/training/trainer/trainer_current_attendance.html',{'z':z,'mem':mem})
    else:
        return redirect('/')


def trainer_Task(request) :
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        return render(request,'software_training/training/trainer/trainer_task.html',{'z' :z})
    else:
        return redirect('/')
    
def trainer_teamlist(request) :
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
            tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        tam = create_team.objects.filter(create_team_trainer=tr_fullname,create_team_status = 0).order_by('-id')
        des = designation.objects.get(designation_name='trainee')
        cut = user_registration.objects.filter(designation_id=des.id)
        return render(request,'software_training/training/trainer/trainer_teamlist.html',{'z' :z,'tam': tam, 'cut': cut})
    else:
        return redirect('/')

def trainer_taskpage(request,id) :
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
            tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        d = create_team.objects.get(id=id)
        return render(request, 'software_training/training/trainer/trainer_taskfor.html',{'d': d, 'z': z})
    else:
        return redirect('/')
    
def trainer_givetask(request,id) :
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
            tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        d = create_team.objects.get(id=id)
        des = designation.objects.get(designation_name='trainee')
        var = user_registration.objects.filter(team_id=d).filter(designation_id=des.id)
        if request.method == 'POST':
            list= request.POST.get('list')
            name = request.POST.get('taskname')
            desc = request.POST.get('description')
            files= request.FILES['files']
            start= request.POST.get('start')
            end = request.POST.get('end')
            task_status = 0
            team_name = id
            vars = trainer_task(trainer_task_user_id=list,trainer_task_taskname=name,trainer_task_description=desc,trainer_task_files=files,trainer_task_startdate=start,
                     trainer_task_enddate=end,trainer_task_status=task_status,trainer_task_team_name_id =team_name)
            vars.save()
            return render(request, 'software_training/training/trainer/trainer_givetask.html', {'z': z, 'var': var})
        else:
            return render(request,'software_training/training/trainer/trainer_givetask.html',{'z': z, 'var': var})
    else:
        return redirect('/')
    
def trainer_taskgivenpage(request,id) :
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
            tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        d = create_team.objects.get(id=id)
        c = trainer_task.objects.filter(trainer_task_team_name_id=d.id)
        des = designation.objects.get(designation_name='trainee')
        mem1 = user_registration.objects.filter(designation_id=des.id).filter(team_id=d).order_by('-id')
        mem = user_registration.objects.filter(designation_id=des.id).filter(team_id=d).values_list('id')
        tsk = trainer_task.objects.filter(trainer_task_team_name_id=d.id).filter(trainer_task_user__in=mem).order_by('-id')
        return render(request,'software_training/training/trainer/trainer_taskgiven.html',{'mem': mem,'mem1': mem1, 'tsk': tsk, 'z': z})
    else:
        return redirect('/')

def trainer_task_previous_teamlist(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
            tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id).filter(fullname=tr_fullname)
        tam = create_team.objects.filter(create_team_trainer=tr_fullname,create_team_status= 1).order_by('-id')
        des = designation.objects.get(designation_name='trainee')
        cut = user_registration.objects.filter(designation_id=des.id)
        return render(request, 'software_training/training/trainer/trainer_task_previous_teamlist.html',{'z': z, 'cut':cut, 'tam':tam})
    else:
        return redirect('/')
def trainer_task_previous_team_tasklist(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        tsk = trainer_task.objects.filter(trainer_task_team_name_id=id).order_by('-id')
        return render(request, 'software_training/training/trainer/trainer_task_previous_team_tasklist.html',{'z': z, 'tsk':tsk})
    else:
        return redirect('/')

def trainer_trainees(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
   
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
            tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        cut = create_team.objects.filter(create_team_trainer=tr_fullname).values_list('id',flat=True)
        print(cut)
        des = designation.objects.get(designation_name='trainee')
        user = user_registration.objects.filter(designation_id=des.id,team_id__in=cut)
        return render(request, 'software_training/training/trainer/trainer_current_trainees.html',{'z':z,'n': user})
    else:
        return redirect('/')
        
def trainer_traineesdetails(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
            tr_fullname = request.session['tr_fullname']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        mem = user_registration.objects.get(id=id)
        tre = create_team.objects.get(id=mem.team.id)
        labels = []
        data = []
        queryset = user_registration.objects.filter(id=mem.id)
        for i in queryset:
            labels = [i.workperformance,i.attitude,i.creativity]
            data = [i.workperformance,i.attitude,i.creativity]
        return render(request, 'software_training/training/trainer/trainer_traineesdetails.html',{'mem': mem, 'tre': tre, 'z': z ,'labels': labels,'data': data,})
    else:
        return redirect('/')

def trainer_current_attendance_view(request,id):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        else:
           tr_fullname = "dummy"
        z = user_registration.objects.filter(id=tr_id)
        mem = user_registration.objects.get(id=id)
        return render(request,'software_training/training/trainer/trainer_current_attendance_view.html',{'mem': mem, 'z': z})
    else:
        return redirect('/')

def trainer_paymentlist(request):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
            tr_fullname = request.session['tr_fullname']
        if request.session.has_key('tr_designation_id'):
            tr_designation_id = request.session['tr_designation_id']
        else:
            m_id = "dummy"
        z = user_registration.objects.filter(designation_id=tr_designation_id).filter(fullname=tr_fullname).filter(id=tr_id)
        acc=acntspayslip.objects.filter(acntspayslip_user_id=tr_id).all().order_by('-id')
        return render(request, 'software_training/training/trainer/trainer_paymentlist.html', {'acc': acc,'z':z})
    else:
        return redirect('/')

def trainer_payment_viewslip(request,id,tid):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
            tr_fullname = request.session['tr_fullname']
        if request.session.has_key('tr_designation_id'):
            tr_designation_id = request.session['tr_designation_id']
        else:
            m_id = "dummy"
        z= user_registration.objects.filter(designation_id=tr_designation_id).filter(fullname=tr_fullname).filter(id=tr_id)
        user = user_registration.objects.get(id=tid)
        acc = acntspayslip.objects.get(id=id)
        names = acntspayslip.objects.all()
        return render(request, 'software_training/training/trainer/trainer_payment_viewslip.html', {'z': z,'user':user,'acc':acc})
    else:
        return redirect('/')

def trainer_payment_print(request,id,tid):
    if 'tr_id' in request.session:
        if request.session.has_key('tr_id'):
            tr_id = request.session['tr_id']
        if request.session.has_key('tr_fullname'):
            tr_fullname = request.session['tr_fullname']
        if request.session.has_key('tr_designation_id'):
            tr_designation_id = request.session['tr_designation_id']
        else:
            m_id = "dummy"
        z = user_registration.objects.filter(designation_id=tr_designation_id).filter(fullname=tr_fullname).filter(id=tr_id)
        mem = user_registration.objects.filter(id=tr_id)   
        user = user_registration.objects.get(id=tid)
        acc = acntspayslip.objects.get(id=id)
        return render(request, 'software_training/training/trainer/trainer_payment_print.html', {'z': z,'user':user,'acc':acc,'mem': mem})
    else:
        return redirect('/')


def pdf(request,id,tid):
    date = datetime.now()   
    acc = acntspayslip.objects.get(id=id)
    user = user_registration.objects.get(id=tid)
    template_path = 'software_training/training/trainer/trainer_payment_pdf.html'
    context = {'acc': acc,'user':user,
    'media_url':settings.MEDIA_URL,
    'date':date
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] = 'filename="certificate.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#******************  Trainee  *****************************

def trainee_dashboard_trainee(request):
    if 'te_id' in request.session: 
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        z = user_registration.objects.filter(id=te_id)
        labels = []
        data = []
        queryset = user_registration.objects.filter(id=te_id)
        for i in queryset:
            labels=[i.workperformance,i.attitude,i.creativity]
            data=[i.workperformance,i.attitude,i.creativity]
        return render(request, 'software_training/training//trainee/trainee_dashboard_trainee.html',{'z': z ,'labels': labels,'data': data,})
    else:
        return redirect('/')
       
def trainee_task(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        return render(request,'software_training/training/trainee/trainee_task.html',{'z':z})   
    else:
        return redirect('/')

def trainee_task_list(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        mem=trainer_task.objects.filter(trainer_task_user=te_id,trainer_task_status = 0).all().order_by('-id')
        return render(request,'software_training/training/trainee/trainee_task_list.html',{'z':z,'mem':mem})
    else:
        return redirect('/')

def trainee_task_details(request,id):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        mem=trainer_task.objects.get(id=id)
        if request.method=="POST":
            mem.trainer_task_user_description=request.POST['description']
            mem.trainer_task_user_files=request.FILES['files']
            mem.trainer_task_submitteddate=datetime.now()
            mem.trainer_task_status=1
            mem.save()
            return redirect('trainee_task_list')
        return render(request,'software_training/training/trainee/trainee_task_details.html',{'z':z,'mem':mem})
    else:
        return redirect('/')

def trainee_completed_taskList(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        mem=trainer_task.objects.filter(trainer_task_user=te_id,trainer_task_status = 1).all().order_by('-id')
        return render(request,'software_training/training/trainee/trainee_completed_taskList.html',{'z':z,'mem':mem})
    else:
        return redirect('/')

def trainee_completed_details(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        return render(request,'software_training/training/trainee/trainee_completed_details.html',{'z':z})
    else:
        return redirect('/')

def trainee_topic(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        return render(request, 'software_training/training/trainee/trainee_topic.html',{'z':z})
    else:
        return redirect('/')

def trainee_currentTopic(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        if request.session.has_key('te_team_id'):
            te_team_id = request.session['te_team_id']         
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        mem=topic.objects.filter(topic_trainee=te_id,topic_team=te_team_id,topic_status = 0).all().order_by('-id')
        return render(request, 'software_training/training/trainee/trainee_currentTopic.html',{'z':z,'mem':mem})
    else:
        return redirect('/')  

def save_trainee_review(request,id):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        if request.session.has_key('te_team_id'):
            te_team_id = request.session['te_team_id']         
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        vars=topic.objects.get(id=id)
        vars.topic_review = request.POST.get('review')
        vars.topic_status = 1
        vars.save()
        return redirect('trainee_currentTopic')
    else:
        return redirect('/')  

def trainee_previousTopic(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        if request.session.has_key('te_team_id'):
            te_team_id = request.session['te_team_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        mem=topic.objects.filter(topic_trainee=te_id,topic_team=te_team_id,topic_status = 1).all().order_by('-id')
        return render(request, 'software_training/training/trainee/trainee_previousTopic.html',{'z':z,'mem':mem})
    else:
        return redirect('/')
def trainee_reported_issue(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        mem=reported_issue.objects.filter(reported_issue_reporter=te_id).all().order_by('-id')    
        return render(request, 'software_training/training/trainee/trainee_reported_issue.html',{'z':z,'mem':mem})
    else:
        return redirect('/')

def trainee_report_reported(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        if request.session.has_key('te_designation_id'):
            te_designation_id = request.session['te_designation_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(designation_id=te_designation_id).filter(id=te_id)
        var = reported_issue()
        if request.method == 'POST':
            var.reported_issue_designation_id=designation.objects.get(id=te_designation_id)
            var.reported_issue_reported_to  = user_registration.objects.get(id=int(request.POST['reportto']))
            var.reported_issue_issue = request.POST['report']
            var.reported_issue_reporter  = user_registration.objects.get(id=te_id)
            var.reported_issue_reported_date = datetime.now()
            var.reported_issue_issuestatus=0
            var.save()
        return render(request, 'software_training/training/trainee/trainee_report_reported.html',{'z':z})
    else:
        return redirect('/')

def trainee_report_issue(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        des = designation.objects.get(designation_name='manager')
        mem = user_registration.objects.filter(designation_id=des.id)
        des1 = designation.objects.get(designation_name='trainer')
        mem1= user_registration.objects.filter(designation_id=des1.id)
        return render(request, 'software_training/training/trainee/trainee_report_issue.html',{'z':z,'mem':mem,'mem1':mem1})
    else:
        return redirect('/')

def trainee_applyleave_form(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        mem = user_registration.objects.all()
        des=designation.objects.get(designation_name="trainee")
        z=user_registration.objects.filter(designation_id=des.id)
        user=user_registration.objects.get(id=te_id)
        le=leave()
        if request.method=="POST":
            le.leave_from_date=request.POST['from']
            le.leave_to_date=request.POST['to']
            le.leave_reason=request.POST['reason']
            le.leave_leave_status =request.POST['haful']
            le.leave_leaveapproved_status=0
            le.leave_designation_id=des.id
            le.leave_user=user
            le.save()
            return redirect('trainee_applyleave_card')
        return render(request, 'software_training/training/trainee/trainee_applyleave_form.html',{'mem': mem,'z':z}) 
    else:
        return redirect('/')
    
def trainee_applyleave_card(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        mem = user_registration.objects.all()
        des=designation.objects.get(designation_name="trainee")
        z=user_registration.objects.filter(designation_id=des.id)
        return render(request, 'software_training/training/trainee/trainee_applyleave_cards.html',{'mem':mem,'z':z})
    else:
        return redirect('/')
    
def trainee_appliedleave(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        des=designation.objects.get(designation_name="trainee")
        le=leave.objects.filter(leave_designation_id=des.id ,leave_user=te_id).all().order_by('-id')
        return render(request, 'software_training/training/trainee/trainee_appliedleave.html',{'z':z,'le':le})
    else:
        return redirect('/')

def Attendance(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        return render(request,'software_training/training/trainee/trainees_attendance.html',{'z':z})
    else:
        return redirect('/')

def trainees_attendance_viewattendance(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        return render(request,'software_training/training/trainee/trainees_attendance_viewattendance.html',{'z':z})
    else:
        return redirect('/')

def trainees_attendance_viewattendancelist(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        if request.method == 'POST':
            std = request.POST['startdate']
            edd = request.POST['enddate']
            user=te_id
            atten = attendance.objects.filter(attendance_date__gte=std,attendance_date__lte=edd,attendance_user_id=user)
        return render(request,'software_training/training/trainee/trainees_attendance_viewattendancelist.html',{'z':z,'atten':atten})
    else:
        return redirect('/')

def trainee_payment(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        return render(request,'software_training/training/trainee/trainee_payment.html',{'z':z})
    else:
        return redirect('/')
   
def trainee_payment_addpayment(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        pay=paymentlist()
        if request.method=="POST":
            pay.paymentlist_user_id = user_registration.objects.get(id=te_id)
            pay.paymentlist_amount_pay = request.POST['amount']
            pay.paymentlist_amount_date = request.POST['paymentdate']
            pay.paymentlist_current_date = datetime.now()
            pay.paymentlist_amount_downlod = request.FILES['files']
            pay.paymentlist_amount_status = 0 
            member = user_registration.objects.get(id=te_id)
            co = course.objects.get(id = member.course_id)
            member.total_pay=int(request.POST['amount'])+member.total_pay
            member.payment_balance = co.course_total_fee - member.total_pay
            member.save()
            pay.save()
            return redirect('trainee_payment')

        return render(request,'software_training/training/trainee/trainee_payment_addpayment.html',{'z':z})
    else:
        return redirect('/')
def trainee_payment_viewpayment(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        mem=paymentlist.objects.filter(paymentlist_user_id = te_id).order_by('-id')
        return render(request,'software_training/training/trainee/trainee_payment_viewpayment.html',{'z':z,'mem':mem})
    else:
        return redirect('/')

def trainee_logout(request):
    if 'te_id' in request.session:  
        request.session.flush()
        return redirect('Tlogin')
    else:
        return redirect('Tlogin') 

def trainees_account(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        return render(request,'software_training/training/trainee/trainees_account.html',{'z':z})
    else:
        return redirect('/')

def imagechange_trainees(request,id):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)     
        mem=user_registration.objects.get(id=id)
        if request.method=="POST":
            mem.photo = request.FILES['filenamees']
            mem.save()
            return redirect('trainees_account')
    else:
        return redirect('/')

def trainees_chpasswd(request):
    if 'te_id' in request.session:
        if request.session.has_key('te_id'):
            te_id = request.session['te_id']
        else:
            te_id = "dummy"
        z=user_registration.objects.filter(id=te_id)
        if request.method == 'POST':
            abc = user_registration.objects.get(id=te_id)   
            oldps = request.POST['currentPassword']
            newps = request.POST['newPassword']
            cmps = request.POST.get('confirmPassword')
            if oldps != newps:
                if newps == cmps:
                    abc.password = request.POST.get('confirmPassword')
                    abc.save()
                    return redirect('trainee_dashboard_trainee')
            elif oldps == newps:
                messages.add_message(request, messages.INFO, 'Current and New password same')
            else:
                messages.info(request, 'Incorrect password same')                
            return render(request, 'software_training/training/trainee/trainees_chpasswd.html', {'z': z})   
        return render(request, 'software_training/training/trainee/trainees_chpasswd.html', {'z': z})
    else:
        return redirect('/')


#****************************  Admin- view  ********************************
def Admin_Dashboard(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    vars = user_registration.objects.all().exclude(designation_id=z.id)
    c = course.objects.all()
    return render(request, 'software_training/training/admin/admin_Dashboard.html', {'mem': mem, 'var':var, 'vars':vars,'c':c, })

def Admin_categories(request):
    mem = User.objects.all()
    c = category.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_categories.html', {'mem': mem,'var':var,'c':c,}) 

def Admin_emp_categories(request):
    mem = User.objects.all()
    c = category.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_emp_categories.html', {'mem': mem,'var':var,'c':c,})  

def Admin_courses(request,id):
    mem = User.objects.all()
    c = course.objects.filter(course_category_id=id)
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_courses.html', {'mem': mem,'var':var,'c':c,})

def Admin_emp_course_list(request,id):
    mem = User.objects.all()
    c = course.objects.filter(course_category_id=id)
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_emp_course_list.html', {'mem': mem,'var':var,'c':c,})

def Admin_emp_course_details(request,id):
    mem = User.objects.all()
    c = user_registration.objects.filter(course_id=id)
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_emp_course_details.html', {'mem': mem,'var':var,'c':c})

def Admin_emp_profile(request,id):
    mem = User.objects.all()
    c = user_registration.objects.get(id=id)
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    labels = []
    data = []
    queryset = user_registration.objects.filter(id=c.id)
    for i in queryset:
        labels=[i.workperformance,i.attitude,i.creativity]
        data=[i.workperformance,i.attitude,i.creativity]
    return render(request,'software_training/training/admin/admin_emp_profile.html', {'mem': mem,'var':var,'c':c,'labels':labels,'data':data})

def Admin_emp_attendance(request,id):
    mem = User.objects.all()
    c = user_registration.objects.get(id=id)
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_emp_attendance.html', {'mem': mem,'var':var,'c':c,})

def Admin_emp_attendance_show(request,id):
    mem = User.objects.all()
    c = attendance.objects.filter(attendance_user_id=id)
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_emp_attendance_show.html', {'mem': mem,'var':var,'c':c,})

def Admin_task(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_task.html', {'mem': mem,'var':var,})


def Admin_givetask(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)

    if request.method == 'POST':
        sc1 = request.POST['Department']
        sc2 = request.POST['designation']
        sc3 = request.POST['projectname']
        sc4 = request.POST['task']
        sc7 = request.POST['discrip']
        sc5 = request.POST['start']
        sc6 = request.POST['end']
        ogo = request.FILES['img[]']
        print(sc4)
        
        catry = trainer_task(tasks=sc4,files=ogo,description=sc7,
                                  startdate=sc5, enddate=sc6,department_id = sc1,designation_id = sc2,user_id = sc3)
        catry.save()
    cate = category.objects.all()
    desig = designation.objects.all()
    proj = course.objects.all()
    emp = user_registration.objects.all()
    return render(request,'software_training/training/admin/admin_givetask.html', {'mem': mem,'var':var,'cate':cate,'desig':desig,'proj':proj,'emp':emp,})


def Admin_taskcategory(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)  

 
    Adm = user_registration.objects.filter(id=z.id) 
    dept_id = request.GET.get('dept_id')
    # Desig = designation.objects.filter(department_id=dept_id)
    Desig = course.objects.all()
    print("jishnu")
    return render(request,'software_training/training/admin/admin_taskcategory.html', {'Desig': Desig,'Adm':Adm,'mem':mem,'var':var,})

def Admin_current_task(request):
    mem = User.objects.all()
    c = trainer_task.objects.filter(trainer_task_status = 0).order_by('-id')
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id,)
    return render(request,'software_training/training/admin/admin_current_task.html', {'mem': mem,'var':var,'c':c,})

def Admin_previous_task(request):
    mem = User.objects.all()
    c = trainer_task.objects.filter(trainer_task_status = 1).order_by('-id')
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_previous_task.html', {'mem': mem,'var':var,'c':c,})

def Admin_registration_details(request):
    mem = User.objects.all()
    vars = user_registration.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_registration_details.html', {'mem': mem,'vars':vars,'var':var,})
def teamdelete(request,id):
    var = user_registration.objects.get(id=id)
    var.delete()
    return redirect("Admin_registration_details")  

def Admin_attendance(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_attendance.html', {'mem': mem,'var':var,}) 

def Admin_attendance_show(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_attendance_show.html', {'mem': mem,'var':var,})

def Admin_reported_issues(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_reported_issues.html', {'mem': mem,'var':var,}) 

def Admin_emp_reported_detail(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_emp_reported_detail.html', {'mem': mem,'var':var,})

def Admin_emp_reported_issue_show(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_emp_reported_issue_show.html', {'mem': mem,'var':var,})

def Admin_manager_reported_detail(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_manager_reported_detail.html', {'mem': mem,'var':var,})

def Admin_manager_reported_issue_show(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_manager_reported_issue_show.html', {'mem': mem,'var':var,})

def Admin_add(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_add.html', {'mem': mem,'var':var,}) 

def Admin_addcategories(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_addcategories.html', {'mem': mem,'var':var,}) 

def Admin_categorieslist(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_categorieslist.html', {'mem': mem,'var':var,}) 

def Admin_addcourse(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_addcourse.html', {'mem': mem,'var':var,}) 

def Admin_addnewcourse(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_addnewcourse.html', {'mem': mem,'var':var,}) 

def Admin_addnewcategories(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_addnewcategories.html', {'mem': mem,'var':var,}) 

def Admin_courselist(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_courselist.html', {'mem': mem,'var':var,}) 

def Admin_coursedetails(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    return render(request,'software_training/training/admin/admin_coursedetails.html', {'mem': mem,'var':var,}) 

def Admin_account_trainer(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    
    return render(request, 'software_training/training/admin/admin_account_trainer.html',{'mem': mem,'var':var,})

def imagechange(request,id):
    
    if request.method == 'POST':
        # id = request.GET.get('id')
        abc = user_registration.objects.get(id=id)
        abc.photo = request.FILES['filenamees']
        abc.save()
        return redirect('Admin_account_trainer')
    return render(request, 'software_training/training/admin/admin_account_trainer.html' )


def Admin_changepassword(request):
    mem = User.objects.all()
    z = designation.objects.get(designation_name='Admin')
    var = user_registration.objects.filter(designation_id=z.id)
    if request.method == 'POST':
        abc = user_registration.objects.get(id=z.id)
        oldps = request.POST['currentPassword']
        newps = request.POST['newPassword']
        cmps = request.POST.get('confirmPassword')
        if oldps != newps:
            if newps == cmps:
                abc.password = request.POST.get('confirmPassword')
                abc.save()
                return render(request, 'software_training/training/admin/admin_Dashboard.html', {'z': z})
    
            elif oldps == newps:
                messages.add_message(request, messages.INFO, 'Current and New password same')
        else:
            messages.info(request, 'Incorrect password same')
    
        return render(request, 'software_training/training/admin/admin_changepassword.html', {'mem': mem,'var':var,'z': z})
    
    return render(request, 'software_training/training/admin/admin_changepassword.html', {'mem': mem,'var':var,'z': z})

#******************accounts****************

def accounts_Dashboard(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
    
        return render(request, 'software_training/training/account/accounts_Dashboard.html',{'mem':mem})
    else:
        return redirect('/')

def logout5(request):
    if 'acc_id' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/') 

def account_accounts(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id= acc_id)
        return render(request, 'software_training/training/account/account_accounts.html', {'mem': mem})
    else:
        return redirect('/')

def imagechange_accounts(request): 
    if 'acc_id' in request.session:
        if request.method == 'POST':
            id = request.GET.get('id')
            abc = user_registration.objects.get(id=id)
            abc.photo = request.FILES['filenamees']
            abc.save()
            return redirect('account_accounts')
        return render(request, 'software_training/training/account/account_accounts.html')
    else:
        return redirect('/')

def changepassword_accounts(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_fullname'):
            acc_fullname = request.session['acc_fullname']
        if request.session.has_key('acc_designation_id'):
            acc_designation_id = request.session['acc_designation_id']
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        else:
            acc_fullname = "dummy"
        mem = user_registration.objects.filter(designation_id=acc_designation_id,id=acc_id).filter(fullname=acc_fullname)

        # mem = user_registration.objects.filter(id=acc_id)
    
        if request.method == 'POST':
            abc = user_registration.objects.get(id=acc_id)
    
            oldps = request.POST['currentPassword']
            newps = request.POST['newPassword']
            cmps = request.POST.get('confirmPassword')
            if oldps != newps:
                if newps == cmps:
                    abc.password = request.POST.get('confirmPassword')
                    abc.save()
                    return render(request, 'software_training/training/account/changepassword_accounts.html', {'mem': mem,})
            elif oldps == newps:
                messages.add_message(request, messages.INFO, 'Current and New password same')
            else:
                messages.info(request, 'Incorrect password same')
    
            return render(request, 'software_training/training/account/changepassword_accounts.html', {'mem': mem,})
    
        return render(request, 'software_training/training/account/changepassword_accounts.html', {'mem': mem,})

    else:
        return redirect('/')   


def accounts_registration_details(request):

    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']

        mem = user_registration.objects.filter(id=acc_id)
        des = designation.objects.get(designation_name='trainee')
        deta = user_registration.objects.filter(designation_id = des.id)
        vars = paymentlist.objects.all()
        return render(request,'software_training/training/account/accounts_registration_details.html', { 'mem' : mem, 'deta':deta , 'vars':vars})
    else:
        return redirect('/')
    
def accounts_payment_detail_list(request, id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        a = user_registration.objects.get(id=id)
        c = course.objects.get(id=a.course_id)  
        pay = paymentlist.objects.filter(paymentlist_user_id = a.id).order_by('-id') 
        return render(request,'software_training/training/account/accounts_payment_detail_list.html',{ 'mem' : mem, 'pay': pay , 'a':a , 'c':c})
    else:
        return redirect('/')

def verify(request,id):
    rem = paymentlist.objects.get(id=id)
    rem.paymentlist_amount_status = 1
    rem.save()
    return redirect('/softwareapp/accounts_registration_details')
    
def reminder(request,id):
    rem = user_registration.objects.get(id=id)
    rem.payment_status = 1
    rem.save()
    return redirect('/softwareapp/accounts_registration_details')
    
def accounts_payment_salary(request,id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        vars=user_registration.objects.get(id=id)
        if request.method == "POST":
            abc = acntspayslip()
            abc.acntspayslip_basic_salary = request.POST["salary"] 
            abc.acntspayslip_hra = request.POST["hra"] 
            abc.acntspayslip_conveyns = request.POST["ca"] 
            abc.acntspayslip_pf_tax = request.POST["pt"] 
            abc.acntspayslip_incentives = request.POST["ins"] 
            abc.acntspayslip_delay = request.POST["delay"] 
            abc.acntspayslip_leavesno= request.POST["leave"] 
            abc.acntspayslip_fromdate= request.POST["efdate"] 
            abc.acntspayslip_tax = 0
            abc.acntspayslip_pf = 0 
            abc.acntspayslip_incometax = 0 
            abc.acntspayslip_basictype = request.POST["basictype"] 
            abc.acntspayslip_hratype = request.POST["hratype"] 
            abc.acntspayslip_contype = request.POST["contype"] 
            abc.acntspayslip_protype = request.POST["protype"]
            abc.acntspayslip_instype = request.POST["instype"]
            abc.acntspayslip_deltype = request.POST["deltype"]
            abc.acntspayslip_leatype = request.POST["leatype"] 

            abc.acntspayslip_user_id = user_registration.objects.get(id=id)
            print(vars.designation.id)
            # abc.acntspayslip_designation = vars.designation.id 
            print(abc.acntspayslip_designation)
            abc.save()
        return render(request, 'software_training/training/account/accounts_payment_salary.html',{'vars':vars,'mem' : mem})
    else:
        return redirect('/')
    
def accounts_payment_view(request, id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        reg =user_registration.objects.get(id=id)
        use =acntspayslip.objects.filter(acntspayslip_user_id=id)
        return render(request, 'software_training/training/account/accounts_payment_view.html',{'mem':mem, 'use':use, 'reg':reg})
    else:
        redirect('/')


def accounts_report(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        return render(request,'software_training/training/account/account_report.html',{'mem':mem})
    else:
        return redirect('/')

def accounts_report_issue(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']

        if request.session.has_key('acc_designation_id'):
            acc_designation_id = request.session['acc_designation_id']

        mem = user_registration.objects.filter(id=acc_id)
        des = designation.objects.get(designation_name = 'manager')
        #cut = user_registration.objects.get(designation_id=des.id)
        vars = reported_issue()
        if request.method == 'POST':
            vars.reported_issue_issue=request.POST['issue']
            vars.reported_issue_reporter = user_registration.objects.get(id=acc_id)
            vars.reported_issue_reported_date=datetime.now()
            vars.reported_issue_issuestatus=0
            vars. reported_issue_designation_id = designation.objects.get(id=acc_designation_id)
            vars.reported_issue_reported_to= user_registration.objects.get(designation_id=des.id)
            vars.save()
            return redirect('/softwareapp/accounts_report')
        return render(request, 'software_training/training/account/account_report_issue.html',{'mem':mem})
    else:
        redirect('/')   

def accounts_reported_issue(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        n = reported_issue.objects.filter(reported_issue_reporter=acc_id).order_by('-id')
        return render(request, 'software_training/training/account/account_reported_issue.html',{'mem':mem, 'n':n})
    else:
        redirect('/')





def accounts_emp_dep(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
       # mem1 = course.objects.get(id=id)
        des=designation.objects.all().exclude(designation_name = 'trainee')
        context = {'des':des,'mem' : mem}
        return render(request, 'software_training/training/account/accounts_emp_dep.html', context)
    else:
        return redirect('/')
    
def accounts_emp_list(request, id): 
    if 'acc_id' in request.session: 
        if request.session.has_key('acc_id'): 
            acc_id = request.session['acc_id'] 
        mem = user_registration.objects.filter(id=acc_id)   
        mem2 = designation.objects.get(id=id)
        
        use = user_registration.objects.filter(designation=mem2) 
        context = {'use':use,'mem' : mem} 
        return render(request, 'software_training/training/account/accounts_emp_list.html', context) 
    else: 
        return redirect('/') 
    
def accounts_emp_details(request, id): 
    if 'acc_id' in request.session: 
        if request.session.has_key('acc_id'): 
            acc_id = request.session['acc_id'] 
        mem = user_registration.objects.filter(id=acc_id)   
        vars=user_registration.objects.get(id=id) 
        context = {'vars':vars,'mem' : mem} 
        return render(request, 'software_training/training/account/accounts_emp_details.html', context) 
    else:
        return redirect('/') 
    

def accounts_add_bank_acnt(request, id):
    if 'acc_id' in request.session:  
        if request.session.has_key('acc_id'):  
            acc_id = request.session['acc_id']  
        mem = user_registration.objects.filter(id=acc_id) 
        mem1 = user_registration.objects.filter(id=id) 
        if request.method == 'POST': 
            vars = user_registration.objects.get(id=id) 
            vars.account_no = request.POST['account_no'] 
            vars.ifsc = request.POST['ifsc'] 
            vars.bank_branch = request.POST['bank_branch'] 
            vars.bank_name= request.POST['bank_name'] 
            vars.save() 
        return render(request, 'software_training/training/account/accounts_add_bank_acnt.html',{'mem':mem, 'mem1':mem1})
    else:
        return redirect('/')

def accounts_bank_acnt_details(request):
    return render(request, 'software_training/training/account/accounts_bank_acnt_details.html')

def accounts_salary_details(request, id):
    if 'acc_id' in request.session:  
        if request.session.has_key('acc_id'):  
            acc_id = request.session['acc_id']  
        mem = user_registration.objects.filter(id=acc_id) 
        mem1=user_registration.objects.filter(id=id)
        usk=acntspayslip.objects.filter(acntspayslip_user_id =id)
        return render(request, 'software_training/training/account/accounts_salary_details.html',{ 'mem1':mem1,'usk':usk,'mem': mem})
    else:
        return redirect('/')

def accounts_expenses(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        vars=acntexpensest.objects.all()
        return render(request, 'software_training/training/account/accounts_expenses.html',{'mem':mem, 'vars':vars})
    else:
        return redirect('/')
 
def accounts_expenses_viewEdit(request, id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        var=acntexpensest.objects.filter(id=id)
        return render(request, 'software_training/training/account/accounts_expenses_viewEdit.html',{'mem':mem, 'var':var})
    else:
        return redirect('/')
    

def accounts_expenses_viewEdit_Update(request, id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        emps = acntexpensest.objects.get(id=id)
        if request.method == 'POST':            
            emps.acntexpensest_payee = request.POST['payee']
            emps.acntexpensest_payacnt = request.POST['payacnt']
            emps.acntexpensest_paymethod = request.POST['paymod']
            emps.acntexpensest_paydate = request.POST['paydt']
            emps.acntexpensest_category = request.POST['category']
            emps.acntexpensest_description = request.POST['description']
            emps.acntexpensest_refno = request.POST['ref']
            emps.acntexpensest_amount = request.POST['amount']
            emps.acntexpensest_tax = request.POST['tax']
            emps.acntexpensest_total = request.POST['total']                
            emps.save() 
            return redirect('/softwareapp/accounts_expenses')
        return render(request,'software_training/training/account/accounts_expenses_viewEdit.html',{'mem':mem})
    else:
        return redirect('/')
    

def accounts_expense_newTransaction(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        mem1=acntexpensest()
        if request.method == 'POST':
            mem1.acntexpensest_payee = request.POST['payee']
            mem1.acntexpensest_payacnt = request.POST['payacnt']
            mem1.acntexpensest_paymethod = request.POST['paymod']
            mem1.acntexpensest_paydate = request.POST['paydt']
            mem1.acntexpensest_category = request.POST['category']
            mem1.acntexpensest_description = request.POST['description']
            mem1.acntexpensest_refno = request.POST['ref']
            mem1.acntexpensest_amount = request.POST['amount']
            mem1.acntexpensest_tax = request.POST['tax']
            mem1.acntexpensest_total = request.POST['total']                
            mem1.save()
            return redirect('/softwareapp/accounts_expenses')
        else:
            return render(request, 'software_training/training/account/accounts_expense_newTransaction.html',{'mem':mem})
    else:
        return redirect('/')
  

  
def accounts_payment_dep(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        des = designation.objects.all().exclude(designation_name = 'trainee')
        context = {'des':des,'mem' : mem}
        return render(request, 'software_training/training/account/accounts_payment_dep.html',context)
    else:
        return redirect('/')

def accounts_payment_list(request,id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)
        
        mem1 = designation.objects.get(id=id)
        use=user_registration.objects.filter(designation=mem1)
        context = {'use':use, 'mem':mem}
        return render(request,'software_training/training/account/accounts_payment_list.html',context)
    else:
        return redirect('/')

def account_payment_details(request, id):
    if 'acc_id' in request.session: 
        if request.session.has_key('acc_id'):  
            acc_id = request.session['acc_id'] 
        mem = user_registration.objects.filter(id=acc_id)
        vars = user_registration.objects.get(id=id) 
        context = {'vars':vars,'mem' : mem} 
        return render(request, 'software_training/training/account/account_payment_details.html', context) 
    else:
        return redirect('/')

def accounts_payment_details(request, id):
    if 'acc_id' in request.session: 
        if request.session.has_key('acc_id'):  
            acc_id = request.session['acc_id'] 
        mem = user_registration.objects.filter(id=acc_id)
        vars = user_registration.objects.get(id=id) 
        context = {'vars':vars,'mem' : mem} 
        return render(request, 'software_training/training/account/accounts_payment_details.html', context) 
    else:
        return redirect('/')
    
def accounts_payslip(request):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)   
        des = designation.objects.all()
        return render(request, 'software_training/training/account/accounts_payslip.html', {'des':des,'mem':mem})      
    else:
        return redirect('/')


def accounts_acntpay(request):
    if 'acc_id' in request.session:
        fdate = request.POST['fdate']
        tdate = request.POST['tdate']
        desig_id = int(request.POST['desi'])  
        names = acntspayslip.objects.filter(acntspayslip_fromdate__range=(fdate,tdate),acntspayslip_designation= desig_id).values('acntspayslip_user_id__fullname','acntspayslip_eno', 'acntspayslip_user_id__account_no', 'acntspayslip_user_id__bank_name', 'acntspayslip_user_id__bank_branch','acntspayslip_user_id__id', 'acntspayslip_user_id__email')  
        print(fdate)
        print(tdate)
      
        print(desig_id)
        print(names)
        return render(request, 'software_training/training/account/accounts_acntpay.html')
    else:
        return redirect('/')
    
def accounts_paydetails(request,id):
     if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)  
        user = user_registration.objects.get(id=id)
        acc = acntspayslip.objects.get(user_id=id)
        names = acntspayslip.objects.all()
        return render(request, 'software_training/training/account/accounts_paydetails.html',{'acc':acc, 'user':user,'names':names, 'mem': mem})

def accounts_print(request,id):
    if 'acc_id' in request.session:
        if request.session.has_key('acc_id'):
            acc_id = request.session['acc_id']
        mem = user_registration.objects.filter(id=acc_id)  
        user = user_registration.objects.get(id=id)
        acc = acntspayslip.objects.get(user_id=id)
        return render(request, 'software_training/training/account/accounts_print.html',{'mem':mem, 'acc':acc, 'user':user,})
    else:
        return redirect('/')