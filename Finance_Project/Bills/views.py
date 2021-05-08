from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from Finance_Project.models import Bills as bill 
from Finance_Project.models import expense  
from django.contrib import messages

from django.db.models import Func
import json
from django.db.models import Sum
from django.db.models import F
from django.db.models import F, FloatField
from django.db.models.functions import Cast


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# from django.shortcuts import render_to_response
from django.http import HttpResponse

# Create your views here.

def Extract(field, date_field='DOW'):
    template = "EXTRACT({} FROM %(expressions)s::timestamp)".format(date_field)
    return Func(field, template=template)
#Import models of login after creation

def showBill(request):
    storage = messages.get_messages(request)
    storage.used = True
    import datetime
    today=datetime.date.today()
    U_name=request.session["User_name"]
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
            user_bill_details=bill.objects.filter(user_id=U_id,Active=False).order_by('Due_date')
            user_bill_details2=bill.objects.filter(user_id=U_id,Active=True).order_by('Due_date')
            print(user_bill_details)
            return render(request,'viewBills.html',{'bills': user_bill_details,'bill_active':user_bill_details2})

        user_bill_details=bill.objects.filter(user_id=U_id,Due_date__range=(date_start,date_end))
        user_bill_details2=bill.objects.filter(user_id=U_id,Bill_Active=True).order_by('Due_date')
        print(user_bill_details)
    # return render(request,'viewExpenseStat.html',{'expenses': user_expenses_details,"dataval":results2_JSON})
        results2={
                "Bill_id":user_bill_details2.values('Bill_id')
            }
        result_list = list(user_bill_details2.values('Bill_id'))
        results2_JSON=json.dumps(result_list)

        U_name=request.session["User_name"]
        
        results2_u={
            "current_user":U_name
            }
            
        results2_JSONu=json.dumps(results2_u)
        return render(request,'viewBills.html',{'bills': user_bill_details,'bill_active':user_bill_details2,'dataval':results2_JSON,'datavalu':results2_JSONu})
        # return render(request,'viewBills.html',{'bills': user_bill_details,'bill_active':user_bill_details2})
    
    
    else:
        print("HEYYYYYYYYYYY")
        U_id=request.session.get("User_id")
        user_bill_details=bill.objects.filter(user_id=U_id,Bill_Active=False).order_by('Due_date')
        user_bill_details2=bill.objects.filter(user_id=U_id,Bill_Active=True).order_by('Due_date')
        # user_goal_details2.rem=F('Amount_till_save')/F('amount_till_now')
        # user_goal_details2.save()
        # print(user_goal_details2)
        results2={
            "Bill_id":user_bill_details2.values('Bill_id')
            }
        result_list = list(user_bill_details2.values('Bill_id'))
        results2_JSON=json.dumps(result_list)
        U_name=request.session["User_name"]
        
        results2_u={
            "current_user":U_name
            }
            
        results2_JSONu=json.dumps(results2_u)
        return render(request,'viewBills.html',{'bills': user_bill_details,'bill_active':user_bill_details2,'dataval':results2_JSON,'datavalu':results2_JSONu,'UserName':U_name})


@csrf_exempt
def delete(request):
    print("YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    index=request.POST['index']
    U_id=request.session.get("User_id")
        
    print(index)
    bill.objects.filter(Bill_id=int(index)).update(Bill_Active=False)

    bill_det=bill.objects.filter(Bill_id=int(index))
    bill_amt=bill_det.values_list('Bill_Amount')[0]
    bill_date=bill_det.values_list('Due_date')[0]
    bill_type=bill_det.values_list('Bill_type')[0]
    # exp_count=expense.objects.all()
    bill_details=bill_det.values_list('Details')[0]
    a = expense(user_id=U_id, Amount =bill_amt[0] , Date_time=bill_date[0],Type=bill_type[0],detail=bill_details[0],Expense_id=expense.objects.all().count()+1)

    a.save()
    return HttpResponse("Success")



def AddBills(request):
    if request.method=='POST' and 'Bills' in request.POST:
            # from __main__ import *
            # u_id = U_id
            # count_income=income.objects.raw("SELECT COUNT(*) FROM income;")
            # inc_id = count_income+1
            #print(inc_id)
            u_id=request.session.get("User_id")
            print("Are we getting it??")
            print(u_id)
            bill_amount=int(request.POST.get('Bill_amount'))
            
            print(bill_amount)

            bill_date=request.POST.get('Bill_date')
            bill_type=request.POST.get('Bill_type')
            bill_desc=request.POST.get('Bill_desc')
            print(bill_desc)
            print(bill_date)
            print('YESSSSS')
            U_name=request.session["User_name"]
            
            results2={
            "current_user_id":u_id,
            "current_user":U_name
            }
            
            results2_JSON=json.dumps(results2)
            try:
                if is_valid(bill_amount):
                    messages.success(request,'Income added successfully')
                    print("sucess")
            except ValueError as e:
                    messages.error(request,''+ str(e))
                    print("sucess not")
            try:
                save_bill=bill()
                #user_count=SignUp_details.objects.raw("SELECT COUNT(*) FROM signup_details;")
                #saverecord.user_id=int(user_count)+1
                user_count=bill.objects.all().count()
                save_bill.Bill_id=int(user_count)+1
            
                
                save_bill.user_id=u_id
                save_bill.Bill_Amount=bill_amount
                save_bill.Due_date=bill_date
                save_bill.Bill_type=bill_type
                save_bill.Details=bill_desc
                save_bill.Bill_Active=True
                save_bill.save()
                
                messages.success(request,'Bills added successfully!!!')
                #sweetify.success(request, 'You did it', text='Good job! You successfully showed a SweetAlert message', persistent='Hell yeah')
                #return render(request,'addBill.html')
                print("sucess")
                return render(request,'addBill.html',{'dataval':results2_JSON})
            except ValueError as e:
                print(e)
                return render(request,'addBill.html',{'dataval':results2_JSON})

    else :
        u_id=request.session.get("User_id")

        U_name=request.session["User_name"]
        results2={
            "current_user_id":u_id,
            "current_user":U_name
            }
            
        results2_JSON=json.dumps(results2)
        return render(request,'addBill.html',{'dataval':results2_JSON})

def is_valid(bill_amount):
    amount_reason = amount_valid(bill_amount)
    if not amount_reason == '':
        raise ValueError(amount_reason)
    return False


def amount_valid(bill_amount):
    if bill_amount < 0 :
        reason=('Amount entered is not valid.')
        return '',reason
    else:
        return ''
