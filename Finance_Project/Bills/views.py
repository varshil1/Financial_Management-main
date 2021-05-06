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
        return render(request,'viewBills.html',{'bills': user_bill_details,'bill_active':user_bill_details2,'dataval':results2_JSON})
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
        return render(request,'viewBills.html',{'bills': user_bill_details,'bill_active':user_bill_details2,'dataval':results2_JSON})


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