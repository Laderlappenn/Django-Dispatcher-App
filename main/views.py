from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator

from .forms import PostForm
from .models import Post


def main(request):
    queryset = Post.objects.all()

    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/main.html', {'page_obj': page_obj})


@staff_member_required
def create_post(request):

    if request.method == 'GET':
        form = PostForm()
        return render(request, 'main/create_post.html', {'form':form})

    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user = request.user.id
            form.instance.user_id = user
            form.save()
            return HttpResponseRedirect('../')
        else:
            return render(request, 'main/create_post.html', {'form': form})


def post(request, pkey):
    queryset = get_object_or_404(Post, pk=pkey)
    return render(request, 'main/post.html', {'post':queryset})



# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})