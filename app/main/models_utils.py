import datetime
from pathlib import Path
from typing import Any, List
from dateutil.relativedelta import relativedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import F
from pandas import DataFrame



def create_report_order(report, order_model, order_line_model) -> Any:
    time_data = {
        'hours': 1,
        'days': 1,
        'months': 1
    }

    last_date = datetime.datetime.now() - relativedelta(
        **{report.report_for + "s": time_data[report.report_for + 's']}
    )
    all_orders = getattr(order_model, 'objects').filter(
        date_created__gte=last_date
    )
    report_order_line_list = []

    for order in all_orders:
        order_report = order.orderline_set.all().annotate(
            ID=F('order__order_id'),
            Наминование=F('material__title'),
            Сумма=F('price_by_order') * F('count'),
            Количество=F('count'),
        ).values(
            'ID',
            'Наминование',
            'Сумма',
            'Количество'
        )
        report_order_line_list.extend(list(order_report))

    data_frame = DataFrame(report_order_line_list)
    file_name = f'Report_{datetime.datetime.now()}.xlsx'
    file_path = Path('media', 'reports') / file_name
    data_frame.to_excel(file_path)

    report.result_file = SimpleUploadedFile(
        name=file_name,
        content=open(file_path, 'rb',).read()
    )

    return dict()


