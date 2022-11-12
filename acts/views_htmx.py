from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import QueryDict
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Act
from .views import ActForm


@login_required
def act_edit_form(request, pkey):
    # TODO find out how to send less queries
    queryset = get_object_or_404(Act, pk=pkey)
    if request.user.type == 'DISPATCHER' or request.user.id == queryset.user_id:
        form = ActForm(instance=queryset)
        return render(request, 'acts/forms/edit-act-form.html', {'act': queryset, 'form': form})


@login_required
def act_edit(request, pkey):
    if request.method == 'PUT':
        # TODO find out how to send less queries
        queryset = get_object_or_404(Act, id=pkey)
        if request.user.type == 'DISPATCHER' or request.user.id == queryset.user_id:
            data = QueryDict(request.body).dict()
            form = ActForm(data, instance=queryset)
            if form.is_valid():
                form.save()
                Act.objects.filter(id=pkey).update(act_processing='Ожидание принятия заявки')
                return render(request, 'acts/details/act-detail.html', {'act': queryset})
            else:
                return render(request, 'acts/forms/edit-act-form.html', {'form': form})


def act_status(request):
    if request.user.type == 'DISPATCHER':
        status = request.GET.get('status')
        match status:
            case 'all':
                queryset = Act.objects.all().order_by('-date_updated')
            case 'completed':
                queryset = Act.objects.filter(completed=True)
            case 'uncompleted':
                queryset = Act.objects.filter(completed=False)
            case 'new':
                queryset = Act.objects.filter(act_processing='Ожидание принятия заявки')
            case 'expired':
                now = timezone.localtime(timezone.now())
                queryset = Act.objects.filter(do_until__lt=now).exclude(do_until=None)
            case _:
                queryset = Act.objects.all().order_by('-date_updated')

        paginator = Paginator(queryset, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'acts/details/act-status.html', {'page_obj': page_obj, 'status': status})

# change type of request?
def accept_or_return_act(request, pkey):
    if request.user.is_staff == 1:
        status = request.GET.get('status')
        if status == 'accept':
            Act.objects.filter(id=pkey).update(act_processing='Заявки принята')
            button_status = 'Заявка принята'
        else:
            Act.objects.filter(id=pkey).update(act_processing='Заявка возвращена')
            button_status = 'Заявка возвращена'

        return render(request, 'acts/details/act-accept.html', {'button_title': button_status})
