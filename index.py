import random
from sqlalchemy import create_engine, Table, MetaData, select, Column, String, Integer, SmallInteger, ForeignKey
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///db.sqlite3')
connection = engine.connect()
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    # books = relationship("Book")
 

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    copyright = Column(SmallInteger, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))


Author.__table__.create(engine)
Book.__table__.create(engine)


session.add(Author(first_name='tolstoy', last_name='lev'))
session.add(Author(first_name='turgenev', last_name='ivan'))

session.add(Book(title='war and peace', copyright='1880', author_id=1))
session.add(Book(title='anna karenina', copyright='1890', author_id=1))
session.add(Book(title='rudin', copyright='1870', author_id=2))

session.commit()


authors_result = []
authors = session.query(Author).all()
for author in authors:
    authors_result.append({'id': author.id, 'first_name': author.first_name})


books = session.query(Book).all()
for book in books:
    author = next(filter(lambda a: a['id'] == book.author_id, authors_result))
    print(book.id, book.title, book.copyright, author['first_name'])





