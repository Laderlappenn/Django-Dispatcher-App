from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from acts.models import Act
from django.http import JsonResponse
# from .forms import ActForm, ActSetDateForm
from django.contrib.auth import get_user_model

@login_required
def acts(request):
    if request.user.type == 'DISPATCHER':
        queryset = Act.objects.select_related('user').all().order_by('-date_updated')
    else:
        queryset = Act.objects.select_related('user').filter(
            user_id=request.user.id)  # request.session.get('_auth_user_id')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'acts/act_list.html', {'page_obj': page_obj})

def accept(request, pkey):
    user_id = request.user.id
    executer = get_user_model().objects.get(id=user_id)
    try:
        act = get_object_or_404(Act, id=pkey)
        act.executer_id = executer  # replace field_name and new_value with the appropriate values
        act.save()
    except Act.DoesNotExist:
        return JsonResponse({'act': "not found"})

    return render(request, 'acceptor/button.html', {})