# Generated by Django 2.1.5 on 2020-08-22 16:51

from django.db import migrations, models
import django.db.models.deletion
import frontend.models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0012_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanAttach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=frontend.models.loan_attach_file)),
                ('loan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.Loan')),
            ],
        ),
    ]
