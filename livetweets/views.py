from django.shortcuts import render


def livetweets(request):

    return render(request, "livetweets.html")

