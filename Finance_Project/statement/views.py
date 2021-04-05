from django.shortcuts import render
from django.shortcuts import render
from login.models import Employee
from login.models import SignUp_details
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.views.generic import TemplateView

from django.http import HttpResponse
from django.views.generic import View
 
#importing get_template from loader
from django.template.loader import get_template
 
#import render_to_pdf from util.py 
from .utils import render_to_pdf 


def showdata(request):
    
    results=Employee.objects.all()
    print(results)
    return render(request,'index.html',{"dataval":results})



class GeneratePdf(TemplateView):
    

    def get(self, request, *args, **kwargs):
        
        #getting the template
        pdf = render_to_pdf(self.template_name)
         
         #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')