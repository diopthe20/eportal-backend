# Generated by Django 4.2.3 on 2023-07-06 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0004_rename_mobile_pdfagent_mobile_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfagent',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
