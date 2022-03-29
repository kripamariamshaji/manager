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

# Create your views here.

def login(request):
    Adm1 = designation.objects.get(designation_name="Admin")
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

        elif user_registration.objects.filter(email=request.POST['email'], password=request.POST['password'], designation_id=Adm1.id).exists():
                member = user_registration.objects.get(
                email=request.POST['email'], password=request.POST['password'])
                request.session['a_designation_id'] = member.designation_id
                request.session['a_fullname'] = member.fullname
                request.session['a_id'] = member.id
                return render(request, 'software_training/training/admin/Admin_Dashboard.html', {'member': member})
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
        return redirect('login')
    else:
        return redirect('login') 

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
        
        labels = []
        data = []
        queryset = user_registration.objects.filter(id=m_id)
        for i in queryset:
            labels=[i.workperformance,i.attitude,i.creativity]
            data=[i.workperformance,i.attitude,i.creativity]
        return render(request, 'software_training/training/manager/manager_Dashboard.html', {'mem': mem ,'labels': labels,'data': data,})
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
        return render(request,'software_training/training/manager/manager_trainer.html')
    
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

    return redirect('login')

def manager_current_team(request):
    return render(request,'software_training/training/manager/manager_current_team.html')

def Manager_current_task(request):
    return render(request,'software_training/training/manager/manager_current_task.html')

def manager_current_assigned(request):
    return render(request,'software_training/training/manager/manager_current_assigned.html')

def manager_current_trainees(request):
    return render(request,'software_training/training/manager/manager_current_trainees.html')

def manager_current_empdetails(request):
    return render(request,'software_training/training/manager/manager_current_empdetails.html')

def manager_current_attendance(request):
    return render(request,'software_training/training/manager/manager_current_attendance.html')

def manager_current_attendance_list(request):
    return render(request,'software_training/training/manager/manager_current_attendance_list.html')

def manager_current_task_list(request):
    return render(request,'software_training/training/manager/manager_current_task_list.html')

def manager_current_task_details(request):
    return render(request,'software_training/training/manager/manager_current_task_details.html')
    
def manager_previous_team(request):
    return render(request,'software_training/training/manager/manager_previous_team.html')

def Manager_previous_task(request):
    return render(request,'software_training/training/manager/Manager_previous_task.html')

def manager_previous_assigned(request):
    return render(request,'software_training/training/manager/manager_previous_assigned.html')

def manager_previous_trainees(request):
    return render(request,'software_training/training/manager/manager_previous_trainees.html')

def manager_previous_empdetails(request):
    return render(request,'software_training/training/manager/manager_previous_empdetails.html')

def manager_previous_attendance(request):
    return render(request,'software_training/training/manager/manager_previous_attendance.html')

def manager_previous_attendance_list(request):
    return render(request,'software_training/training/manager/manager_previous_attendance_list.html')

def manager_previous_task_list(request):
    return render(request,'software_training/training/manager/manager_previous_task_list.html')

def manager_previous_task_details(request):
    return render(request,'software_training/training/manager/manager_previous_task_details.html')

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
       
        cut = reported_issue.objects.filter(reported_issue_reported_to_id=m_id,reported_issue_designation_id_id=des.id,reported_issue_issuestatus=0)
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
        cut = reported_issue.objects.filter(reported_issue_reported_to_id=m_id).filter(reported_issue_designation_id_id=des.id).filter(reported_issue_issuestatus=1)
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
        cut = reported_issue.objects.filter(reported_issue_reported_to_id=m_id).filter(reported_issue_designation_id_id=des.id).filter(reported_issue_issuestatus=0)
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
        cut = reported_issue.objects.filter(reported_issue_reported_to_id=m_id).filter(reported_issue_designation_id_id=des.id).filter(reported_issue_issuestatus=1)
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
        des = designation.objects.get(designation_name='manager')
        des1 = designation.objects.get(designation_name='trainingmanager')
        ree = user_registration.objects.get(designation_id=des.id)
        if request.method == 'POST':
            vars = reported_issue()
            vars.issue = request.POST['issue']
            vars.issuestatus = 0
            vars.reporter_id = usernametm2
            vars.designation_id = des1.id
            vars.reported_to = ree
            vars.reported_date = datetime.now()
            vars.save()
            return redirect('reportedissue')
        return render(request, 'reportissue.html', {'mem': mem})
    else:
        return redirect('/')
    return render(request,'software_training/training/manager/manager_report_issue.html')

