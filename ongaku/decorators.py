from django.http import Http404
from functools import wraps

def owner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        obj = kwargs.get('obj')
        if not obj or obj.owner != request.user:
            raise Http404("このページは存在しません。")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
