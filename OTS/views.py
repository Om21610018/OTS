from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from OTS.models import *
from django.template import loader
from django.contrib.auth import logout
import random

# Create your views here.
def welcome(request):
    template=loader.get_template('welcome.html')
    return HttpResponse(template.render())



def candidateRegistrationForm(request):
    res = render(request,'registration_form.html')
    return res
    # template = loader.get_template('registration_form.html')
    # return HttpResponse(template.render())

def candidateRegistration(request):
    # jab form waha se submit hota hai tab request mei form data aata hai 
    if request.method=='POST':
        username=request.POST['username']
        #Check if the user already exists
        if(len(Candidate.objects.filter(username=username))) :
            userStatus=1#user already exists
        else :
            candidate=Candidate()
            candidate.username=username
            candidate.password=request.POST['password']
            candidate.name=request.POST['name']
            candidate.save()
            userStatus=2

    else:
        userStatus=3#iska mtlb hai ki method post nhi hai
    context={
        'userStatus':userStatus,
    }
    res=render(request,'registration.html',context)#kitne bhi bhej skte ho argumennts
    return res




        #POST ke naame ki and GET ke naam ki dictionary hoti hai request attribute mei
        #Aur unki keys woh name attribute ke value hote hai
    pass
def loginView(request):
    if(request.method=='POST'):
        username = request.POST['username']
        password = request.POST['password']
        candidate = Candidate.objects.filter(username=username,password=password)
        if(len(candidate)==0) :
            loginError="Invalid Username or Password"
            res = render(request,'login.html',{'loginError':loginError})#ye jab aapka login fail hoga tab call hoga
        else : 
            #login success
            request.session['username']=candidate[0].username
            request.session['name']=candidate[0].name #used to store the username and name
            res=HttpResponseRedirect('home')
    else :
        res = render(request,'login.html')
    return res

def candidateHome(request):
    if 'name' not in request.session.keys() :#session storage pure file kei liye hota hai IMPORTANT HAI BAHOT PRIVACY KE LIYE WITHOUT DIRECT LINK ACCESS NHI HOGA
        res=HttpResponseRedirect('login')
    else :
        name=request.session['name']
        context={
            'name':name
        }
        res = render(request,'home.html',context)
    return res

def testPaper(request):
    if 'name' not in request.session.keys() :#session storage pure file kei liye hota hai IMPORTANT HAI BAHOT PRIVACY KE LIYE WITHOUT DIRECT LINK ACCESS NHI HOGA
        res=HttpResponseRedirect('login')
    #fetch question from database table
    n=int(request.GET['n'])# iski value url mei hogi
    question_pool = list(Question.objects.all())
    random.shuffle(question_pool)#it shuffles the element in list
    questions_list=question_pool[:n]#needs starting n questions
    context={
        'questions':questions_list,
    }
    return render(request,'test_paper.html',context)

def calculateTestResult(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect('login')
    total_attempt=0
    total_wrong=0
    total_right=0
    qid_list=[]
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list :
        question=Question.objects.get(qid=n)#usually ek hi result aayega woh bhi object hoga
        try:    
            if question.ans==request.POST['q'+str(n)] :
                total_right+=1
            else :
                total_wrong+=1
            total_attempt+=1
        except :
            pass
    
    points=(total_right-total_wrong)/len(qid_list)*10
    #store result in result table
    result=Result()
    result.username=Candidate.objects.get(username=request.session['username'])
    result.attempt=total_attempt
    result.right=total_right
    result.wrong=total_wrong
    result.points=points
    result.save()
    #update candidate table
    candidate=Candidate.objects.get(username=request.session['username'])
    candidate.test_attempted+=1
    candidate.points=(candidate.points*(candidate.test_attempted-1)+points)/candidate.test_attempted
    candidate.save()
    return HttpResponseRedirect('result')
        

def testResultHistory(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect('login')
        return res
    candidate=Candidate.objects.get(username=request.session['username'])
    result=Result.objects.filter(username_id=candidate.username)
    context={
        'candidate':candidate,
        'results':result,
    }
    res=render(request,'candidate_history.html',context)
    return res

def showTestResult(request):
    if 'name' not in request.session.keys():#ye code har baar check krega goi unothorized entry chah raha hai kya 
        res=HttpResponseRedirect('login')
        return res
    #fetch latest result form result table
    result=Result.objects.filter(result=Result.objects.latest('result').result,username=request.session['username'])
    context={
        'result':result,
    }
    res=render(request,"show_result.html",context)
    return res


def logoutView(request):
    del request.session['username']
    del request.session['name']
    logout(request)#destroy sesssion variables
    return HttpResponseRedirect('login')