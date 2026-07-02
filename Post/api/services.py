from .models import Like
def toggle_like(user, post):
    like = Like.objects.filter(post=post, author=user).first()

    if like:
        like.is_active = not like.is_active
        like.save()
        return like

    return Like.objects.create(post=post, author=user, is_active=True)
