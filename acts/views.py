from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from .models import Act
from .forms import ActForm, ActSetDateForm


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


@login_required
def create_act(request):
    if request.method == 'GET':
        form = ActForm()
        return render(request, 'acts/create_act.html', {'form': form})

    elif request.method == 'POST':
        form = ActForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user.id
            form.instance.user_id = user
            form.save()
            return HttpResponseRedirect('http://127.0.0.1:8000/acts/')
        else:
            return render(request, 'acts/create_post.html', {'form': form})


@login_required
def act(request, pkey):
    queryset = get_object_or_404(Act, pk=pkey)
    if request.user.type == 'DISPATCHER' or request.user.id == queryset.user_id:
        return render(request, 'acts/act.html', {'act': queryset})
    else:
        return render(request, 'no_access.html')


def act_search(request):
    if request.user.type == 'DISPATCHER':
        if request.method == 'POST':
            # any orm injections?
            search = request.POST['search']
            acts = Act.objects.all()
            queryset = [act for act in acts if (
                    (search.lower() in act.title.lower())
                    or
                    (search.lower() in act.adress.lower())
                    or
                    (search.lower() in act.text.lower()))
                        ]

            paginator = Paginator(queryset, 10)
            page_obj = paginator.get_page(None)
            return render(request, 'acts/details/act-search.html', {'page_obj': page_obj, 'search': search})

        if request.method == 'GET':
            search = request.GET['search']
            acts = Act.objects.all()
            queryset = [act for act in acts if (
                    (search.lower() in act.title.lower())
                    or
                    (search.lower() in act.adress.lower())
                    or
                    (search.lower() in act.text.lower()))
                        ]

            paginator = Paginator(queryset, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'acts/details/act-search.html', {'page_obj': page_obj, 'search': search})


def set_date(request, pkey):
    if request.user.is_staff == 1:
        if request.method == 'GET':
            queryset = Act.objects.filter(id=pkey).values_list('do_until', flat=True).first()

            form = ActSetDateForm()  # instance=queryset
            return render(request, 'acts/forms/date-form.html', {'form': form, 'act_id': pkey, 'date': queryset})
        if request.method == 'PUT':
            button_status = 'Дата выставлена'
            # TODO optimize queries
            queryset = get_object_or_404(Act, id=pkey)
            data = QueryDict(request.body).dict()
            form = ActSetDateForm(data, instance=queryset)
            if form.is_valid():
                form.save()

            return render(request, 'acts/details/act-accept.html', {'button_title': button_status})
