from django.shortcuts import render
from login.models import Employee
from login.models import SignUp_details
from Finance_Project.models import Goals,expense,income,Bills
from django.contrib import messages
import json
from django.db.models import Sum
from django.http import HttpResponseRedirect
from heapq import nlargest
from django.http import HttpResponse
from django.shortcuts import redirect


import calendar
import numpy as np
from django.db.models import Func

def Extract(field, date_field='DOW'):
    template = "EXTRACT({} FROM %(expressions)s::timestamp)".format(date_field)
    return Func(field, template=template)
#Import models of login after creation

def get_week_of_month(year, month, day):
    x = np.array(calendar.monthcalendar(year, month))
    week_of_month = np.where(x==day)[0][0] + 1
    return(week_of_month)

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
    storage = messages.get_messages(request)
    storage.used = True
    
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
            # messages.success(request,'Login successfully')
            U_id = SignUp_details.objects.get(user_name=uname_given).user_id
            request.session["User_id"]=U_id
            request.session["User_name"]=uname_given
            
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
            # print(U_id)


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
                temp_dict_exp[x.Type]=0
            for x in user_expenses_details:
                exp_per=int(x.Amount)*100 /int(total_exp)
                temp_dict_exp[x.Type]=round(temp_dict_exp[x.Type]+exp_per,2)
                
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
                temp_dict_inc[x.Type]=0
            for x in user_inc_details:
                inc_per=int(x.Amount)*100 /int(total_inc)
                temp_dict_inc[x.Type]=round(temp_dict_inc[x.Type]+inc_per,2)
                
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

            # for x in user_inc_names:
            #     print(x)
            # for x in user_inc_perc:
            #     print(x)

            # Income ends
            
            # Total details
            if income.objects.filter(user_id=U_id).aggregate(Sum('Amount'))['Amount__sum'] is None:
                user_inc_total=0
            else:
                user_inc_total=int(income.objects.filter(user_id=U_id).aggregate(Sum('Amount'))['Amount__sum'])


            
            if expense.objects.filter(user_id=U_id).aggregate(Sum('Amount'))['Amount__sum'] is None:
                user_exp_total=0
            else:
                user_exp_total=int(expense.objects.filter(user_id=U_id).aggregate(Sum('Amount'))['Amount__sum']) 
            
            user_acc_balance= user_inc_total-user_exp_total if user_inc_total>=user_exp_total else 0

            
            
            print(str(user_exp_total)+' '+str(user_inc_total)+' '+str(user_acc_balance))


            # Monthly charts
            # select extract(month from "Date_time"),sum("Amount") from "expense" where extract(year from "Date_time")=2020 group by extract(month from "Date_time")
            import datetime
            today=datetime.date.today()
            
            # a=expense.objects.filter(user_id=U_id).values('Date_time').annotate(total=Sum('Amount')).order_by('Amount')
            a=expense.objects.filter(user_id=U_id,Date_time__year=today.year).annotate(month_stamp=Extract('Date_time', 'month')).values_list('month_stamp').annotate(total=Sum('Amount')).order_by('month_stamp')
            
            user_exp_mon_num=[]
            user_exp_mon_amount=[]
            # a=expense.objects.raw('select extract(month from "Date_time")as MonthNum,sum("Amount") as TotAmount from "expense" where extract(year from "Date_time")=2020 AND "user_id"='+str(U_id)+' group by extract(month from "Date_time")')
            # print(a)

            for x in a:
                # print(x[0])
                user_exp_mon_num.append(x[0])
                user_exp_mon_amount.append(x[1]/1000)
                # print(x[1])
            t1=0
            for x in range(1,13):
                
                if x not in user_exp_mon_num:
                    user_exp_mon_num.insert(t1,x)
                    user_exp_mon_amount.insert(t1,0.00)
                t1+=1
            # print(user_exp_mon_num)
            # print(user_exp_mon_amount)
            # t1=user_expenses_mon.Monthnum
            # t2=user_expenses_mon.TotAmount
            
            # print(user_expenses_mon)
            # print(t2)



