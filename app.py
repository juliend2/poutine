from poutine import Poutine
from model import *
from Cheetah.Template import Template
import datetime
import urllib


class App(Poutine):
	def __init__(self, environ):
		Poutine.__init__(self, environ)

	# ACTIONS :
	def test(self):
		nameSpace = {
			'title': 'Testing page', 
			'subtitle':'testing',
			'debugval':self.environ
			}
		return str(Template(file='test.tmpl', searchList=[nameSpace]))
	
	def index(self):
		questions = session.query(Question).order_by(Question.id)
		nameSpace = {'title': 'Question Links', 'subtitle': 'Questions', 'questions':questions}
		session.commit()
		# print >> self.environ['wsgi.errors'], str(questions)
		return str(Template(file='index.tmpl', searchList=[nameSpace]))
	
	def add(self):
		posted = self.getpost()
		if len(posted) > 0 :	# receive post :
			# add some questions :
			q = Question(question=urllib.unquote_plus(posted['question']), created=str(datetime.datetime.now))
			session.add(q)
			self.redirect('index')
			return '' # must return a string, otherwise it triggers this : TypeError: object of type 'NoneType' has no len()
		else:				   # normal get query :
			nameSpace = {'title': 'Question Links : Add a question', 'subtitle': 'Add a question in the form below :'}
			return str(Template(file='add.tmpl', searchList=[nameSpace]))
	
	def delete(self):
		try: 
			question = session.query(Question).filter_by(id = self.qs['id']).one()
			session.delete(question)
			self.redirect('index')
			return ''
		except NoResultFound, e:
			return str(e)
		
	def addanswer(self):
		posted = self.getpost()
		if len(posted) > 0 :	# receive post :
			# add some answers :
			print >> self.environ['wsgi.errors'], str(posted['question_id'])
			a = Answer(answer_link=urllib.unquote_plus(posted['link']), question_id=int(posted['question_id']), answer_text=urllib.unquote_plus(posted['text']), created=str(datetime.datetime.now))
			session.add(a)
			self.redirect('index')
			return ''

	def deleteanswer(self):
		try: 
			answer = session.query(Answer).filter_by(id = self.qs['id']).one()
			session.delete(answer)
			self.redirect('index')
			return ''
		except NoResultFound, e:
			return str(e)
