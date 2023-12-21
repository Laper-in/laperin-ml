import re
from nltk.tokenize import RegexpTokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from fastapi import FastAPI

app = FastAPI()


@app.post("/text")
class TextPreprocessing:
    def __init__(self):
        # initialize tokenizer, stopwords, and stemmer
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stopwords_factory = StopWordRemoverFactory()
        #self.stemmer_factory = StemmerFactory()
        
        # initialize additional stopwords and remove 'tahu' from stopwords list
        self.additional_stopwords = ['cm', 'kg', 'gr', 'gram', 'ml', 'liter', 'blok', 'biji', 'pcs', 'ikat', 'jempol', 'ekor', 'siung', 'sejumput', 'batang', 'buah', 'potong', 'butir', 'btr', 'bonggol', 'balok', 'genggam', 'lembar', 'papan', 'sdt', 'sdm', 'paha', 'dada', 'filet', 'fillet', 'iris']
        self.stopwords = self.stopwords_factory.get_stop_words() + self.additional_stopwords
        self.stopwords.remove('tahu')

    def remove_brackets_text(self, text):
        '''Remove text inside brackets and brackets itself'''
        return re.sub(r'\([^)]*\)', '', text)

    def remove_brackets_text_list(self, list_content):
        '''Remove text inside brackets and brackets itself from list of text'''
        return [self.remove_brackets_text(i) for i in list_content]

    def tokenize(self, list_content):
        '''Tokenize sentences into words from list of sentences'''
        return [self.tokenizer.tokenize(i.lower()) for i in list_content]

    def remove_stopwords(self, list_content):
        '''Remove stopwords from list of words in list of contents'''
        return [[j for j in i if j not in self.stopwords] for i in list_content]

    def remove_non_alpha(self, list_content):
        '''Remove non-alphabetic characters from list of words in list of contents'''
        return [[j for j in i if j.isalpha()] for i in list_content]
    
    def sql_query_to_list(self, sql_result):
        '''Convert SQL query result to 1D list'''
        list_2d = [list(x) for x in sql_result]
        list_1d = [s for S in list_2d for s in S]

        return list_1d
    
    def list1d_to_string(self, list_content):
        '''Convert list of words to string'''
        return str(list_content).strip('[]')

    def clean_doc(self, list_content):
        '''convert list of list of words to list of string'''
        return [' '.join(map(str, x)) for x in list_content]

    def get_query(self, clean_doc):
        '''Get query content from combined query and content list'''
        return clean_doc[0]

    def get_content(self, clean_doc):
        '''Get content from combined query and content list'''
        return clean_doc[1:]

    def combine_query_content(self, query, content):
        '''Combine query and content list in one list'''
        combined = content.copy()
        combined.insert(0, query)
        return combined
