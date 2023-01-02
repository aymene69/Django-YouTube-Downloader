from django.shortcuts import render
from django.http import HttpResponse
from .forms import RechercheDeezer
from pytube import YouTube
import os
import datetime

def index(request):
    return render(request, 'home/accueil.html')

def audio(request):
    if request.method == "POST":
        form = RechercheDeezer(request.POST)
        if form.is_valid():
            recherche = form.cleaned_data['recherche']
            yt = YouTube(recherche)
            titre = yt.title
            image = yt.thumbnail_url
            path = yt.streams.filter(type="audio").order_by("abr").desc()[0].download(('media'))
            filename = os.path.split(path)[1]
            autheur = yt.author
            afficher = True
            filename2 = titre.replace('#', '')
            os.system("ffmpeg -i 'media/" + filename + "' 'media/" + filename2 + ".mp3' -y")
            filename2 = filename2 + ".mp3"

    form = RechercheDeezer()
    try:
        if afficher == True:
            return render(request, 'home/download.html', {'autheur': autheur, 'titre': titre, 'filename': filename, 'image': image, 'filename2': filename2})
    except:
        return render(request, 'home/index1.html', {'form': form})

def video(request):
    if request.method == "POST":
        form = RechercheDeezer(request.POST)
        if form.is_valid():
            recherche = form.cleaned_data['recherche']
            debut = form.cleaned_data['debut']
            fin = form.cleaned_data['fin']
            if debut == fin:
                try:
                    yt = YouTube(recherche)
                    titre = yt.title
                    image = yt.thumbnail_url
                    yt.streams.filter(type="audio").order_by("abr").desc()[0].download(("media/"))
                    os.rename("media/" + yt.streams.filter(type="audio").order_by("abr").desc()[0].default_filename, 'media/audio.webm')
                    pathv = yt.streams.order_by('resolution').desc()[0].download(('media/'))
                    filename = os.path.split(pathv)[1]
                    autheur = yt.author
                    filename2 = titre.replace('#', '')
                    os.system("ffmpeg -i '" + pathv + "' -i 'media/audio.webm' -strict -2 -c:v copy -c:a copy 'media/" + filename2 + "_.mp4' -y")
                    filename2 = filename2 + "_.mp4"
                    afficher2 = True
                except:
                    return render(request, 'home/erreur.html')
            else:
                heure = datetime.datetime.strptime(debut, "%H:%M:%S").strftime('%M:%H:%S').datetime.datetime.strptime(fin, "%H:%M:%S").strftime('%M:%H:%S')
                yt = YouTube(recherche)
                titre = yt.title
                image = yt.thumbnail_url
                yt.streams.filter(type="audio").order_by("abr").desc()[0].download(("media/"))
                os.rename("media/" + yt.streams.filter(type="audio").order_by("abr").desc()[0].default_filename, 'media/audio.webm')
                pathv = yt.streams.order_by('resolution').desc()[0].download(('media/'))
                filename = os.path.split(pathv)[1]
                autheur = yt.author
                filename2 = titre.replace('#', '')
                os.system("ffmpeg -ss " + debut + " -i '" + pathv + "' -to " + fin + " -ss " + debut + " -i 'media/audio.webm' -to " + fin + " -strict -2 -c:v copy -c:a copy 'media/" + filename2 + "_.mp4' -y")
                filename2 = filename2 + "_.mp4"
                afficher2 = True

                
                    

    form = RechercheDeezer(initial={'debut': '00:00:00', 'fin': '00:00:00'})

    try:
        if afficher2 == True:
            return render(request, 'home/download2.html', {'autheur': autheur, 'titre': titre, 'filename': filename, 'image': image, 'filename2': filename2})
    except:
        return render(request, 'home/index.html', {'form': form})
