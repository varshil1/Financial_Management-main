from django.db import models

class Employee(models.Model):
    empid=models.IntegerField(primary_key=True)
    empname=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    class Meta:
        db_table="employee"

#Create class login and Signup -hemil
class SignUp_details(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    mobile_no=models.IntegerField(max_length=10)
    email_id=models.EmailField()
    password=models.CharField(max_length=100)
    class Meta:
        db_table="signup_details"
