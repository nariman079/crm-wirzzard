# Generated by Django 5.0.6 on 2024-06-05 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_orderreport_result_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество в единицах материала'),
        ),
        migrations.AlterField(
            model_name='orderreport',
            name='result_file',
            field=models.FileField(blank=True, editable=False, null=True, upload_to='reports/', verbose_name='Скачать отчет'),
        ),
    ]