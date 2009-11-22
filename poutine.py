
    #~POUTINE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #                                      #
    # It's a Web nano-framework in Python #
    #                                       #
    #~Enjoy!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import inspect
import sys
import os
import wsgiref.util as wsgi
from Cheetah.Template import Template
from sqlalchemy import *
import datetime
    
class Poutine:
    # sqlAlchemy :
    db = create_engine('mysql://root:@127.0.0.1:3306/questionlinks')
    db.echo = False  # Try changing this to True and see what happens
    metadata = MetaData(db) 
    questions = Table('questions', metadata, # questions model
        Column('id', Integer, primary_key=True),
        Column('question', String(255)),
        Column('sorting', Integer),
        Column('created', DateTime),
    )
    
    # poutine-related :
    environ = {}
    retval = {}
    def __init__(self, environ):
        self.environ = environ
        self.retval = { #or : 303 See Other , or 404 Not Found
            'output':'', \
            'status':'200 OK', \
            'location':'' \
        }
        
    def dispatch(self):
        qs = self.getquerystring()
        if qs.has_key('action'):
            if qs['action'] == 'index':
                # index :
                select = self.questions.select()
                questions = select.execute()
                nameSpace = {'title': 'Question Links', 'contents': 'index', 'questions':questions}
                print >> self.environ['wsgi.errors'], str(questions)
                self.retval['output'] = str(Template(file='index.tmpl', searchList=[nameSpace]))
            elif qs['action'] == 'add' :
                posted = self.getpost()
                if len(posted) > 0 :    # receive post :
                    # add some questions :
                    nameSpace = {'title': 'Question Links : Add a question', 'contents': 'Add a question in the form below :'}
                    i = self.questions.insert()
                    i.execute(question=posted['question'], created=datetime.datetime.now)
                    self.redirect('index')
                else:                   # normal get query :
                    nameSpace = {'title': 'Question Links : Add a question', 'contents': 'Add a question in the form below :'}
                    self.retval['output'] = str(Template(file='add.tmpl', searchList=[nameSpace]))
            else:
                self.retval['output'] = qs['action']
        else:
            self.respond404()

        return self.retval # Return the response Dictionary


    def getpath(self):
        return "\n".join(sys.path)

    def respond404(self):
        self.retval['status'] = '404 Not Found'
        self.retval['output'] = ''
        return self.retval

    def redirect(self, address):
        self.retval['output'] = ''
        self.retval['status'] = '303 See Other'
        self.retval['location'] = '?action='+address
        return self.retval

    def getquerystring(self):
        qs = self.environ['QUERY_STRING']
        return self.parse_qs(qs)

    def getkey(self, key):
        qs = self.environ['QUERY_STRING']
        return self.parse_qs(qs)[key]
        
    def getpost(self):
        try:
            request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = self.environ['wsgi.input'].read(request_body_size)
        # print >> self.environ['wsgi.errors'], str(self.parse_qs(request_body)) # debugging technique , more info at : http://code.google.com/p/modwsgi/wiki/DebuggingTechniques
        return self.parse_qs(request_body)

    def parse_qs(self, qs):
        """
        parse query string
        """
        if qs == '':
            return {}
        else:
            querylist = qs.split('&')
            if len(querylist) < 1 :
                return {}
            else:
                querydict = {}
                for item in querylist:
                    lis = item.split('=')
                    querydict[lis[0]] = lis[1]
                return querydict
