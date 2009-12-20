import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relation, backref

# sqlAlchemy :
Base = declarative_base()
db = create_engine('mysql://root:@127.0.0.1:3306/questionlinks')
db.echo = True  # set to True to see the SQL output in the terminal
Session = sessionmaker(bind=db)
session = Session()


class Question(Base):
	__tablename__ = 'questions'
	id = Column('id',Integer, primary_key=True)
	question = Column(String)
	sorting = Column(Integer)
	created = Column(String)
	answers = relation("Answer", backref="question", order_by = "Answer.id",cascade="all")
	def __init__(self, question, sorting=0, created=str(datetime.datetime.now)):
		self.question = question
		self.sorting = sorting
		self.created = created
	def __repr__(self):
		return "<Question('%s','%s','%s')>" % (self.question, self.sorting, self.created)

class Answer(Base):
	__tablename__ = 'answers'
	id = Column('id',Integer, primary_key=True)
	answer_link = Column(String)
	answer_text = Column(Text)
	sorting = Column(Integer)
	created = Column(String)
	question_id = Column('question_id',Integer, ForeignKey('questions.id'))
	def __init__(self, question_id, answer_link='', answer_text='', sorting=0, created=str(datetime.datetime.now)):
		self.answer_link = answer_link
		self.answer_text = answer_text
		self.sorting = sorting
		self.created = created
		self.question_id = question_id
	def __repr__(self):
		return "<Answer('%s','%s','%s','%s','%s')>" % (self.answer_link, self.answer_text, self.sorting, self.created, self.question_id)


if __name__ == '__main__':
	questions = session.query(Question).order_by(Question.id).first()
	for an in questions.answers:
		print an