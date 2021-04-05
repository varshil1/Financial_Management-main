from django.shortcuts import render
from login.models import Employee
from login.models import SignUp_details
from django.contrib import messages
import json


from django.http import HttpResponse

#Import models of login after creation

def showdata(request):
    results=Employee.objects.all()
    print(results)
    return render(request,'index.html',{"dataval":results})

def getData(request):
    results={
            "data":[5,15,25,35,45],
            "labels":["Marriage2", "New-car", "Property", "Leh-ladakh trip", "Charity"]
            }
    # dataJSON = dumps(results)
    return HttpResponse(json.dumps(results))
    #return JsonResponse(results)


def login(request):
    return render(request,'login.html')

def UserLogin(request):
    if request.method=='POST' and 'login' in request.POST:
        
        uname_given=request.POST.get('username_log')
        upass_given=request.POST.get('pass_log')
        
        user_details=SignUp_details.objects.filter(user_name=uname_given)
        #upass_db=SignUp_details.password.all()
        results=user_details
        #results=upass_given
        #objects.raw('SELECT * FROM p_club_app_resources LIMIT 6')
        
        if SignUp_details.objects.filter(user_name=uname_given,password=upass_given) :
        #if True:
            messages.success(request,'Login successfully')
            results2={
            "data":[25,15,25,35,45],
            "labels":["Marriage", "New-car", "Property", "Leh-ladakh trip", "Charity"]
            }
            results2_JSON=json.dumps(results2)
            return render(request,'index_2.html',{"dataval":results2_JSON})
        else:
            messages.success(request,'Login unsuccessfully')
        
        
    elif request.method=='POST' and 'signin' in request.POST:
        
        user_name=request.POST.get('user_name')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        mobile_no=request.POST.get('mobile_no')
        email_id=request.POST.get('email_id')
        password=request.POST.get('password')
        try:
            if is_valid(user_name,first_name,last_name,mobile_no,email_id,password):
                messages.success(request,'Register successfully')
        except ValueError as e:
                messages.error(request,'Register unsuccessfully:'+ str(e))
                return render(request,'login.html')
        try:
            saverecord=SignUp_details()
            #user_count=SignUp_details.objects.raw("SELECT COUNT(*) FROM signup_details;")
            #saverecord.user_id=int(user_count)+1
            saverecord.user_name=user_name
            saverecord.first_name=first_name
            saverecord.last_name=last_name
            saverecord.mobile_no=mobile_no
            saverecord.email_id=email_id
            saverecord.password=password
            saverecord.save()
            messages.success(request,'Registered successfully!!!')
            return render(request,'log.html')
        except:
            return render(request,'index.html')
        
    else:
        return render(request,'login.html')




def is_valid(user_name,first_name,last_name,mobile_no,email_id,password):
    flag=0

    userreason=user_name_valid(user_name)
    if not userreason=='':
        raise ValueError(userreason)
    return False

    pwreason=password_valid(user_name,password)
    if not pwreason=='':
        raise ValueError(pwreason)
    return False

    if not email_valid(email_id):
        raise ValueError('Email ID is invalid')
    return False

    nwreason=name_Valid(first_name,last_name)
    if not nwreason=='':
        raise ValueError(nwreason)
    return False
        
    if not mob_valid(mobile_no):
         raise ValueError('Mobile Number is invalid')
    return False   




def user_name_valid(username):
    numupper =0
    for c in username:
        if c.isupper():
            numupper = numupper + 1

    if numupper <= 0:
        pwreason=('Username must contain at least one uppercase character')
        return '',pwreason

    numlower =0
    for c in username:
        if c.islower():
            numlower = numlower + 1

    if numlower <= 0:
        pwreason=('username must contain at least one lowercase character')
        return '', pwreason

        if len(username)<8:
            pwreason = ('username must be greater than 8 characters')
            return '',pwreason

    numdigit=0
    for c in username:
        if c.isdigit():
            numdigit = numdigit + 1

    if numdigit <= 0:
        pwreason= ('username must contain at least one number')
        return '',pwreason

        
    else:
        return ''






def password_valid(username,password):
    numupper =0
    for c in password:
        if c.isupper():
            numupper = numupper + 1

    if numupper <= 0:
        pwreason=('password must contain at least one uppercase character')
        return '',pwreason

    numlower =0
    for c in password:
        if c.islower():
            numlower = numlower + 1

    if numlower <= 0:
        pwreason=('password must contain at least one lowercase character')
        return '', pwreason

        if len(password)<8:
            pwreason = ('password must be greater than 8 characters')
            return '',pwreason

    numdigit=0
    for c in password:
        if c.isdigit():
            numdigit = numdigit + 1

    if numdigit <= 0:
        pwreason= ('password must contain at least one number')
        return '',pwreason

    if username in password:
        pwreason= ('username cannot be used as part of your password')
        return '',pwreason
        
    else:
        return ''


def email_valid(email_id):
    import re
 
    # Make a regular expression
    # for validating an Email
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
 
 
    # pass the regular expression
    # and the string in search() method
    if(re.search(regex, email)):
        return True
 
    else:
        return False


def name_Valid(first_name,last_name):
    
    if not first_name.isalpha():
        pwreason= ('first name is not valid')
        return '',pwreason
    if not last_name.isalpha():
        pwreason= ('first name is not valid')
        return '',pwreason

def mob_valid(mobile_no):
    import re
 
    # 1) Begins with 0 or 91
    # 2) Then contains 7 or 8 or 9.
    # 3) Then contains 9 digits
    Pattern = re.compile("(0/91)?[7-9][0-9]{9}")
    return Pattern.match(mobile_no)


def UserSignUp(request):
    if request.method=='POST' and 'signin' in request.POST:
        if  request.POST.get('user_name') and request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('mobile_no') and request.POST.get('email_id') and request.POST.get('password'):
            saverecord=SignUp_details()
            saverecord.user_name=request.POST.get('user_name')
            saverecord.first_name=request.POST.get('first_name')
            saverecord.last_name=request.POST.get('last_name')
            saverecord.mobile_no=request.POST.get('mobile_no')
            saverecord.email_id=request.POST.get('email_id')
            saverecord.password=request.POST.get('password')
            saverecord.save()
            messages.success(request,'Registered successfully!!!')




            