# a=expense.objects.filter(user_id=U_id).values('Date_time').annotate(total=Sum('Amount')).order_by('Amount')
            a=income.objects.filter(user_id=U_id,Date_time__year=today.year).annotate(month_stamp=Extract('Date_time', 'month')).values_list('month_stamp').annotate(total=Sum('Amount')).order_by('month_stamp')
            # print("Here")
            # print(a)
            user_inc_mon_num=[]
            user_inc_mon_amount=[]
            # a=expense.objects.raw('select extract(month from "Date_time")as MonthNum,sum("Amount") as TotAmount from "expense" where extract(year from "Date_time")=2020 AND "user_id"='+str(U_id)+' group by extract(month from "Date_time")')
            # print(a)

            for x in a:
                # print(x[0])
                user_inc_mon_num.append(x[0])
                user_inc_mon_amount.append(x[1]/1000)
                # print(x[1])
            t1=0
            for x in range(1,13):
                
                if x not in user_inc_mon_num:
                    user_inc_mon_num.insert(t1,x)
                    user_inc_mon_amount.insert(t1,0.00)
                t1+=1
            # print(user_inc_mon_num)
            # print(user_inc_mon_amount)
            # t1=user_expenses_mon.Monthnum
            # t2=user_expenses_mon.TotAmount
            
            # print(user_expenses_mon)
            # print(t2)

           # jeje=income.objects.filter(Date_time__year=today.year)
            # print(jeje)

            b=income.objects.filter(user_id=U_id,Date_time__year=today.year,Date_time__month=today.month).annotate(day_stamp=Extract('Date_time','DAY')).values_list('day_stamp').annotate(total=Sum('Amount')).order_by('day_stamp')
            user_inc_daily_num=[]
            user_inc_daily_amount=[]
            # a=expense.objects.raw('select extract(month from "Date_time")as MonthNum,sum("Amount") as TotAmount from "expense" where extract(year from "Date_time")=2020 AND "user_id"='+str(U_id)+' group by extract(month from "Date_time")')
            # print(b)

            for x in b:
                # print(x[0])
                user_inc_daily_num.append(x[0])
                user_inc_daily_amount.append(x[1]/1000)
                # print(x[1])
            t1=0
            for x in range(1,32):
                
                if x not in user_inc_daily_num:
                    user_inc_daily_num.insert(t1,x)
                    user_inc_daily_amount.insert(t1,0.00)
                t1+=1
            print(user_inc_daily_num)
            print(user_inc_daily_amount)
            # t1=user_expenses_mon.Monthnum
            # t2=user_expenses_mon.TotAmount
            
            # print(user_expenses_mon)
            # print(t2)




            b2=expense.objects.filter(user_id=U_id,Date_time__year=today.year,Date_time__month=today.month).annotate(day_stamp=Extract('Date_time','DAY')).values_list('day_stamp').annotate(total=Sum('Amount')).order_by('day_stamp')
            user_exp_daily_num=[]
            user_exp_daily_amount=[]
            # a=expense.objects.raw('select extract(month from "Date_time")as MonthNum,sum("Amount") as TotAmount from "expense" where extract(year from "Date_time")=2020 AND "user_id"='+str(U_id)+' group by extract(month from "Date_time")')
            # print(b2)

            for x in b2:
                # print(x[0])
                user_exp_daily_num.append(x[0])
                user_exp_daily_amount.append(x[1]/1000)
                # print(x[1])
            t1=0
            for x in range(1,32):
                
                if x not in user_exp_daily_num:
                    user_exp_daily_num.insert(t1,x)
                    user_exp_daily_amount.insert(t1,0.00)
                t1+=1
            # print(user_exp_daily_num)
            # print(user_exp_daily_amount)
            # t1=user_expenses_mon.Monthnum
            # t2=user_expenses_mon.TotAmount
            
            # print(user_expenses_mon)
            # print(t2)


            user_bill_details_temp=Bills.objects.filter(user_id=U_id,Bill_Active=True).order_by('Due_date')

            if expense.objects.filter(user_id=U_id,worth='yes').aggregate(total_price=Sum('Amount'))["total_price"] is None:
                user_exp_worth_yes=0
            else:
                user_exp_worth_yes=int(expense.objects.filter(user_id=U_id,worth='yes').aggregate(total_price=Sum('Amount'))["total_price"])
            

            if expense.objects.filter(user_id=U_id,worth='no').aggregate(total_price=Sum('Amount'))["total_price"] is None:
                user_exp_worth_no=0
            else:
                user_exp_worth_no=int(expense.objects.filter(user_id=U_id,worth='no').aggregate(total_price=Sum('Amount'))["total_price"])
            
            user_exp_worth_total=user_exp_worth_yes+user_exp_worth_no
            #print(user_exp_worth_yes)
            #print(user_exp_worth_no)
            print(user_exp_worth_total)
            if user_exp_worth_total==0:
                user_exp_worth_yes_per=0
            else:
                user_exp_worth_yes_per=(user_exp_worth_yes/user_exp_worth_total)*100

            
            print(user_exp_worth_yes_per)
            worthy_message=''
            if user_exp_worth_yes_per>75:
                worthy_message='Congratulations! You are a wise spender and avoid unnecessary expenses. Your worthy expenses are '+str(round(user_exp_worth_yes_per,2))
            elif user_exp_worth_yes_per>=50 and user_exp_worth_yes_per<75:
                worthy_message=' Congratulations! More than half of your expenses are worthy. Keep it up. Your worthy expenses are '+str(round(user_exp_worth_yes_per,2))
            elif user_exp_worth_yes_per>=25 and user_exp_worth_yes_per<50:
                worthy_message='Be careful! More than half of your expenses are unnecessary. Please spend wisely. Your worthy expenses are '+str(round(user_exp_worth_yes_per,2))
            elif user_exp_worth_yes_per>0 and user_exp_worth_yes_per<25:
                worthy_message='Alert! Your unnecessary expenses are way too high. Please take care and avoid them. Your worthy expenses are '+str(round(user_exp_worth_yes_per,2))
            else :
                worthy_message='ADD EXPENSES TO CHECK YOUR STATUS'

            print(worthy_message)
            results2={
            "data_goals":user_goals_perc,
            "labels_goals":user_goals_names,
            "data_exp":user_expenses_perc,
            "labels_exp":user_expenses_names,
            "data_inc":user_inc_perc,
            "user_inc_total":user_inc_total,
            "user_exp_total":user_exp_total,
            "user_acc_balance":user_acc_balance,
            "user_exp_mon_amount":user_exp_mon_amount,
            "user_inc_mon_amount":user_inc_mon_amount,
            "user_exp_daily_amount":user_exp_daily_amount,
            "user_inc_daily_amount":user_inc_daily_amount,
            "worthy_expenses":worthy_message,
            "labels_inc":user_inc_names,
            "current_user":uname_given,
            "current_user_id":U_id
            }
            
            results2_JSON=json.dumps(results2)
            user_bill_details=Bills.objects.filter(user_id=U_id,Bill_Active=True).order_by('Due_date')[:3]
            
            result_list = list(user_bill_details_temp.values('Bill_id'))
            results3_JSON=json.dumps(result_list)
            
            return render(request,'index_2.html',{"dataval":results2_JSON,"bill_details":user_bill_details,"dataval2":results3_JSON})
        else:
            messages.error(request,'Login unsuccessfully')
           
            return render(request,'login.html')
        
        
    elif request.method=='POST' and 'signin' in request.POST:
        flag=0
        user_name=request.POST.get('user_name')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        mobile_no=request.POST.get('mobile_no')
        email_id=request.POST.get('email_id')
        password=request.POST.get('password')
        try:
            temp=is_valid(user_name,first_name,last_name,mobile_no,email_id,password)
            if temp==None:
                messages.success(request,'Register successfully')
                print("helu")
                # return render(request,'login.html')
                flag=1
            else:
                for a in temp:
                    messages.error(request,'Register unsuccessfully:'+ str(a))
                    print(str(a))
                return render(request,'login.html')
                # return redirect('/')
                # return render(request, 'login.html', {'messages': messages})
        except ValueError as e:
                for a in e:
                    messages.error(request,'Register unsuccessfully:'+ str(a))
                    print(str(a))

        print(flag)
                # return render(request,'login.html')
        if flag==1:
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
                print('saved')
                messages.success(request,'Registered successfully!!!')
                return render(request,'login.html')
            except :
                print('Hellll')
                return render(request,'login.html')
        
    else:
        return render(request,'login.html')




