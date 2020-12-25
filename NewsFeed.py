from urllib.parse import quote
import feedparser
from bs4 import BeautifulSoup
from newspaper import Article
from newspaper import Config
import pandas as pd
from TalkAudio import TalkAudio

class NewsFeed():
'''
The NewsFeed class takes in a search term, number of entries(default=5), extensive flag(default=True) adn reads out via audio
the required news articles related to the search term.
Attributes
    ----------
    search : str
        search term as input (default 'stock market')
    extensive : boolean
        flaf to read out complete news article or only summary (default True)
    n_entries : int
        the number of news entries to red out (default 5)
'''
    def __init__(self, search='stock market',n_entries=5,extensive=True):
        self.search = search
        self.n_entries = n_entries
        self.extensive = extensive
        self.feed_url = "http://news.google.com/news?q={}&hl=en-US&sort=date&gl=US&num={}&output=rss".format(quote(self.search),self.n_entries)
        self.config = Config()
        self.config.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        self.talkaudio = TalkAudio()
        
    def clean(self, html):
    	'''
		Attributes
    	----------
    	html : str
        	html input to parse

        Returns the text from html.
    	'''
        soup = BeautifulSoup(html,features='lxml')
        text = soup.get_text()
        text = text.replace('\xa0', ' ')
        return text

    def parse(self):
    	'''
        Parses and returns the news entries as list from the given url.
    	'''
        feeds = feedparser.parse(self.feed_url).entries
        newsentries = []
        ind = 0
        while(ind < self.n_entries):
            entry = {
                'Description': self.clean(f.get("description", "")),
                'Date': f.get("published", ""),
                'Title': f.get("title", ""),
                'Link': f.get("link", "")
            }
            newsentries.append(entry)
            ind+=1
        return newsentries
    
    def get_article_text(self,newsitem):
    	'''
		Attributes
    	----------
    	newsitem : list
        	list containing the news entries

        Returns the text for each news entries.
    	'''
        article = Article(newsitem['Link'],config=self.config)
        article.download()
        article.parse()
        article.nlp()
        return article.text if self.extensive==True else article.summary
            
    def read_out(self):
    	'''
    	Reads out the news articles one by one.
    	'''
        news = self.parse()
        if(len(news)==0):
            print('No news articles found for the topic {}. Try again later'.format(self.search))
            self.talkaudio.talk('No news articles found for the topic {}. Try again later'.format(self.search))
            return
        print('Top headlines for {}'.format(self.search))
        self.talkaudio.talk('Top headlines for {}'.format(self.search))
        count=1
        for item in news:
            print('\nArticle number {}\n'.format(count))
            self.talkaudio.talk('Article number {}'.format(count))
            print(item['Title']+'\n')
            self.talkaudio.talk(item['Title'])
            self.talkaudio.talk(self.get_article_text(item))
            count+=1