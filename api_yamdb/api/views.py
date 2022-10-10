from django.views.generic.edit import CreateView

from .models import CustomUser


class AuthorCreateView(CreateView):
    model = CustomUser
    fields = ['email', 'username']
