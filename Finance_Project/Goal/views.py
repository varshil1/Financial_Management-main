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
        U_name=request.session["User_name"]
        
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
        U_name=request.session["User_name"]
        
        results2_u={
            "current_user":U_name
            }
            
        results2_JSONu=json.dumps(results2_u)
    # return render(request,'viewExpenseStat.html',{'expenses': user_expenses_details,"dataval":results2_JSON})
        return render(request,'viewGoal.html',{'goals': user_goal_details,'goal_active':user_goal_details2,'datavalu':results2_JSONu})
    
    
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
        # import datetime
        # import json

        
        
        U_name=request.session["User_name"]
        
        results2_u={
            "current_user":U_name
            }
            
        results2_JSONu=json.dumps(results2_u)

        result_list = list(user_goal_details2.values('Goal_id','rem','Goal_name','description','Amount_to_save','Goal_deadline'))
        results2_JSON=json.dumps(result_list,default=default)
        return render(request,'viewGoal.html',{'goals': user_goal_details,'goal_active':user_goal_details2,'dataval':results2_JSON,'datavalu':results2_JSONu})


def default(o):
    import datetime
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


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
def Update(request):
    print("YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    index=request.POST['index']
    
    print(index)

    new_goal=request.POST['update_goal']
    new_goal_desc=request.POST['update_goal_desc']
    new_goal_amt=int(request.POST['update_goal_amount'])
    new_goal_date=request.POST['update_goal_date']
    
    # print(new_goal)
    # print(new_goal_amt)
    # print(new_goal_date)
    # print(new_goal_desc)
    # goal.objects.filter(Goal_id=int(index)).update(Active=False)

    if new_goal_amt<=0:
        return HttpResponse("Failure")

    goal.objects.filter(Goal_id=int(index)).update(Goal_name=new_goal,Amount_to_save=new_goal_amt,Goal_deadline=new_goal_date,description=new_goal_desc)
    

    return HttpResponse("Success")





@csrf_exempt
def delete(request):
    # print("YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    index=request.POST['index']
    
    print(index)
    goal.objects.filter(Goal_id=int(index)).update(Active=False)
    return HttpResponse("Success")




def AddGoal(request):
    if request.method=='POST' and 'Goals' in request.POST:
            # from __main__ import *
            # u_id = U_id
            # count_income=income.objects.raw("SELECT COUNT(*) FROM income;")
            # inc_id = count_income+1
            #print(inc_id)
            u_id=request.session.get("User_id")
            print("Are we getting it??")
            print(u_id)
                
            goal_name=request.POST.get('Goal_name')
            goal_desc=request.POST.get('Goal_desc')
            goal_amount=int(request.POST.get('Goal_amount'))
            
            print(goal_amount)

            goal_date=request.POST.get('Goal_date')
            print(goal_desc)
            print(goal_date)
            print('YESSSSS')

            U_name=request.session["User_name"]
            
            results2={
            "current_user_id":u_id,
            "current_user":U_name
            }
            
            results2_JSON=json.dumps(results2)
            
            try:
                if is_valid(goal_amount):
                    messages.success(request,'Goal added successfully')
                    print("sucess")
            except ValueError as e:
                    messages.error(request,''+ str(e))
                    print("sucess not")
            try:
                save_goal=goal()
                #user_count=SignUp_details.objects.raw("SELECT COUNT(*) FROM signup_details;")
                #saverecord.user_id=int(user_count)+1

                user_count=goal.objects.all().count()
                save_goal.Goal_id=int(user_count)+1
            
                save_goal.user_id=u_id
                save_goal.Amount_to_save=goal_amount
                save_goal.Goal_deadline=goal_date
                save_goal.Active=True
                save_goal.amount_till_now='0'
                save_goal.Goal_name=goal_name
                save_goal.description=goal_desc
                save_goal.save()
                messages.success(request,'Goal added successfully!!!')
                print("sucess")
                return render(request,'addGoal.html',{'dataval':results2_JSON})
            except ValueError as e:
                print(e)
                return render(request,'addGoal.html',{'dataval':results2_JSON})

    else :
        u_id=request.session.get("User_id")
            
        U_name=request.session["User_name"]
            
        results2={
        "current_user_id":u_id,
        "current_user":U_name
        }
            
        results2_JSON=json.dumps(results2)
        return render(request,'addGoal.html',{'dataval':results2_JSON})

def is_valid(goal_amount):
    amount_reason = amount_valid(goal_amount)
    if not amount_reason == '':
        raise ValueError(amount_reason)
    return False


def amount_valid(goal_amount):
    if goal_amount < 0 :
        reason=('Amount entered is not valid.')
        return '',reason
    else:
        return ''


