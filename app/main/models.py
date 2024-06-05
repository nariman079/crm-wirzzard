import uuid
from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models

from main.models_utils import create_report_order


class MaterialType(models.Model):
    class Meta:
        verbose_name = "Категория материала"
        verbose_name_plural = "Категории материалов"

    title = models.CharField(
        verbose_name="Название",
        max_length=200
    )

    def __str__(self):
        return self.title


class Supplier(models.Model):
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    title = models.CharField(
        verbose_name="Название",
        max_length=225
    )
    phone_number = models.CharField(
        verbose_name="Номер телефона"
    ),
    email = models.EmailField(
        verbose_name="Электронная почта"
    )
    address = models.CharField(
        verbose_name="Адрес",
        max_length=300
    )

    def __str__(self):
        return self.title


class Material(models.Model):
    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    title = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание",
        max_length=200,
    )
    price = models.IntegerField(
        verbose_name="Цена за единицу материала",
        max_length=200,
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )
    material_type = models.ForeignKey(
        MaterialType,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(
        auto_created=True, auto_now_add=True
    )
    for_sale = models.BooleanField(
        verbose_name="На продаже",
        default=True
    )
    stock_amount = models.PositiveIntegerField(
        verbose_name="Остаток на складе"
    )

    def __str__(self):
        return self.title


class Order(models.Model):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    order_id = models.CharField(
        verbose_name="Уникальный код заказа",
        max_length=200,
        null=True, blank=True,
        editable=False
    )

    total_amount = models.PositiveIntegerField(
        verbose_name="Общая стоимость",
        default=0,
        editable=False
    )
    date_created = models.DateTimeField(
        auto_created=True, auto_now_add=True
    )

    def __str__(self):
        return self.order_id

    def save(self, *args, **kwargs):
        if self.pk:
            pass
        else:
            self.order_id = uuid.uuid4().__str__()
        return super().save(*args, **kwargs)


class OrderLine(models.Model):
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField(
        verbose_name="Количество в единицах материала",
        default=0
    )
    price_by_order = models.PositiveIntegerField(
        verbose_name="Цена при покупке",
        null=True, blank=True,
        editable=False
    )

    def __str__(self):
        return self.order.__str__()

    def clean(self):
        if self.material.stock_amount ==  0:
            raise ValidationError({
                'count': f"Нет в наличии"
            })
        else:
            if self.count > self.material.stock_amount:
                raise ValidationError({
                    'count': f"Максимально возможное количество - {self.material.stock_amount}"
                })



    def save(self, *args, **kwargs):
        if self.pk:
            print(self.material.stock_amount)
        else:
            self.price_by_order = self.material.price
            # self.self.add_error('is_active', 'At least one question in this chapter must be active.')
            self.material.stock_amount -= self.count
            self.material.save()
        return super().save(*args, **kwargs)

class OrderReport(models.Model):
    class Meta:
        verbose_name = "Отчет о заказах"
        verbose_name_plural = "Отчеты о заказах"

    class ReportFor(models.TextChoices):
        hour = 'hour', 'Последний час'
        day = 'day', 'Последний день'
        month = 'month', 'Последний месяц'

    report_id = models.CharField(
        verbose_name="Уникальный код отчета",
        max_length=200,
        null=True, blank=True,
        editable=False
    )
    result_file = models.FileField(
        verbose_name="Скачать отчет",
        upload_to='reports/',
        null=True, blank=True,
        editable=False
    )
    report_for = models.CharField(
        verbose_name="Отчет за",
        max_length=255,
        choices=ReportFor.choices,
        default=ReportFor.month.name
    )

    def __str__(self):
        return self.report_id

    def save(self, *args, **kwargs):
        if self.pk:
            pass
        else:
            self.report_id = uuid.uuid4().__str__()
            create_report_order(self, Order, OrderLine)

        return super().save(*args, **kwargs)