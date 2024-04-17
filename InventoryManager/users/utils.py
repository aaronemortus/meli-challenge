from django.http import HttpResponseForbidden
from django.views import View


class PermissionDeniedView(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self, request):
        """
        Override this method in subclasses to implement permission logic.
        """
        return True
    