from django.shortcuts import render, redirect

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from interfapp.models import Document
from interfapp.forms import DocumentForm

#from .xml_module import *

def choose_file(request):
    return render(request, 'interfapp/choose_file.html', {})


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.process()
            documents = Document.objects.all()
            # Redirect to the document list after POST
            return render(request, 'interfapp/list.html', #HttpResponseRedirect(reverse('interfapp.views.list'),tuple())
            {'documents': documents, 'form': form})
    else:
        form = DocumentForm() # A empty, unbound form

        # Load documents for the list page
        documents = Document.objects.all()

        # Render list page with the documents and the form
        return render(
            request,
            'interfapp/list.html',
            {'documents': documents, 'form': form}
        )

def delete_doc(request, doc_id=None):
    objet = Document.objects.get(id=doc_id)
    objet.erase()
    return redirect("/list")

def graph(request, doc_id=None):
    return render(request, "interfapp/xmltograph.html", {})

