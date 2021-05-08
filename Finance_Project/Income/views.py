from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from Finance_Project.models import income
from login.models import SignUp_details
from django.contrib import messages
import json

from django.db.models import Func
from django.db.models import Sum
from django.http import HttpResponse





def Extract(field, date_field='DOW'):
    template = "EXTRACT({} FROM %(expressions)s::timestamp)".format(date_field)
    return Func(field, template=template)
#Import models of login after creation

def showIncome(request):
    # results=Employee.objects.all()
    # print(results)
    storage = messages.get_messages(request)
    storage.used = True
    import datetime
    today=datetime.date.today()

    if request.method=='POST' and 'date_submit' in request.POST:
    # if request.method=='POST':
        print("hey")
        date_start=request.POST.get('date_start')
        date_end=request.POST.get('date_end')
        print(date_start)
        print(date_end)
        U_id=request.session.get("User_id")
        
        if date_end > date_start:
            pass
        else:
            messages.error(request,"Please enter date properly")
            user_income_details=income.objects.filter(user_id=U_id).order_by('Date_time')
            print(user_income_details)
            return render(request,'viewIncomeStat.html',{'incomes': user_income_details})
         
        user_income_details=income.objects.filter(user_id=U_id,Date_time__range=(date_start,date_end))
        print(user_income_details)

        a=user_income_details.annotate(month_stamp=Extract('Date_time', 'month')).values_list('month_stamp').annotate(total=Sum('Amount')).order_by('month_stamp')
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
        print(user_inc_mon_num)
        print(user_inc_mon_amount)
        # t1=user_expenses_mon.Monthnum
        # t2=user_expenses_mon.TotAmount
        
        # print(user_expenses_mon)
        # print(t2)
        
        
        # user_expenses_details=expense.objects.filter(user_id=U_id,Date_time__month=today.month)
        user_income_names=[]
        user_income_perc=[]
        temp_dict_inc={}
        total_inc=income.objects.filter(user_id=U_id).aggregate(Sum('Amount'))['Amount__sum']
        for x in user_income_details:
            temp_dict_inc[x.Type]=0
        for x in user_income_details:
            inc_per=int(x.Amount)*100 /int(total_inc)
            temp_dict_inc[x.Type]=round(temp_dict_inc[x.Type]+inc_per,2)
            
        for x in temp_dict_inc:
            print(str(x)+':'+str(temp_dict_inc[x]))

        for i in temp_dict_inc: 
            user_income_names.append(i)
            user_income_perc.append(temp_dict_inc[i])


        
        U_name=request.session["User_name"]
        results2={
            "user_inc_mon_num":user_inc_mon_num,
            "user_inc_mon_amount":user_inc_mon_amount,
            "user_income_names":user_income_names,
            "user_income_perc":user_income_perc,
            "current_user_id":U_id,
            "current_user": U_name
            }
        
        
    
        results2_JSON=json.dumps(results2)
        return render(request,'viewIncomeStat.html',{'incomes': user_income_details,"dataval":results2_JSON})
        
    else:
        print("HEYYYYYYYYYYY")
        U_id=request.session.get("User_id")
        U_name=request.session["User_name"]
        user_income_details1=income.objects.filter(user_id=U_id,Date_time__year=today.year).order_by('Date_time')
        user_income_details=income.objects.filter(user_id=U_id).order_by('Date_time')
        print(user_income_details)
        
        a=user_income_details1.annotate(month_stamp=Extract('Date_time', 'month')).values_list('month_stamp').annotate(total=Sum('Amount')).order_by('month_stamp')
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
        print(user_inc_mon_num)
        print(user_inc_mon_amount)
        # t1=user_expenses_mon.Monthnum
        # t2=user_expenses_mon.TotAmount
        
        # print(user_expenses_mon)
        # print(t2)
        
        
        user_income_details3=income.objects.filter(user_id=U_id,Date_time__month=today.month)
        user_income_names=[]
        user_income_perc=[]
        temp_dict_inc={}
        total_inc=income.objects.filter(user_id=U_id,Date_time__month=today.month).aggregate(Sum('Amount'))['Amount__sum']
        for x in user_income_details3:
            temp_dict_inc[x.Type]=0
        for x in user_income_details3:
            inc_per=int(x.Amount)*100 /int(total_inc)
            temp_dict_inc[x.Type]=round(temp_dict_inc[x.Type]+inc_per,2)
            
        for x in temp_dict_inc:
            print(str(x)+':'+str(temp_dict_inc[x]))

        for i in temp_dict_inc: 
            user_income_names.append(i)
            user_income_perc.append(temp_dict_inc[i])


        
        results2={
            "user_inc_mon_num":user_inc_mon_num,
            "user_inc_mon_amount":user_inc_mon_amount,
            "user_income_names":user_income_names,
            "user_income_perc":user_income_perc,
            "current_user_id":U_id,
            "current_user":U_name
            }
            
        results2_JSON=json.dumps(results2)
        return render(request,'viewIncomeStat.html',{'incomes': user_income_details,"dataval":results2_JSON})


# Create your views here.
def AddIncome(request):
    if request.method=='POST' and 'Income' in request.POST:
            # from __main__ import *
            # u_id = U_id
            # count_income=income.objects.raw("SELECT COUNT(*) FROM income;")
            # inc_id = count_income+1
            #print(inc_id)
            u_id=request.session.get("User_id")
            
            print("Are we getting it??")
            print(u_id)

            
            inc_amount=int(request.POST.get('Income_Amount'))
            
            print(inc_amount)

            inc_date=request.POST.get('Income_date')
            inc_type=request.POST.get('Income_Type')
            inc_desc=request.POST.get('Income_desc')
            print(inc_desc)
            print(inc_date)
            print('YESSSSS')
            
            U_name=request.session["User_name"]
            
            results2={
            "current_user_id":u_id,
            "current_user":U_name
            }
            
            results2_JSON=json.dumps(results2)
            try:
                if is_valid(inc_amount):
                    messages.success(request,'Income added successfully')
                    print("sucess")
            except ValueError as e:
                    messages.error(request,''+ str(e))
                    print("sucess not")
            try:
                save_income=income()
                user_count=income.objects.all().count()
                save_income.id=int(user_count)+1
                # save_income.id=
                save_income.user_id=u_id
                save_income.Amount=inc_amount
                save_income.Date_time=inc_date
                save_income.Type=inc_type
                save_income.description=inc_desc
                save_income.save()
                messages.success(request,'Income added successfully!!!')
                print("sucess")
                return render(request,'addIncome.html',{'dataval':results2_JSON})
            except ValueError as e:
                print(e)
                return render(request,'addIncome.html',{'dataval':results2_JSON})

    else :
        u_id=request.session.get("User_id")

        U_name=request.session["User_name"]
        results2={
            "current_user_id":u_id,
            "current_user":U_name
            }
            
        results2_JSON=json.dumps(results2)
        return render(request,'addIncome.html',{'dataval':results2_JSON})

def is_valid(inc_amount):
    amount_reason = amount_valid(inc_amount)
    if not amount_reason == '':
        raise ValueError(amount_reason)
    return False


def amount_valid(inc_amount):
    if inc_amount < 0 :
        reason=('Amount entered is not valid.')
        return '',reason
    else:
        return ''

