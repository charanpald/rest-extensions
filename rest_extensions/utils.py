from django.core.exceptions import PermissionDenied
from django.http import Http404


def get_model_object(Model, pk, user=None, permission=None):
    """
    Return a model instance if the user has the correct permission. If one of
    user or permission is unspecified then just return the object.
    """
    try:
        obj = Model.objects.get(pk=pk)
    except Model.DoesNotExist:
        raise Http404("Missing object with id: " + pk)

    if user is None or permission is None:
        return obj
    elif user.has_perm(permission, obj):
        return obj
    else:
        raise PermissionDenied
