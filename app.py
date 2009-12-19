from poutine import Poutine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from Cheetah.Template import Template
import urllib
import datetime

Base = declarative_base()
# sqlAlchemy :
db = create_engine('mysql://root:@127.0.0.1:3306/questionlinks')
db.echo = False  # set to True to see the SQL output in the terminal
Session = sessionmaker(bind=db)
session = Session()

class Question(Base):
	__tablename__ = 'questions'
	id = Column(Integer, primary_key=True)
	question = Column(String)
	sorting = Column(String)
	created = Column(String)
	def __init__(self, question, sorting=0, created=str(datetime.datetime.now)):
		self.question = question
		self.sorting = sorting
		self.created = created
	def __repr__(self):
		return "<Question('%s','%s', '%s')>" % (self.question, self.sorting, self.created)

class App(Poutine):
	
	# metadata = MetaData(db) 
	# questions = Table('questions', metadata, # questions model
	# 	Column('id', Integer, primary_key=True),
	# 	Column('question', String(255)),
	# 	Column('sorting', Integer),
	# 	Column('created', DateTime),
	# )
	
	def __init__(self, environ):
		Poutine.__init__(self, environ)

	# ACTIONS :
	def index(self):
		questions = session.query(Question)
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
			q = Question(question=urllib.unquote_plus(posted['question']), created=datetime.datetime.now)
			session.add(q)
			self.redirect('index')
			return '' # must return a string, otherwise it triggers this : TypeError: object of type 'NoneType' has no len()
		else:				   # normal get query :
			nameSpace = {'title': 'Question Links : Add a question', 'contents': 'Add a question in the form below :'}
			return str(Template(file='add.tmpl', searchList=[nameSpace]))
	
	def delete(self):
		try: 
			question = session.query(Question).filter_by(id = self.qs['id']).one()
			session.delete(question)
			self.redirect('index')
			return ''
		except NoResultFound, e:
			return str(e)
		
		
