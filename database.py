from sqlalchemy import create_engine
from sqlalchemy import Column, String,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

db_string = "postgres://patrick:Getting started@localhost:5432/database"

db = create_engine(db_string)
base = declarative_base()
with open("stack_2.json" , 'r') as f:
    datas = json.load(f)
#print(datas)
class search(base):
    __tablename__ = 'keywords_a'
    id = Column(Integer,primary_key=True,autoincrement=True)
    keyword = Column(String)
    urls = Column(String)

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

# # Create
# for i in range(10,20):
#     doctor_strange = search(id=i, keyword="python"+str(i), urls="mamanet")
#     session.add(doctor_strange)
# session.commit()

# Read

def adding_record(keyword , session,url,count):
    if not session.query(search).filter_by(keyword = keyword).first():
        user = search(keyword=keyword , urls = json.dumps({url : count}))
        session.add(user)
    else:
        query = session.query(search).filter_by(keyword = keyword).first()
        #print(query.urls)
        a = eval(query.urls)
        a[url] = count
        query.urls = str(a)
    session.commit()




for data in datas:
    for keyword in data['keyword']:
        adding_record(keyword,session,data['url'],data['keyword'][keyword])

a = session.query(search).filter_by(id = 0).first()

films = session.query(search)
for film in films:
    print(film.keyword)

# Update
# doctor_strange.urls = "Some2016Film"
# session.commit()

# # Delete
# session.delete(doctor_strange)
# session.commit()
#
# films = session.query(search)
# for film in films:
#     print()
#     print()
#     print(film.keyword)