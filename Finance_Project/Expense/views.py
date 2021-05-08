from django.shortcuts import render
from Finance_Project.models import expense
from django.contrib import messages

from django.db.models import Func
import json
from django.db.models import Sum
# Create your views here.


def Extract(field, date_field='DOW'):
    template = "EXTRACT({} FROM %(expressions)s::timestamp)".format(date_field)
    return Func(field, template=template)
#Import models of login after creation

def showExpense(request):
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
            user_expenses_details=expense.objects.filter(user_id=U_id).order_by('Date_time')
            print(user_expenses_details)
            return render(request,'viewExpenseStat.html',{'expenses': user_expenses_details})
         
        user_expenses_details=expense.objects.filter(user_id=U_id,Date_time__range=(date_start,date_end))
        print(user_expenses_details)

        a=user_expenses_details.annotate(month_stamp=Extract('Date_time', 'month')).values_list('month_stamp').annotate(total=Sum('Amount')).order_by('month_stamp')
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
        print(user_exp_mon_num)
        print(user_exp_mon_amount)
        # t1=user_expenses_mon.Monthnum
        # t2=user_expenses_mon.TotAmount
        
        # print(user_expenses_mon)
        # print(t2)
        
        
        # user_expenses_details=expense.objects.filter(user_id=U_id,Date_time__month=today.month)
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

        for i in temp_dict_exp: 
            user_expenses_names.append(i)
            user_expenses_perc.append(temp_dict_exp[i])


        U_name=request.session["User_name"]
        
        results2={
            "user_exp_mon_num":user_exp_mon_num,
            "user_exp_mon_amount":user_exp_mon_amount,
            "user_expenses_names":user_expenses_names,
            "user_expenses_perc":user_expenses_perc,
            "current_user_id":U_id,
            "current_user":U_name
            }
        
        
    
        results2_JSON=json.dumps(results2)
        return render(request,'viewExpenseStat.html',{'expenses': user_expenses_details,"dataval":results2_JSON})
        
    else:
        print("HEYYYYYYYYYYY")
        U_id=request.session.get("User_id")
        user_expenses_details1=expense.objects.filter(user_id=U_id,Date_time__year=today.year).order_by('Date_time')
        user_expenses_details=expense.objects.filter(user_id=U_id).order_by('Date_time')
        print(user_expenses_details)
        
        a=user_expenses_details1.annotate(month_stamp=Extract('Date_time', 'month')).values_list('month_stamp').annotate(total=Sum('Amount')).order_by('month_stamp')
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
        print(user_exp_mon_num)
        print(user_exp_mon_amount)
        # t1=user_expenses_mon.Monthnum
        # t2=user_expenses_mon.TotAmount
        
        # print(user_expenses_mon)
        # print(t2)
        
        
        user_expenses_details3=expense.objects.filter(user_id=U_id,Date_time__month=today.month)
        user_expenses_names=[]
        user_expenses_perc=[]
        temp_dict_exp={}
        total_exp=expense.objects.filter(user_id=U_id,Date_time__month=today.month).aggregate(Sum('Amount'))['Amount__sum']
        for x in user_expenses_details3:
            temp_dict_exp[x.Type]=0
        for x in user_expenses_details3:
            exp_per=int(x.Amount)*100 /int(total_exp)
            temp_dict_exp[x.Type]=round(temp_dict_exp[x.Type]+exp_per,2)
            
        for x in temp_dict_exp:
            print(str(x)+':'+str(temp_dict_exp[x]))

        for i in temp_dict_exp: 
            user_expenses_names.append(i)
            user_expenses_perc.append(temp_dict_exp[i])


        U_name=request.session["User_name"]
        
        results2={
            "user_exp_mon_num":user_exp_mon_num,
            "user_exp_mon_amount":user_exp_mon_amount,
            "user_expenses_names":user_expenses_names,
            "user_expenses_perc":user_expenses_perc,
            "current_user_id":U_id,
            "current_user":U_name
            }
            
        results2_JSON=json.dumps(results2)
        return render(request,'viewExpenseStat.html',{'expenses': user_expenses_details,"dataval":results2_JSON})
        

def AddExpense(request):
    if request.method=='POST' and 'Expense' in request.POST:
            # from __main__ import *
            # u_id = U_id
            # count_income=income.objects.raw("SELECT COUNT(*) FROM income;")
            # inc_id = count_income+1
            #print(inc_id)
            u_id=request.session.get("User_id")
            exp_amount=int(request.POST.get('Expense_amount'))
            print(u_id)
            print(exp_amount)

            exp_date=request.POST.get('Expense_date')
            exp_type=request.POST.get('Expense_type')
            exp_desc=request.POST.get('Expense_desc')
            exp_worth=request.POST.get('worth')
            print(exp_worth)
            print(exp_desc)
            print(exp_date)
            print('YESSSSS')
            U_name=request.session["User_name"]
            
            results2={
            "current_user_id":u_id,
            "current_user":U_name
            }
            
            results2_JSON=json.dumps(results2)
            try:
                if is_valid(exp_amount):
                    messages.success(request,'Expense added successfully')
                    print("sucess")
            except ValueError as e:
                    messages.error(request,''+ str(e))
                    print("sucess not")
            try:
                save_expense=expense()
                #user_count=SignUp_details.objects.raw("SELECT COUNT(*) FROM signup_details;")
                #saverecord.user_id=int(user_count)+1
                user_count=expense.objects.all().count()
                save_expense.Expense_id=int(user_count)+1
                
                save_expense.user_id=u_id
                save_expense.Amount=exp_amount
                save_expense.Date_time=exp_date
                save_expense.Type=exp_type
                save_expense.detail=exp_desc
                save_expense.worth=exp_worth
                save_expense.save()
                messages.success(request,'Expense added successfully!!!')
                print("sucess")
                return render(request,'addExpense.html',{'dataval':results2_JSON})
            except ValueError as e:
                print(e)
                return render(request,'addExpense.html',{'dataval':results2_JSON})

    else :
        u_id=request.session.get("User_id")

        U_name=request.session["User_name"]
        results2={
            "current_user_id":u_id,
            "current_user":U_name
            }
            
        results2_JSON=json.dumps(results2)
        return render(request,'addExpense.html',{'dataval':results2_JSON})

def is_valid(exp_amount):
    amount_reason = amount_valid(exp_amount)
    if not amount_reason == '':
        raise ValueError(amount_reason)
    return False


def amount_valid(exp_amount):
    if exp_amount < 0 :
        reason=('Amount entered is not valid.')
        return '',reason
    else:
        return ''



 