def manager_reported_issue(request):
    return render(request,'software_training/training/manager/manager_reported_issue.html')

def Manager_attendance(request):
    return render(request,'software_training/training/manager/manager_attendance.html') 

def manager_trainee_attendance(request):
    return render(request,'software_training/training/manager/manager_trainee_attendance.html') 

def manager_trainer_attendance(request):
    return render(request,'software_training/training/manager/manager_trainer_attendance.html') 

def manager_trainer_attendance_table(request):
    return render(request,'software_training/training/manager/manager_trainer_attendance_table.html') 

def manager_trainee_attendance_table(request):
    return render(request,'software_training/training/manager/manager_trainee_attendance_table.html') 

def manager_applyleave(request):
    return render(request,'software_training/training/manager/manager_applyleave.html') 

def manager_applyleavsub(request):
    return render(request,'software_training/training/manager/manager_applyleavsub.html')

def manager_requestedleave(request):
    return render(request,'software_training/training/manager/manager_requestedleave.html')

def manager_trainer_leave(request):
    return render(request,'software_training/training/manager/manager_trainer_leave.html')

def manager_trainers_leavelist(request):
    return render(request,'software_training/training/manager/manager_trainers_leavelist.html')

def manager_trainer_leavestatus(request):
    return render(request,'software_training/training/manager/manager_trainer_leavestatus.html')

def manager_trainee_leave(request):
    return render(request,'software_training/training/manager/manager_trainee_leave.html')

def manager_trainee_leavelist(request):
    return render(request,'software_training/training/manager/manager_trainee_leavelist.html')

def manager_trainee_leavestatus(request):
    return render(request,'software_training/training/manager/manager_trainee_leavestatus.html')

def manager_new_team(request):
    return render(request,'software_training/training/manager/manager_new_team.html')

def manager_new_teamcreate(request):
    return render(request,'software_training/training/manager/manager_new_teamcreate.html')

def manager_newtrainees(request):
    return render(request,'software_training/training/manager/manager_newtrainees.html')

    
#******************Trainer*****************************

def trainer_dashboard(request):
    return render(request,'software_training/training/trainer/trainer_dashboard.html')

def trainer_applyleave(request):
    return render(request, 'software_training/training/trainer/trainer_applyleave.html')

def trainer_applyleave_form(request):
    return render(request, 'software_training/training/trainer/trainer_applyleave_form.html')

def trainer_traineesleave_table(request):
    return render(request, 'software_training/training/trainer/trainer_traineesleave_table.html')

def trainer_reportissue(request):
    return render(request, 'software_training/training/trainer/trainer_reportissue.html')

def trainer_reportissue_form(request):
    return render(request, 'software_training/training/trainer/trainer_reportissue_form.html')

def trainer_reportedissue_table(request):
    return render(request, 'software_training/training/trainer/trainer_reportedissue_table.html')

def trainer_topic(request):
    return render(request,'software_training/training/trainer/trainer_topic.html')

def trainer_addtopic(request):
    return render(request,'software_training/training/trainer/trainer_addtopic.html')

def trainer_viewtopic(request):
    return render(request,'software_training/training/trainer/trainer_viewtopic.html')

def trainer_attendance(request):
    return render(request,'software_training/training/trainer/trainer_attendance.html')

