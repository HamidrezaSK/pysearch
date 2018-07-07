from sqlalchemy import create_engine
from sqlalchemy import Column, String,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import json
db_string = "postgres://patrick:Getting started@localhost:5432/database"

db = create_engine(db_string)
base = declarative_base()

def text_procces(sentence):
    import nltk,re
    #nltk.download('stopwords')
    from nltk.corpus import stopwords
    sno = nltk.stem.SnowballStemmer('english')
    words_dic=dict()
    for word in re.split('[\W]',sentence):
        if word.lower() not in stopwords.words('english') and len(word)>1:
            if sno.stem(word) in words_dic:
                words_dic[sno.stem(word)]+=1
            else :
                words_dic[sno.stem(word)]=1
    return words_dic
class search(base):
    __tablename__ = 'keywords_a'
    id = Column(Integer,primary_key=True,autoincrement=True)
    keyword = Column(String)
    urls = Column(String)
Session = sessionmaker(db)
session = Session()
base.metadata.create_all(db)
# meta = sqlalchemy.MetaData()
# table = sqlalchemy.Table('keywords', meta, autoload=True, autoload_with=db)
# table.drop(db)
def get_query(processed_sentence):
    data = []
    for i in processed_sentence:
        query = session.query(search).filter_by(keyword=i).first()
        if query:
            urls = list(eval(query.urls).keys())
            data.append(urls)
    if data:
        urls = set(data[0])
    else:
        urls = set([])
    for i in data:
        urls = set(urls)&set(i)
    return urls
# def sort_urls(urls,):
#     sorted_urls = []
#     for i in urls:
def find_some(urls , keywords):
    answer = {}
    for url in urls:
        answer[url] = 0
        for keyword in keywords:
            if keyword != "python":
                query = session.query(search).filter_by(keyword=keyword).first()
                if query:
                    url_count = eval(query.urls)[url]
                    answer[url]+=url_count
    return answer


sentence = "python list sort get"
processed_sentence = text_procces(sentence)
urls = get_query(processed_sentence)
urls_dict = find_some(urls,list(processed_sentence.keys()))
urls_list = []
for i in urls_dict:
    urls_list.append([i,urls_dict[i]])
urls_list = sorted(urls_list,key=lambda k: k[1],reverse=True)
print(urls_list)


