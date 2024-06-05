"""
Setting up admin panels
"""
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from main.models import Material, MaterialType, Order, OrderReport, OrderLine, Supplier
from main.admin_utils import get_total_amount_order


class AdminCore(admin.AdminSite):
    """
    Customization admin panel for content management
    """
    site_header = "Система учета материалов"
    site_title = "Система учета материалов"
    index_title = "Основные сущности"


admin_core = AdminCore(name="Count material")


class OrderInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        if not any(form.cleaned_data and not form.cleaned_data.get('DELETE', False) for form in self.forms):
            raise ValidationError('Добавьте объекты для создания заказа')


class OrderLineTabularInline(admin.TabularInline):
    model = OrderLine
    formset = OrderInlineFormSet

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        print(db_field)
        if db_field.name == 'material':
            kwargs['queryset'] = Material.objects.filter(stock_amount__gt=0)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title',)


class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'total_amount_new', 'date_created')

    inlines = [
        OrderLineTabularInline
    ]

    def total_amount_new(self, order: Order):
        return get_total_amount_order(order)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class OrderLineAdmin(admin.ModelAdmin):
    pass


class OrderReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'result_file', 'report_for')

    def save_model(self, request, obj, form, change):
        messages.add_message(request, messages.INFO, 'Отчет готов! Вы можете его скачать.')
        super().save_model(request, obj, form, change)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin_core.register(Material, MaterialAdmin)
admin_core.register(MaterialType, MaterialTypeAdmin)
admin_core.register(Order, OrderAdmin)
admin_core.register(OrderReport, OrderReportAdmin)
admin_core.register(OrderLine, OrderLineAdmin)
admin_core.register(Supplier, SupplierAdmin)
