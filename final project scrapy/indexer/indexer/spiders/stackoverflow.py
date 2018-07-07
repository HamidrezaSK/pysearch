import scrapy

class StackSpider(scrapy.Spider):
    name = "StackSpider"

    def start_requests(self):
        url = "https://stackoverflow.com/questions/tagged/python?sort=votes&pagesize=50&page="
        for page in range(55,140):
            yield scrapy.Request(url=url+str(page), callback=self.question_list_parse)

    def question_list_parse(self,response):
        for question in response.xpath('*//a[@class="question-hyperlink"]/@href').extract():
            yield scrapy.Request(url='https://stackoverflow.com'+question, callback=self.question_parse)

    def question_parse(self,response):
        import nltk,re
        from nltk.corpus import stopwords
        sno = nltk.stem.SnowballStemmer('english')
        tags = ' '.join(response.xpath('//*[@id="question"]//a[contains(@class,"post-tag")]/text()').extract())
        question=' '.join(response.xpath('//*[@id="question"]//div[@class="post-text"]//p/text()').extract())
        title=response.xpath('*//div[@id="question-header"]//a[@class="question-hyperlink"]/text()').extract_first()
        yield {'url':response.url,'keyword':self.text_procces(tags+question+title)}

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
