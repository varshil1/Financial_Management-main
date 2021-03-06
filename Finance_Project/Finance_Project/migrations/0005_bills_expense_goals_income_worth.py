# Generated by Django 3.1.7 on 2021-04-03 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Finance_Project', '0004_delete_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('user_id', models.IntegerField()),
                ('Bill_id', models.AutoField(primary_key=True, serialize=False)),
                ('Due_date', models.DateField()),
                ('Bill_type', models.CharField(max_length=50)),
                ('Details', models.TextField()),
                ('Bill_Amount', models.IntegerField()),
                ('Bill_Active', models.BooleanField()),
            ],
            options={
                'db_table': 'Bills',
            },
        ),
        migrations.CreateModel(
            name='expense',
            fields=[
                ('user_id', models.IntegerField()),
                ('Amount', models.IntegerField()),
                ('Date_time', models.DateTimeField()),
                ('Type', models.CharField(max_length=50)),
                ('Expense_id', models.AutoField(primary_key=True, serialize=False)),
                ('detail', models.TextField()),
            ],
            options={
                'db_table': 'expense',
            },
        ),
        migrations.CreateModel(
            name='Goals',
            fields=[
                ('Goal_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('Goal_name', models.CharField(max_length=50)),
                ('Amount_to_save', models.IntegerField()),
                ('amount_till_now', models.IntegerField()),
                ('Active', models.BooleanField()),
                ('Goal_deadline', models.IntegerField()),
            ],
            options={
                'db_table': 'Goals',
            },
        ),
        migrations.CreateModel(
            name='income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('Amount', models.IntegerField()),
                ('Date_time', models.DateTimeField()),
                ('Type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'income',
            },
        ),
        migrations.CreateModel(
            name='worth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('preference', models.CharField(max_length=50)),
                ('Expense_id', models.IntegerField()),
            ],
            options={
                'db_table': 'worth',
            },
        ),
    ]