def is_valid(user_name,first_name,last_name,mobile_no,email_id,password):
    flag=0

    userreason=user_name_valid(user_name)
    if not len(userreason)==0:
        return userreason
    
    pwreason=password_valid(user_name,password)
    if not len(pwreason)==0:
        return pwreason
    
    if not email_valid(email_id):
        return ['Email ID is invalid']
    
    nwreason=name_Valid(first_name,last_name)
    if not len(nwreason)==0:
        return nwreason
        
    if not mob_valid(mobile_no):
         return ['Mobile Number is invalid']
    
    return None



def user_name_valid(username):
    numupper =0
    pw_final=[]
    for c in username:
        if c.isupper():
            numupper = numupper + 1

    if numupper <= 0:
        pwreason=('Username must contain at least one uppercase character')
        pw_final.append(pwreason)

    numlower =0
    for c in username:
        if c.islower():
            numlower = numlower + 1

    if numlower <= 0:
        pwreason=('username must contain at least one lowercase character')
        pw_final.append(pwreason)

    if len(username)<8:
        pwreason = ('username must be greater than 8 characters')
        pw_final.append(pwreason)

    numdigit=0
    for c in username:
        if c.isdigit():
            numdigit = numdigit + 1

    if numdigit <= 0:
        pwreason= ('username must contain at least one number')
        pw_final.append(pwreason)

    return pw_final    
    






