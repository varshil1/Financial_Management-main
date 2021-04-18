from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from Finance_Project.models import income
from login.models import SignUp_details
from django.contrib import messages
import json


from django.http import HttpResponse
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
            try:
                if is_valid(inc_amount):
                    messages.success(request,'Income added successfully')
                    print("sucess")
            except ValueError as e:
                    messages.error(request,''+ str(e))
                    print("sucess not")
            try:
                save_income=income()
                #user_count=SignUp_details.objects.raw("SELECT COUNT(*) FROM signup_details;")
                #saverecord.user_id=int(user_count)+1
                save_income.user_id=u_id
                save_income.Amount=inc_amount
                save_income.Date_time=inc_date
                save_income.Type=inc_type
                save_income.description=inc_desc
                save_income.save()
                messages.success(request,'Income added successfully!!!')
                print("sucess")
                return render(request,'addIncome.html')
            except ValueError as e:
                print(e)
                return render(request,'addIncome.html')

    else :
        return render(request,'addIncome.html')

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

