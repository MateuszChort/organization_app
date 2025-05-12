from crum import get_current_user


def apply_user_context(instance):
    user = get_current_user()
    if user and not user.pk:
        user = None
    if getattr(instance, "created_at", None):
        instance.modified_by = user
    else:
        instance.created_by = getattr(instance, "created_by", user)

    return instance
