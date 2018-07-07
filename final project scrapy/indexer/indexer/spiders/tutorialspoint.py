import scrapy 

class TutorSpider(scrapy.Spider):
    name = "TutorSpider"

    def start_requests(self):
        url = 'https://www.tutorialspoint.com/python3/index.htm'
        yield scrapy.Request(url=url , callback = self.index_parse)
    def index_parse(self,response):
        for doc in response.xpath('*//aside[@class="sidebar"]//a/@href').extract():
            yield scrapy.Request(url = 'https://www.tutorialspoint.com'+doc , callback = self.doc_parse)
    def doc_parse(self,response):
        body=response.xpath('*//div[@class="col-md-7 middle-col"]')
        title = body.xpath('//h1/text()').extract()[-1]
        text = ' '.join(body.xpath('//p').extract()[:-1])
        yield {'url':response.url,'keyword':self.text_procces(text+title)}

    def text_procces(self,sentence):
        import nltk,re
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

