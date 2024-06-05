

from django.db.models import F, Sum

from main.models import Order


def get_total_amount_order(order: Order) -> int:
    total_amount = order.orderline_set.annotate(
        total_sum=F('price_by_order') * F('count')
    ).aggregate(
        Sum('total_sum')
    )

    return total_amount['total_sum__sum']


