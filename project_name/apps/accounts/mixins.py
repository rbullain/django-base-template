from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin


class RedirectAuthenticatedMixin:
    """Redirect the user if authenticated."""
    redirect_url = None

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_url is None:
            raise ImproperlyConfigured(
                '{0} is missing the redirect_url attribute. Define {0}.redirect_url, or override '
                '{0}.dispatch().'.format(self.__class__.__name__)
            )
        if request.user.is_authenticated:
            if self.redirect_url == request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that your"
                    "redirect_url doesn't point to the {0} page.".format(self.__class__.__name__)
                )
            return HttpResponseRedirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
