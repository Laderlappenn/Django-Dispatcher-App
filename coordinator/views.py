from django.shortcuts import render

import random
from django.http import JsonResponse
from .models import Name

def random_name_page(request):

    return render(request, 'coordinator/names.html', {})

def random_name(request):
    names = ['John', 'Jane', 'Jim', 'Jessica', 'Jack']
    selected_name = random.choice(names)
    return JsonResponse({'name': selected_name})


# def random_name(request):
#     names = list(Name.objects.values_list('name', flat=True))
#     selected_name = random.choice(names)
#     return JsonResponse({'name': selected_name})