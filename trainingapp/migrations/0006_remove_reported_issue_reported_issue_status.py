# Generated by Django 4.0 on 2022-04-01 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainingapp', '0005_acntspayslip_acntspayslip_esitype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reported_issue',
            name='reported_issue_status',
        ),
    ]
