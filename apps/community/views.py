from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Post, Reply


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'community/rooms.html', {'rooms': rooms})


def post_list(request, slug):
    room = get_object_or_404(Room, slug=slug)
    posts = room.posts.select_related('author').all()
    return render(request, 'community/posts.html', {'room': room, 'posts': posts})


def post_detail(request, slug, pk):
    room = get_object_or_404(Room, slug=slug)
    post = get_object_or_404(Post, pk=pk, room=room)
    post.views += 1
    post.save(update_fields=['views'])
    replies = post.replies.select_related('author').all()
    return render(request, 'community/thread.html', {'room': room, 'post': post, 'replies': replies})


@login_required
def create_post(request, slug):
    room = get_object_or_404(Room, slug=slug)
    if request.method == 'POST':
        post = Post.objects.create(
            room=room,
            author=request.user,
            title=request.POST.get('title', ''),
            content=request.POST.get('content', ''),
        )
        room.post_count += 1
        room.save(update_fields=['post_count'])
        return redirect('community:thread', slug=slug, pk=post.pk)
    return render(request, 'community/create_post.html', {'room': room})


@login_required
def create_reply(request, slug, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        Reply.objects.create(
            post=post,
            author=request.user,
            content=request.POST.get('content', ''),
        )
        return redirect('community:thread', slug=slug, pk=pk)
    return redirect('community:thread', slug=slug, pk=pk)