def trainer_attendance_trainees(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainees.html')

def trainer_attendance_trainer(request):
    return render(request, 'software_training/training/trainer/trainer_attendance_trainer.html')

def trainer_attendance_trainer_viewattendance(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainer_viewattendance.html')

def trainer_attendance_trainer_viewattendancelist(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainer_viewattendancelist.html')

def trainer_team(request):
    return render(request,'software_training/training/trainer/trainer_team.html')

def trainer_currentteam(request):
    return render(request,'software_training/training/trainer/trainer_current_team_list.html')

def trainer_currenttrainees(request):
    return render(request, 'software_training/training/trainer/trainer_current_trainees_list.html')

def trainer_currenttraineesdetails(request):
    return render(request,'software_training/training/trainer/trainer_current_tainees_details.html')

def trainer_currentattentable(request):
    return render(request,'software_training/training/trainer/trainer_current_atten_table.html')

def trainer_currentperform(request):
    return render(request,'software_training/training/trainer/trainer_current_perform.html')

def trainer_currentattenadd(request):
    return render(request,'software_training/training/trainer/trainer_current_atten_add.html')

def trainer_previousteam(request):
    return render(request,'software_training/training/trainer/trainer_previous_team_list.html')

def trainer_previoustrainees(request):
    return render(request,'software_training/training/trainer/trainer_previous_trainess_list.html')

def trainer_previoustraineesdetails(request):
    return render(request, 'software_training/training/trainer/trainer_previous_trainees_details.html')

def trainer_previousattentable(request):
    return render(request,'software_training/training/trainer/trainer_previous_atten_table.html')

def trainer_previousperfomtable(request):
    return render(request,'software_training/training/trainer/trainer_previous_performtable.html')

def trainer_current_attendance(request):
    return render(request,'software_training/training/trainer/trainer_current_attendance.html')

def trainer_Task(request) :
    return render(request,'software_training/training/trainer/trainer_task.html')
    
def trainer_teamlistpage(request) :
    return render(request,'software_training/training/trainer/trainer_teamlist.html')
    
def trainer_taskpage(request) :
    return render(request, 'software_training/training/trainer/trainer_taskfor.html')
    
def trainer_givetask(request) :
    return render(request, 'software_training/training/trainer/trainer_givetask.html')
    
def trainer_taskgivenpage(request) :
    return render(request,'software_training/training/trainer/trainer_taskgiven.html')
    
def trainer_taska(request):
    return render(request, 'software_training/training/trainer/trainer_taska.html')

def trainer_task_completed_teamlist(request):
    return render(request, 'software_training/training/trainer/trainer_task_completed_teamlist.html')

def trainer_task_completed_team_tasklist(request):
    return render(request, 'software_training/training/trainer/trainer_task_completed_team_tasklist.html')

def trainer_task_previous_teamlist(request):
    return render(request, 'software_training/training/trainer/trainer_task_previous_teamlist.html')

def trainer_task_previous_team_tasklist(request):
    return render(request, 'software_training/training/trainer/trainer_task_previous_team_tasklist.html')

def trainer_trainees(request):
    return render(request, 'software_training/training/trainer/trainer_trainees.html')

def trainer_previous_trainees(request):
    return render(request,'software_training/training/trainer/trainer_previous_trainees.html')

def trainer_current_trainees(request):
    return render(request,'software_training/training/trainer/trainer_current_trainees.html')

def trainer_myreportissue_table(request):
    return render(request, 'software_training/training/trainer/trainer_myreportissue_table.html')

def trainer_current_attendance_view(request):
    return render(request,'software_training/training/trainer/trainer_current_attendance_view.html')

def trainer_attendance_trainees_viewattendance(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainees_viewattendance.html')

def trainer_attendance_trainees_viewattendancelist(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainees_viewattendancelist.html')

def trainer_attendance_trainees_addattendance(request):
    return render(request,'software_training/training/trainer/trainer_attendance_trainees_addattendance.html')
    
#******************  Trainee  *****************************

def trainee_dashboard_trainee(request):
    return render(request,'software_training/training/trainee/trainee_dashboard_trainee.html')
    
def trainee_task(request):
   return render(request,'software_training/training/trainee/trainee_task.html')   

def trainee_task_list(request):
    return render(request,'software_training/training/trainee/trainee_task_list.html')

def trainee_task_details(request):
    return render(request,'software_training/training/trainee/trainee_task_details.html')

def trainee_completed_taskList(request):
   return render(request,'software_training/training/trainee/trainee_completed_taskList.html')

def trainee_completedTask(request):
    return render(request,'software_training/training/trainee/trainee_completedTask.html')

def trainee_completed_details(request):
    return render(request,'software_training/training/trainee/trainee_completed_details.html')

def trainee_topic(request):
    return render(request, 'software_training/training/trainee/trainee_topic.html')

def trainee_currentTopic(request):
    return render(request, 'software_training/training/trainee/trainee_currentTopic.html')
    
def trainee_previousTopic(request):
    return render(request, 'software_training/training/trainee/trainee_previousTopic.html')

def trainee_reported_issue(request):
    return render(request, 'software_training/training/trainee/trainee_reported_issue.html')
   
def trainee_report_reported(request):
    return render(request, 'software_training/training/trainee/trainee_report_reported.html')
  
def trainee_report_issue(request):
    return render(request, 'software_training/training/trainee/trainee_report_issue.html')

def trainee_applyleave_form(request):
    return render(request, 'software_training/training/trainee/trainee_applyleave_form.html')  

def trainee_applyleave_card(request):
     return render(request, 'software_training/training/trainee/trainee_applyleave_cards.html')
    
def trainee_appliedleave(request):
     return render(request, 'software_training/training/trainee/trainee_appliedleave.html')
    
def Attendance(request):
   return render(request,'software_training/training/trainee/trainees_attendance.html')
    
def trainees_attendance_viewattendance(request):
    return render(request,'software_training/training/trainee/trainees_attendance_viewattendance.html')
 
def trainees_attendance_viewattendancelist(request):
   return render(request,'software_training/training/trainee/trainees_attendance_viewattendancelist.html')
   
def trainee_payment(request):
   return render(request,'software_training/training/trainee/trainee_payment.html')
   
def trainee_payment_addpayment(request):
   return render(request,'software_training/training/trainee/trainee_payment_addpayment.html')
  
def trainee_payment_viewpayment(request):
     return render(request,'software_training/training/trainee/trainee_payment_viewpayment.html')

#****************************  Admin- view  ********************************

def Admin_Dashboard(request):
    return render(request,'software_training/training/admin/admin_Dashboard.html')

def Admin_categories(request):
    return render(request,'software_training/training/admin/admin_categories.html') 

def Admin_emp_categories(request):
    return render(request,'software_training/training/admin/admin_emp_categories.html')  

def Admin_courses(request):
    return render(request,'software_training/training/admin/admin_courses.html')

def Admin_emp_course_list(request):
    return render(request,'software_training/training/admin/admin_emp_course_list.html')

def Admin_emp_course_details(request):
    return render(request,'software_training/training/admin/admin_emp_course_details.html')

def Admin_emp_profile(request):
    return render(request,'software_training/training/admin/admin_emp_profile.html')

def Admin_emp_attendance(request):
    return render(request,'software_training/training/admin/admin_emp_attendance.html')

def Admin_emp_attendance_show(request):
    return render(request,'software_training/training/admin/admin_emp_attendance_show.html')

def Admin_task(request):
    return render(request,'software_training/training/admin/admin_task.html')

def Admin_givetask(request):
    return render(request,'software_training/training/admin/admin_givetask.html')

def Admin_current_task(request):
    return render(request,'software_training/training/admin/admin_current_task.html')

def Admin_previous_task(request):
    return render(request,'software_training/training/admin/admin_previous_task.html')

def Admin_registration_details(request):
    return render(request,'software_training/training/admin/admin_registration_details.html')  

def Admin_attendance(request):
    return render(request,'software_training/training/admin/admin_attendance.html') 

def Admin_attendance_show(request):
    return render(request,'software_training/training/admin/admin_attendance_show.html')

def Admin_reported_issues(request):
    return render(request,'software_training/training/admin/admin_reported_issues.html') 

def Admin_emp_reported_detail(request):
    return render(request,'software_training/training/admin/admin_emp_reported_detail.html')

def Admin_emp_reported_issue_show(request):
    return render(request,'software_training/training/admin/admin_emp_reported_issue_show.html')

def Admin_manager_reported_detail(request):
    return render(request,'software_training/training/admin/admin_manager_reported_detail.html')

def Admin_manager_reported_issue_show(request):
    return render(request,'software_training/training/admin/admin_manager_reported_issue_show.html')

def Admin_add(request):
    return render(request,'software_training/training/admin/admin_add.html') 

def Admin_addcategories(request):
    return render(request,'software_training/training/admin/admin_addcategories.html') 

def Admin_categorieslist(request):
    return render(request,'software_training/training/admin/admin_categorieslist.html') 

def Admin_addcourse(request):
    return render(request,'software_training/training/admin/admin_addcourse.html') 

def Admin_addnewcourse(request):
    return render(request,'software_training/training/admin/admin_addnewcourse.html') 

def Admin_addnewcategories(request):
    return render(request,'software_training/training/admin/admin_addnewcategories.html') 

def Admin_courselist(request):
    return render(request,'software_training/training/admin/admin_courselist.html') 

def Admin_coursedetails(request):
    return render(request,'software_training/training/admin/admin_coursedetails.html') 

#******************accounts****************

def accounts_Dashboard(request):
    return render(request, 'software_training/training/account/accounts_Dashboard.html')

def accounts_registration_details(request):
    return render(request, 'software_training/training/account/accounts_registration_details.html')

def accounts_payment_details(request):
    return render(request, 'software_training/training/account/account_payment_details.html')

def accounts_payment_salary(request):
    return render(request, 'software_training/training/account/account_payment_salary.html')

def accounts_payment_view(request):
    return render(request, 'software_training/training/account/account_payment_view.html')

def accounts_report_issue(request):
    return render(request, 'software_training/training/account/account_report_issue.html')

def accounts_report(request):
    return render(request, 'software_training/training/account/account_report.html')

def accounts_reported_issue(request):
    return render(request, 'software_training/training/account/account_reported_issue.html')

def accounts_acntpay(request):
    return render(request, 'software_training/training/account/accounts_acntpay.html')

def accounts_employee(request):
    return render(request, 'software_training/training/account/accounts_employee.html')

def accounts_emp_dep(request):
    return render(request, 'software_training/training/account/accounts_emp_dep.html')

def accounts_emp_list(request):
    return render(request, 'software_training/training/account/accounts_emp_list.html')

def accounts_emp_details(request):
    return render(request, 'software_training/training/account/accounts_emp_details.html')

def accounts_add_bank_acnt(request):
    return render(request, 'software_training/training/account/accounts_add_bank_acnt.html')

def accounts_bank_acnt_details(request):
    return render(request, 'software_training/training/account/accounts_bank_acnt_details.html')

def accounts_salary_details(request):
    return render(request, 'software_training/training/account/accounts_salary_details.html')

def accounts_expenses(request):
    return render(request, 'software_training/training/account/accounts_expenses.html')

def accounts_expenses_viewEdit(request):
    return render(request, 'software_training/training/account/accounts_expenses_viewEdit.html')

def accounts_expenses_viewEdit_Update(request):
    return render(request, 'software_training/training/account/accounts_expenses_viewEdit.html')

def accounts_expense_newTransaction(request):
    return render(request, 'software_training/training/account/accounts_expense_newTransaction.html')

def accounts_paydetails(request):
    return render(request, 'software_training/training/account/accounts_paydetails.html')

def accounts_print(request):
    return render(request, 'software_training/training/account/accounts_print.html')

def accounts_payment(request):
    return render(request,'software_training/training/account/accounts_payment.html')

def accounts_payment_dep(request):
    return render(request, 'software_training/training/account/accounts_payment_dep.html')

def accounts_payment_list(request):
    return render(request, 'software_training/training/account/accounts_payment_list.html')

def accounts_payment_details(request):
    return render(request, 'software_training/training/account/accounts_payment_details.html')

def accounts_payment_detail_list(request):
    return render(request, 'software_training/training/account/accounts_payment_detail_list.html')

def accounts_payslip(request):
    return render(request, 'software_training/training/account/accounts_payslip.html')