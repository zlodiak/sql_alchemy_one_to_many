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
session.add(Author(first_name='pushkin', last_name='alex'))

session.add(Book(title='war and peace', copyright='1880', author_id=1))
session.add(Book(title='anna karenina', copyright='1890', author_id=1))
session.add(Book(title='rudin', copyright='1870', author_id=2))
session.add(Book(title='oblomov', copyright='1860', author_id=10))

session.commit()


q = session.query(Author, Book).join(Author, Author.id == Book.author_id)
print(q, '\n')
for row in q:
    print(row.Author.first_name, row.Book.title, row.Book.copyright)
print('\n\n')



# OUTPUT:
# tolstoy war and peace 1880
# tolstoy anna karenina 1890
# turgenev rudin 1870





