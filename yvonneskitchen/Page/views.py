from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from yvonneskitchen.Menu.models import MenuItem
from yvonneskitchen.forms import EstimateForm

def menu(request, section=None, page=None, estimate_page=None):
    context = {}
    context['page'] = 'menu'
    if not request.session.get('estimate_list'):
        request.session['estimate_list'] = []
    if not section:
        section = 'sides'
    context['section'] = section
    if not page:
        page = 1
    if not estimate_page:
        estimate_page = 1
    context['estimate_form'] = EstimateForm(initial={'service_option': None, 'head_count': '# of People:', 'zip_code': 'Zip Code:'})
    p = Paginator(MenuItem.objects.filter(category=section), 6)
    page_object = p.page(page)
    context['menu_page'] = page_object
    context['dinner_entrees'] = page_object.object_list
    context['menu_has_previous_page'] = page_object.has_previous()
    context['menu_has_next_page'] = page_object.has_next()
    estimate_list = MenuItem.objects.filter(id__in=request.session['estimate_list'])
    p = Paginator(estimate_list, 6)
    try:
        page_object = p.page(estimate_page)
    except (EmptyPage, InvalidPage):
        page_object = p.page(p.num_pages)
    context['estimate_page'] = page_object
    context['selected_items'] = page_object.object_list
    context['selected_items_has_previous_page'] = page_object.has_previous()
    context['selected_items_has_next_page'] = page_object.has_next()

    return render_to_response('menu/menu.html', context, context_instance=RequestContext(request))

def menu_add_item(request, section, page, estimate_page, item_id):
    context = {}
    request.session['estimate_list'].append(item_id)
    request.session.modified = True

    return HttpResponseRedirect('/menu/%s/%s/%s/' % (section, page, estimate_page))

def menu_remove_item(request, section, page, estimate_page, item_id):
    context = {}
    request.session['estimate_list'].remove(item_id)
    request.session.modified = True

    return HttpResponseRedirect('/menu/%s/%s/%s/' % (section, page, estimate_page))
