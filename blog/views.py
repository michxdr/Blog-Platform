from django.shortcuts import render, get_object_or_404, redirect
from blog.forms import PostForm
from blog.models import Post, Category, Tag
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def post_list(request):
    posts = Post.objects.filter(status='published')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'posts': page_obj})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})


def post_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status='published', category=category)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status='published', tags=tag)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(status='published', title__icontains=query)
        return render(request, 'blog/post_list.html', {'posts': posts})
    else:
        return redirect('post_list')


