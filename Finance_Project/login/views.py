from django.shortcuts import render
from login.models import Employee
from login.models import SignUp_details
from Finance_Project.models import Goals,expense,income
from django.contrib import messages
import json
from django.db.models import Sum

from heapq import nlargest
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
            U_id = SignUp_details.objects.get(user_name=uname_given).user_id

            # Goal chart and calculations
            user_goals_details=Goals.objects.filter(user_id=U_id,Active=True)
            user_goals_names=[]
            user_goals_perc=[]
            temp_dict={}
            for x in user_goals_details:
                save=int(x.amount_till_now)*100 /int(x.Amount_to_save)
                temp_dict[x.Goal_name]=round(save,2)
                # user_goals_perc.append(round(save,2))
                # user_goals_names.append(x.Goal_name)
                # print(x.Goal_id)
            print(U_id)


            # for x in temp_dict:
            #     print(str(x)+':'+str(temp_dict[x]))

            if len(temp_dict)<=5:
                res = nlargest(len(temp_dict), temp_dict, key = temp_dict.get)
                # print("Here 1")
            else:
                res = nlargest(5, temp_dict, key = temp_dict.get)
                # print("Here 2")

            for i in res: 
                user_goals_names.append(i)
                user_goals_perc.append(temp_dict[i])
            # for x in user_goals_names:
            #     print(x)
            # for x in user_goals_perc:
            #     print(x)


            # Expenses and calculations
            user_expenses_details=expense.objects.filter(user_id=U_id)
            user_expenses_names=[]
            user_expenses_perc=[]
            temp_dict_exp={}
            total_exp=expense.objects.filter(user_id=U_id).aggregate(Sum('Amount'))['Amount__sum']
            for x in user_expenses_details:
                exp_per=int(x.Amount)*100 /int(total_exp)
                temp_dict_exp[x.Type]=round(exp_per,2)
                
            for x in temp_dict_exp:
                print(str(x)+':'+str(temp_dict_exp[x]))


            if len(temp_dict_exp)<=3:
                res = nlargest(len(temp_dict_exp), temp_dict_exp, key = temp_dict_exp.get)
                # print("Here 1 exp")
            else:
                res = nlargest(3, temp_dict_exp, key = temp_dict_exp.get)
                # print("Here 2 exp")

            for i in res: 
                user_expenses_names.append(i)
                user_expenses_perc.append(temp_dict_exp[i])

            others_exp=0
            for j in temp_dict_exp:
                if j not in res:
                    others_exp+=temp_dict_exp[j]

            # print(others_exp)
            user_expenses_names.append("Miscellaneous")
            user_expenses_perc.append(others_exp)

            # for x in user_expenses_names:
            #     print(x)
            # for x in user_expenses_perc:
            #     print(x)




            # Incomes and calculations
            user_inc_details=income.objects.filter(user_id=U_id)
            user_inc_names=[]
            user_inc_perc=[]
            temp_dict_inc={}
            total_inc=income.objects.filter(user_id=U_id).aggregate(Sum('Amount'))['Amount__sum']
            for x in user_inc_details:
                inc_per=int(x.Amount)*100 /int(total_inc)
                temp_dict_inc[x.Type]=round(inc_per,2)
                
            for x in temp_dict_inc:
                print(str(x)+':'+str(temp_dict_inc[x]))


            if len(temp_dict_inc)<=3:
                res_inc = nlargest(len(temp_dict_inc), temp_dict_inc, key = temp_dict_inc.get)
                # print("Here 1 exp")
            else:
                res_inc = nlargest(3, temp_dict_inc, key = temp_dict_inc.get)
                # print("Here 2 exp")

            for i in res_inc: 
                user_inc_names.append(i)
                user_inc_perc.append(temp_dict_inc[i])

            others_inc=0
            for j in temp_dict_inc:
                if j not in res_inc:
                    others_inc+=temp_dict_inc[j]

            # print(others_exp)
            user_inc_names.append("Miscellaneous")
            user_inc_perc.append(round(others_inc,2))

            for x in user_inc_names:
                print(x)
            for x in user_inc_perc:
                print(x)

            results2={
            "data_goals":user_goals_perc,
            "labels_goals":user_goals_names,
            "data_exp":user_expenses_perc,
            "labels_exp":user_expenses_names,
            "data_inc":user_inc_perc,
            "labels_inc":user_inc_names,
            "current_user":uname_given,
            "current_user_id":U_id
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




            