from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings

from yvonneskitchen.Page.models import HomePage
from yvonneskitchen.Menu.models import MenuItem
from yvonneskitchen.forms import EstimateForm, WeeklySpecialForm

def home(request):
    context = {}
    context['page'] = 'home'
    page_variables = HomePage.objects.get(id=1)
    context['intro'] = page_variables.intro_statement
    context['food_description'] = page_variables.food_description
    context['estimate_form'] = EstimateForm(initial={'service_option': None, 'head_count': '# of People:', 'zip_code': 'Zip Code:'})
    context['weekly_special_form'] = WeeklySpecialForm(initial={'name': 'Name:', 'email_address': 'Email Address:'})
    context['special'] = MenuItem.objects.filter(weekly_special=True)[0]
    context['featured_items'] = MenuItem.objects.filter(featured=True)

    return render_to_response('home/home.html', context, context_instance=RequestContext(request))

def iframe(request, page):
    context = {}
    return render_to_response('iframe.html', context, context_instance=RequestContext(request))

def robots(request):
    return HttpResponse(open(settings.ROOT_PATH + '/robots.txt').read(), 'text/plain')
