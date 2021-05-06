from django.shortcuts import render
from Finance_Project.models import Goals as goal 
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

def showGoal(request):
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
            user_goal_details=goal.objects.filter(user_id=U_id,Active=False).order_by('Goal_deadline')
            user_goal_details2=goal.objects.filter(user_id=U_id,Active=True).order_by('Goal_deadline')
            print(user_goal_details)
            return render(request,'viewGoal.html',{'goals': user_goal_details,'goal_active':user_goal_details2})

        user_goal_details=goal.objects.filter(user_id=U_id,Goal_deadline__range=(date_start,date_end))
        user_goal_details2=goal.objects.filter(user_id=U_id,Active=True).order_by('Goal_deadline')
        print(user_goal_details)
    # return render(request,'viewExpenseStat.html',{'expenses': user_expenses_details,"dataval":results2_JSON})
        return render(request,'viewGoal.html',{'goals': user_goal_details,'goal_active':user_goal_details2})
    
    
    else:
        print("HEYYYYYYYYYYY")
        U_id=request.session.get("User_id")
        user_goal_details=goal.objects.filter(user_id=U_id,Active=False).order_by('Goal_deadline')
        user_goal_details2=goal.objects.filter(user_id=U_id,Active=True).order_by('Goal_deadline').annotate(rem= Cast(F('amount_till_now') ,output_field=FloatField())/Cast(F('Amount_to_save') ,output_field=FloatField()))
        # user_goal_details2.rem=F('Amount_till_save')/F('amount_till_now')
        # user_goal_details2.save()
        print(user_goal_details2)
        # results2={
        #     "Goal_id":user_goal_details2.values('Goal_id'),
        #     "rem":user_goal_details2.values('rem')
        #     }
        result_list = list(user_goal_details2.values('Goal_id', 'rem'))
        results2_JSON=json.dumps(result_list)
        return render(request,'viewGoal.html',{'goals': user_goal_details,'goal_active':user_goal_details2,'dataval':results2_JSON})

@csrf_exempt
def Unread(request):
    # print("YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    index=request.POST['index']
    amount_to_be_added=int(request.POST['amount'])

    # print("hello")
    # print("count status ",count)
    
    if amount_to_be_added<=0:
        return HttpResponse("Failure")
    
    a=goal.objects.filter(Goal_id=int(index)).values_list('amount_till_now')[0]
    print(a[0])

    amt_to_save=goal.objects.filter(Goal_id=int(index)).values_list('Amount_to_save')[0]
    amt_remaining=amt_to_save[0]-a[0]
    if amount_to_be_added > amt_remaining:
        return HttpResponse("Failure")

    
    goal.objects.filter(Goal_id=int(index)).update(amount_till_now=amount_to_be_added+a[0])
    # print('H1')
    # print(amt_remaining)
    # print(amount_to_be_added)
    
    if amt_remaining == amount_to_be_added:
        goal.objects.filter(Goal_id=int(index)).update(Active=False)
    # import datetime
    # today=datetime.date.today()
    
    # print("HEYYYYYYYYYYY")
    # U_id=request.session.get("User_id")
    # user_goal_details=goal.objects.filter(user_id=U_id,Active=False).order_by('Goal_deadline')
    # user_goal_details2=goal.objects.filter(user_id=U_id,Active=True).order_by('Goal_deadline').annotate(rem= Cast(F('amount_till_now') ,output_field=FloatField())/Cast(F('Amount_to_save') ,output_field=FloatField()))
    # # user_goal_details2.rem=F('Amount_till_save')/F('amount_till_now')
    # # user_goal_details2.save()
    # print(user_goal_details2)
    # # results2={
    # #     "Goal_id":user_goal_details2.values('Goal_id'),
    # #     "rem":user_goal_details2.values('rem')
    # #     }
    # result_list = list(user_goal_details2.values('Goal_id', 'rem'))
    # results2_JSON=json.dumps(result_list)
    # return render(request,'viewGoal.html',{'goals': user_goal_details,'goal_active':user_goal_details2,'dataval':results2_JSON})



    return HttpResponse("Success")














@csrf_exempt
def delete(request):
    # print("YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    index=request.POST['index']
    
    print(index)
    goal.objects.filter(Goal_id=int(index)).update(Active=False)
    return HttpResponse("Success")