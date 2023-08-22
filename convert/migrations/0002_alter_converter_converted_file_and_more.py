# Generated by Django 4.2.3 on 2023-08-22 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convert', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='converter',
            name='converted_file',
            field=models.FileField(null=True, upload_to='data'),
        ),
        migrations.AlterField(
            model_name='converter',
            name='original_file',
            field=models.FileField(upload_to='data'),
        ),
        migrations.AlterField(
            model_name='converter',
            name='original_thumbnail',
            field=models.FileField(null=True, upload_to='data'),
        ),
    ]