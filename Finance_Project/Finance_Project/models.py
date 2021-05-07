from django.db import models

#class Employee(models.Model):
 #   empid=models.IntegerField(primary_key=True)
#    empname=models.CharField(max_length=100)
 #   email=models.CharField(max_length=100)
   # class Meta:
  #      db_table="employee"
class income(models.Model):
  id=models.IntegerField(primary_key=True)
  user_id=models.IntegerField()
  Amount=models.IntegerField()
  Date_time=models.DateTimeField()
  Type=models.CharField(max_length=50)
  class Meta:
    db_table="income"



class expense(models.Model):
  
  user_id=models.IntegerField()
  Amount=models.IntegerField()
  Date_time=models.DateTimeField()
  Type=models.CharField(max_length=50)
  Expense_id=models.AutoField(primary_key=True)
  detail=models.TextField()
  worth=models.CharField(max_length=5)
  class Meta:
    db_table="expense"

class worth(models.Model):
  user_id=models.IntegerField()
  preference=models.CharField(max_length=50)
  Expense_id=models.IntegerField()

  class Meta:
    db_table="worth"

class Goals(models.Model):
  Goal_id=models.AutoField(primary_key=True)
  user_id=models.IntegerField()
  Goal_name=models.CharField(max_length=50)
  Amount_to_save=models.IntegerField()
  amount_till_now=models.IntegerField()
  Active=models.BooleanField()
  description=models.CharField(max_length=1000)
  Goal_deadline=models.DateTimeField()
  class Meta:
     db_table="Goals"

class Bills(models.Model):
  user_id=models.IntegerField()
  Bill_id=models.AutoField(primary_key=True)
  Due_date=models.DateField()
  Bill_type=models.CharField(max_length=50)
  Details=models.TextField()
  Bill_Amount=models.IntegerField()
  Bill_Active=models.BooleanField()
  class Meta:
    db_table="Bills"