from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from .models import Post, Comment, Reaction
from better_profanity import profanity
from django.urls import reverse

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'board/landing.html')

    posts = Post.objects.filter(status='Approved').order_by('-created_at').prefetch_related('comments', 'reactions')
    total_kindness = Post.objects.filter(status='Approved').count()

    leaderboard = User.objects.annotate(
        approved_posts_count=Count('post', filter=Q(post__status='Approved'))
    ).order_by('-approved_posts_count')[:5]

    return render(request, 'board/index.html', {
        'posts': posts,
        'total_kindness': total_kindness,
        'leaderboard': leaderboard
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'board/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')

@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get('content')
        image = request.FILES.get('image')
        category = request.POST.get('category', 'General')
        is_anon = 'is_anonymous' in request.POST

        if content:
            if profanity.contains_profanity(content):
                messages.error(request, "Your post contains inappropriate language. Let's keep it positive!")
                return render(request, 'board/create_post.html')

            Post.objects.create(
                user=request.user,
                content=content,
                image=image,
                category=category,
                is_anonymous=is_anon,
                status='Pending'
            )
            messages.success(request, "Post submitted! It will appear on the wall once approved by a moderator.")
            return redirect('index')

    return render(request, 'board/create_post.html')

@login_required
def add_reaction(request, post_id, r_type):
    post = get_object_or_404(Post, id=post_id, status='Approved')

    existing_reaction = Reaction.objects.filter(post=post, user=request.user).first()

    if existing_reaction:
        if existing_reaction.reaction_type == r_type:
            existing_reaction.delete()
        else:
            existing_reaction.reaction_type = r_type
            existing_reaction.save()
    else:
        Reaction.objects.create(post=post, user=request.user, reaction_type=r_type)

    return redirect(f"{reverse('index')}#post-{post.id}")

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id, status='Approved')
        text = request.POST.get('comment_text')

        if text:
            if profanity.contains_profanity(text):
                messages.error(request, "Inappropriate language blocked.")
            else:
                Comment.objects.create(post=post, user=request.user, comment_text=text)

        return redirect(f"{reverse('index')}#post-{post.id}")

    return redirect('index')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    return redirect('index')

