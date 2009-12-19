from poutine import Poutine
from sqlalchemy import *
from Cheetah.Template import Template
import urllib
import datetime


class App(Poutine):
	# sqlAlchemy :
	db = create_engine('mysql://root:@127.0.0.1:3306/questionlinks')
	db.echo = False  # set to True to see the SQL output in the terminal
	metadata = MetaData(db) 
	questions = Table('questions', metadata, # questions model
		Column('id', Integer, primary_key=True),
		Column('question', String(255)),
		Column('sorting', Integer),
		Column('created', DateTime),
	)
	def __init__(self, environ):
		Poutine.__init__(self, environ)
		
	# sqlAlchemy :
	db = create_engine('mysql://root:@127.0.0.1:3306/questionlinks')
	db.echo = False  # set to True to see the SQL output in the terminal
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

	


	# ACTIONS :
	def index(self):
		select = self.questions.select()
		questions = select.execute()
		nameSpace = {'title': 'Question Links', 'contents': 'index', 'questions':questions}
		print >> self.environ['wsgi.errors'], str(questions)
		return str(Template(file='index.tmpl', searchList=[nameSpace]))
	
	def testing(self):
		return 'Hello lalalalalaa'
	
	def test(self):
		nameSpace = {
			'title': 'Testing page', 
			'contents':'testing',
			'debugval':self.environ
			}
		return str(Template(file='test.tmpl', searchList=[nameSpace]))

	def add(self):
		posted = self.getpost()
		if len(posted) > 0 :	# receive post :
			# add some questions :
			nameSpace = {'title': 'Question Links : Add a question', 'contents': 'Add a question in the form below :'}
			i = self.questions.insert()
			i.execute(question=urllib.unquote_plus(posted['question']), created=datetime.datetime.now)
			self.redirect('index')
			return '' # must return a string, otherwise it triggers this : TypeError: object of type 'NoneType' has no len()
		else:				   # normal get query :
			nameSpace = {'title': 'Question Links : Add a question', 'contents': 'Add a question in the form below :'}
			return str(Template(file='add.tmpl', searchList=[nameSpace]))
	
	def delete(self):
		
		return self.qs['id']
