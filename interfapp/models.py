from django.db import models
import os

from .xml_module import *

class Document(models.Model):
        docfile = models.FileField(upload_to='documents/')
        xmlurl = models.TextField()
        rdfurl = models.TextField()
        
        def process(self):
            print(os.getcwd())
            dirname = 'interfapp/media/documents/'
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            #f = open(dirname+self.docfile.name.split('.')[0]+'.xml', 'w')
            #f.write('XML succeed in writing')
            #f.close()
            self.xmlurl = dirname+self.docfile.name.split('.')[0]+'.xml'
            f = open(dirname+self.docfile.name.split('.')[0]+'.rdf', 'w')
            f.write('RDF succeed in writing')
            f.close()
            self.rdfurl = dirname+self.docfile.name.split('.')[0]+'.rdf'
            self.save()
            dirname = 'interfapp/media/'
            if self.docfile.name.split('.')[1]=='wav' :
                wav_to_txt(dirname+self.docfile.name)
            txt_to_xml(dirname+self.docfile.name)
            print('FIN PROCESS, XML AND RDF WRITTEN')
            #self.save()

        def erase(self):
            dirname = 'interfapp/media/'
            print("Removing "+dirname+self.docfile.name)
            if os.path.exists(dirname+self.docfile.name):
                os.remove(dirname+self.docfile.name)
                os.remove(dirname+self.docfile.name.split('.')[0]+'.xml')
                os.remove(dirname+self.docfile.name.split('.')[0]+'.rdf')
                self.delete()
            else :
                print("Error")
