
# views.py
# I have created this file - Harry
from django.http import HttpResponse
from django.shortcuts import render
from spellchecker import SpellChecker
import nltk
from nltk.tokenize import word_tokenize
from textblob import TextBlob

def index(request):
    return render(request, 'index.html')

    # return HttpResponse("Home")
def ex1(request):
    sites = ['''<h1>For Entertainment  </h1> <a href="https://www.youtube.com/"> Youtube Videos</a> ''',
             '''<h1>For Interaction  </h1> <a href="https://www.facebook.com/"> Facebook</a> ''',
             '''<h1>For Insight  </h1> <a href="https://www.ted.com/talks"> Ted Talks</a> ''',
             '''<h1>For Internship  </h1> <a href="https://www.internshala.com">Internship</a> ''']
    return HttpResponse((sites))
def analyze(request):
    #Get the text
    djtext = request.POST.get('text', 'default')

    # Check checkbox values
    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    vocabulary_correction = request.POST.get('vocabulary_correction', 'off')

    # Initialize the spell checker
    spell = SpellChecker()

    # Apply transformations unconditionally
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    analyzed = djtext  # Initialize with the original text

    if removepunc == "on":
        analyzed = "".join(char for char in analyzed if char not in punctuations)

    if fullcaps == "on":
        analyzed = analyzed.upper()

    if extraspaceremover == "on":
        analyzed = " ".join(analyzed.split())

    if newlineremover == "on":
        analyzed = analyzed.replace("\n", " ")

    if vocabulary_correction == "on":
        # Split the text into words and correct misspelled words
        text_blob = TextBlob(analyzed)
        corrected_words = []

        for word in text_blob.words:
            corrected_word = word.correct()
            if word != corrected_word:
                suggestions = word.spellcheck()
                corrected_words.append(f"{corrected_word} (Suggestions: {', '.join(suggestion[0] for suggestion in suggestions)})")
            else:
                corrected_words.append(word)

        # Reconstruct the text with corrected words and suggestions
        analyzed = " ".join(corrected_words)
    params = {'purpose': 'Text Analysis', 'analyzed_text': analyzed}
    return render(request, 'analyze.html', params)

    
    

def capfirst(request):
    return HttpResponse("capitalize first")

def newlineremove(request):
    return HttpResponse("newline remove first")


def spaceremove(request):
    return HttpResponse("space remover <a href='/'>back</a> ")

def charcount(request):
    return HttpResponse("charcount ")

# urls.py
"""textutils URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

