from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required()
def greeting_view(request):
    return HttpResponse("Welcome to Bookr, {}".format(request.user.username))
