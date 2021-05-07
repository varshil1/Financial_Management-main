"""Finance_Project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from login import views as v1
from statement import views as v2
from statement.views import GeneratePdf
from Expense import views as v_exp
from Income import views as v_inc 
from Goal import views as v_goal
from Bills import views as v_bill

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$',v1.UserLogin,name='index'),
    url('statement',v2.showdata,name='statement'),
    url('addExpense',v_exp.AddExpense,name='addExpense'),
    url('viewExpense',v_exp.showExpense,name='viewExpense'),
    url('addIncome',v_inc.AddIncome,name='addIncome'),
    url('viewIncome',v_inc.showIncome,name='viewIncome'),
    url('viewGoal',v_goal.showGoal,name='viewGoal'),
    url('viewBill',v_bill.showBill,name='viewBill'),
    url('addGoal',v_goal.AddGoal,name='addGoal'),
    url('addBill',v_bill.AddBills,name='addBill'),
    path('notification/',v_goal.Unread,name='Unread'),
    path('notification2/',v_goal.delete,name='del'),
    path('notification3/',v_bill.delete,name='bill_del'),
    path('notification4/',v_goal.Update,name='edit_goal'),
    path('ajax/getData',v1.getData,name='getData'),
    path('pdf_download/<name>/', GeneratePdf.as_view(template_name='viewGoal.html') , name='pdf_download'),
]