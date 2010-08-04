from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from yvonneskitchen.Page.models import HomePage
from yvonneskitchen.Menu.models import MenuItem
from yvonneskitchen.forms import EstimateForm, WeeklySpecialForm

def slideshow(request, item_id):
    context = {}
    if not request.session.get('estimate_form_service_option'):
        request.session['estimate_form_service_option'] = 'none'
    if not request.session.get('estimate_form_head_count'):
        request.session['estimate_form_head_count'] = ''
    if not request.session.get('estimate_form_zip_code'):
        request.session['estimate_form_zip_code'] = ''
    context['page'] = 'home'
    page_variables = HomePage.objects.get(id=1)
    context['intro'] = page_variables.intro_statement
    context['food_description'] = page_variables.food_description
    context['estimate_form'] = EstimateForm(initial={'service_option': request.session['estimate_form_service_option'], 'head_count': request.session['estimate_form_head_count'], 'zip_code': request.session['estimate_form_zip_code']})
    context['weekly_special_form'] = WeeklySpecialForm(initial={'name': 'Name:', 'email_address': 'Email Address:'})
    context['special'] = MenuItem.objects.filter(weekly_special=True)[0]
    context['featured_items'] = MenuItem.objects.filter(featured=True)[:7]
    context['selected_feature_item'] = MenuItem.objects.get(id=int(item_id))
    context['selected_feature_item_id'] = int(item_id)

    return render_to_response('home/home.html', context, context_instance=RequestContext(request))

def menu(request, section=None, page=None, estimate_page=None, estimate_form=None):
    context = {}
    if not request.session.get('estimate_list'):
        request.session['estimate_list'] = []
    if not request.session.get('estimate_computed'):
        request.session['estimate_computed'] = False
    if not request.session.get('estimate_total'):
        request.session['estimate_total'] = 0
    if not request.session.get('estimate_service_charge'):
        request.session['estimate_service_charge'] = 0
    if not request.session.get('estimate_form_service_option'):
        request.session['estimate_form_service_option'] = 'none'
    if not request.session.get('estimate_form_head_count'):
        request.session['estimate_form_head_count'] = ''
    if not request.session.get('estimate_form_zip_code'):
        request.session['estimate_form_zip_code'] = ''
    if not section:
        section = 'sides'
    if not page:
        page = 1
    if not estimate_page:
        estimate_page = 1
    context['page'] = 'menu'
    context['section'] = section
    if not estimate_form:
        context['estimate_form'] = EstimateForm(initial={'service_option': request.session['estimate_form_service_option'], 'head_count': request.session['estimate_form_head_count'], 'zip_code': request.session['estimate_form_zip_code']})
    else:
        context['estimate_form'] = estimate_form
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
    context['estimate_computed'] = request.session['estimate_computed']
    context['estimate_service_charge'] = request.session['estimate_service_charge']
    context['estimate_total'] = request.session['estimate_total']
    context['estimate_page'] = page_object
    context['selected_items'] = page_object.object_list
    context['selected_items_has_previous_page'] = page_object.has_previous()
    context['selected_items_has_next_page'] = page_object.has_next()

    return render_to_response('menu/menu.html', context, context_instance=RequestContext(request))

def menu_add_item(request, section, page, estimate_page, item_id):
    context = {}
    request.session['estimate_list'].append(item_id)
    request.session['estimate_computed'] = False

    return HttpResponseRedirect('/menu/%s/%s/%s/' % (section, page, estimate_page))

def menu_remove_item(request, section, page, estimate_page, item_id):
    context = {}
    request.session['estimate_list'].remove(item_id)
    request.session['estimate_computed'] = False

    return HttpResponseRedirect('/menu/%s/%s/%s/' % (section, page, estimate_page))

def menu_compute_estimate(request, section='sides', page=1, estimate_page=1):
    context = {}
    if request.method == 'POST':
        form = EstimateForm(request.POST)
        if not request.session.get('estimate_list'):
            request.session['estimate_list'] = []
        if form.is_valid():
            service_option = form.cleaned_data['service_option']
            request.session['estimate_form_service_option'] = service_option
            head_count = form.cleaned_data['head_count']
            request.session['estimate_form_head_count'] = head_count
            zip_code = form.cleaned_data['zip_code']
            request.session['estimate_form_zip_code'] = zip_code
            estimate_list = MenuItem.objects.filter(id__in=request.session['estimate_list'])
            total = 0
            for item in estimate_list:
                if item.per_person_item:
                    if item.weekly_special:
                        total = total + (item.special_price * head_count)
                    else:
                        total = total + (item.price * head_count)
                else:
                    if item.weekly_special:
                        total = total + item.special_price
                    else:
                        total = total + item.price
            if service_option == 'catered':
                total = total + 200
                request.session['estimate_service_charge'] = 200
            else:
                total = total + 100
                request.session['estimate_service_charge'] = 100
            request.session['estimate_computed'] = True
            request.session['estimate_total'] = total
            return menu(request, section=section, page=page, estimate_page=estimate_page, estimate_form=form)
        else:
            context['page'] = 'menu'
            context['section'] = section
            context['estimate_form'] = form
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
            context['estimate_computed'] = False
            context['estimate_page'] = page_object
            context['selected_items'] = page_object.object_list
            context['selected_items_has_previous_page'] = page_object.has_previous()
            context['selected_items_has_next_page'] = page_object.has_next()
            return render_to_response('menu/menu.html', context, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/menu/%s/%s/%s/' % (section, page, estimate_page))

def catering(request):
    context = {}
    context['page'] = 'catering'

    return render_to_response('catering/catering.html', context, context_instance=RequestContext(request))

def delivery(request):
    context = {}
    context['page'] = 'delivery'

    return render_to_response('delivery/delivery.html', context, context_instance=RequestContext(request))

def about(request):
    context = {}
    context['page'] = 'about'

    return render_to_response('about/about.html', context, context_instance=RequestContext(request))

def contact(request):
    context = {}
    context['page'] = 'contact'

    return render_to_response('contact/contact.html', context, context_instance=RequestContext(request))
