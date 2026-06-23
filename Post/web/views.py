from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm
from .models import Comment
from .services import get_post


@login_required
def create_comment(request, post_pk):
    current_post = get_post(post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = current_post
            comment.save()

            return redirect(
                'post_detail',
                pk=current_post.pk
            )

    else:
        form = CommentForm()

    return render(
        request,
        'comment.html',
        {'form': form}
    )


@login_required
def edit_comment(request, post_pk, comment_pk):
    current_post = get_post(post_pk)

    comment = get_object_or_404(
        Comment,
        pk=comment_pk,
        author=request.user
    )

    if request.method == 'POST':
        form = CommentForm(
            request.POST,
            instance=comment
        )

        if form.is_valid():
            form.save()

            return redirect(
                'post_detail',
                pk=current_post.pk
            )

    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        'comment.html',
        {'form': form}
    )


@login_required
def delete_comment(request, post_pk, comment_pk):
    current_post = get_post(post_pk)

    comment = get_object_or_404(
        Comment,
        pk=comment_pk,
        author=request.user
    )

    comment.delete()

    return redirect(
        'post_detail',
        pk=current_post.pk
    )