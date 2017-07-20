from equipment.models import Equipment
from django import template


register = template.Library()


@register.inclusion_tag('cart.html')
def get_cart(request):
    cart = request.session.get('cart', [])
    equipment = Equipment.objects.filter(id__in=cart)
    return {'cart': equipment}
