from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator

from yvonneskitchen.Menu.models import MenuItem
from yvonneskitchen.forms import EstimateForm

def menu(request):
    context = {}
    context['page'] = 'menu'
    context['estimate_form'] = EstimateForm(initial={'service_option': None, 'head_count': '# of People:', 'zip_code': 'Zip Code:'})
    p = Paginator(MenuItem.objects.filter(category='dinner'), 6)
    page = p.page(1)
    context['menu_page'] = page
    context['dinner_entrees'] = page.object_list
    context['menu_has_previous_page'] = page.has_previous()
    context['menu_has_next_page'] = page.has_next()
    p = Paginator(MenuItem.objects.all(), 6)
    page = p.page(1)
    context['selected_items'] = page.object_list
    context['selected_items_has_previous_page'] = page.has_previous()
    context['selected_items_has_next_page'] = page.has_next()

    return render_to_response('menu/menu.html', context, context_instance=RequestContext(request))
