# Generated by Django 4.2.1 on 2023-06-30 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='reference_code',
            field=models.CharField(blank=True, default='No Reference Code Provides', max_length=100, null=True),
        ),
    ]
