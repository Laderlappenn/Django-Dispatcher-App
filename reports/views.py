from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from accounts.models import Account



@login_required
def users(request):
    if request.user.type == 'DISPATCHER':
        queryset = Account.objects.all().order_by('username')
        paginator = Paginator(queryset, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'reports/reports.html', {"page_obj": page_obj})