def password_valid(username,password):
    numupper =0
    pw_final=[]
    for c in password:
        if c.isupper():
            numupper = numupper + 1

    if numupper <= 0:
        pwreason=('password must contain at least one uppercase character')
        pw_final.append(pwreason)

    numlower =0
    for c in password:
        if c.islower():
            numlower = numlower + 1

    if numlower <= 0:
        pwreason=('password must contain at least one lowercase character')
        pw_final.append(pwreason)

        if len(password)<8:
            pwreason = ('password must be greater than 8 characters')
            pw_final.append(pwreason)

    numdigit=0
    for c in password:
        if c.isdigit():
            numdigit = numdigit + 1

    if numdigit <= 0:
        pwreason= ('password must contain at least one number')
        pw_final.append(pwreason)

    if username in password:
        pwreason= ('username cannot be used as part of your password')
        pw_final.append(pwreason)
    return pw_final
    


def email_valid(email_id):
    import re
 
    # Make a regular expression
    # for validating an Email
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
 
 
    # pass the regular expression
    # and the string in search() method
    if(re.search(regex, email_id)):
        return True
 
    else:
        return False


def name_Valid(first_name,last_name):
    pw_final=[]
    if not first_name.isalpha():
        pwreason= ('first name is not valid')
        pw_final.append(pwreason)
    if not last_name.isalpha():
        pwreason= ('Last name is not valid')
        pw_final.append(pwreason)
    return pw_final

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




            