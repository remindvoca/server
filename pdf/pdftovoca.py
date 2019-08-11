# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 18:55:35 2019

@author: JM
"""

import os
import re
from tkinter.filedialog import askopenfilename 

from tqdm import tqdm
from collections import Counter
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter,resolve1
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

from urllib.request import urlopen
from bs4 import BeautifulSoup

'''
표제어 추출 : Lemmatization
1) stem(어간) : 단어의 의미를 담고있는 단어의 핵심 부분
2) affix(접사) : 단어에 추가적인 의미를 주는 부분
cats : cat(stem) + s(affix)

am -> be
the going -> the going
having -> have
'''

def lemma(word,part):
    n = WordNetLemmatizer()

    return n.lemmatize(word,part)

'''
어간 추출 : Stemming

am -> am
the going -> the go
having -> hav
'''
def stem(word):
    s = PorterStemmer()

    return s.stem(word)


def token(text,mode):
    if mode == 'sequence':
        token_list = sent_tokenize(text)
    elif mode == 'apostrophe':
        token_list = WordPunctTokenizer().tokenize(text)
    elif mode == 'hyphen':
        token_list = TreebankWordTokenizer().tokenize(text)
    else:
        token_list = word_tokenize(text)

    return token_list

def tag(token_list,lang='eng'):
    return pos_tag(token_list,lang=lang)

	
class preprocessing:
    def __init__(self, input_path, output_path=None):
        self.input_path = input_path
        self.output_path = output_path

    def isExistFile(self):
        file_name = self.output_path.split('/')[-1]

        for i in os.listdir("."):
            if file_name == i:
                return True

        return False

    def pdf2txt(self):
        '''
        =============================

        return : str, text File path
        '''

        # input
        password=''
        pagenos=set()
        maxpages=0

        # output
        imagewriter = None
        rotation = 0
        codec = 'UTF-8'
        pageno = 1
        scale = 1
        caching = True
        showpageno = True
        laparams = LAParams()

        infp = open(self.input_path,"rb")
        
        if self.output_path == None:
            self.output_path = self.input_path[:-4]+'_trans.txt'
            outfp = open(self.output_path,"w",encoding='UTF8')
        else:
            outfp = open(self.output_path,"w",encoding='UTF8')
            
            
        #page total num
        parser = PDFParser(infp)
        document = PDFDocument(parser)
        page_total_num = resolve1(document.catalog['Pages'])['Count']

        #
        rsrcmgr = PDFResourceManager(caching=caching)

        # pdf -> text converter
        device = TextConverter(rsrcmgr,
                               outfp,
                               codec=codec,
                               laparams=laparams, 
                               imagewriter=imagewriter)

        # pdf -> text interpreter
        interpreter = PDFPageInterpreter(rsrcmgr,device)

        # pdf -> text start
        with tqdm(total=page_total_num) as pbar:
            for page in PDFPage.get_pages(infp,
                                          pagenos,
                                          maxpages,
                                          password=password,
                                          caching=caching,
                                          check_extractable=True):

                page.rotate = (page.rotate+rotation) % 360     
                interpreter.process_page(page)

                pbar.update(1)

        print('[INFO] pdf -> text')

        outfp.close()
        infp.close()
        
        return self.output_path
    
    def clean_text(self):
        '''
        ==========================
        '''

        f = open(self.output_path,"rb")
        line_list = []

        while True:
            line = f.readline()
            line_list.append(line)
            if not line: break

        f.close()

        # remove nextline
        word = b" ".join(line_list).split()
        sentences = b" ".join(word)


        # remove ASCII
        # define pattern 
        pattern = re.compile(b"[\x80-\xff]")
        sentences = re.sub(pattern,b"",sentences)

        sentences = sentences.split(b". ")

        f = open(self.output_path,"wb")

        for sentence in sentences:
            sentence = sentence.replace(b"- ",b'')
            sentence = sentence.replace(b"-",b'')
            #cleaned_txt.append(sentence)
            f.write(sentence + b'. ')

        f.close()
        
        print('[INFO] clean text file')

    def return_without_easy_words(self,result):
        html = urlopen("https://opentutorials.org/module/825")
        bsObject = BeautifulSoup(html, "html.parser")
        contents = str(bsObject.find_all("div", attrs={"class": "entry-content"}))
        datalist = contents.split('\n')
        wordlists = []

        # Get easy words
        for data in datalist:
            if data[:3] != '<li':
                continue
            else:
                temp = data.split(' ', 1)
                if len(temp[0][4:]) > 0 and str(temp[0][4:]).isalnum() :
                    wordlists.append(temp[0][4:])
                else:
                    continue
        # print(wordlists)

        # Removing easy words in the result
        final_result = [each_result for each_result in result if each_result not in wordlists]

        return final_result

    def word_parsing(self,text):
	'''
	text : text
	=========================
	return : word list 
	'''
        stop_words = set(stopwords.words('english')) 
        word_tokens = word_tokenize(text)
        
        result = [] 

        # 불필요한 단어들 제거
        for w in word_tokens: 
            if w not in stop_words: 
                parsing = ''.join([i for i in w if not i.isdigit()]) 
                parsing = re.sub('[-=+,#/\?:^$.@*\"※~&%}{ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', parsing)

                if parsing and parsing.isalpha() == True:
                    if not re.findall('\d+', w):
                        w = w.lower()
                        w = lemma(w,'v')
                        
                        tok = token(w,'hyphen')
                        tags = tag(tok)
                        
                        '''
                        PRP는 인칭 대명사, VBP는 동사, 
                        RB는 부사, VBG는 현재부사, 
                        IN은 전치사, NNP는 고유 명사, 
                        NNS는 복수형 명사, CC는 접속사, DT는 관사
                        '''
                        
                        if tags[0][1] not in ['DT','PRP']:
                            result.append(w)
                            
        return result
		
    def word_Frequency(self):
        '''
        ===============================
        return : Counter object {'word' : 'freq'}
        '''
        
        f = open(self.output_path,"r")

        text = f.readline()

        shortword = re.compile(r'\W*\b\w{1,2}\b')
        text = shortword.sub('', text)

        result = self.word_parsing(text)  
        cnt = Counter(self.return_without_easy_words(result))
        
        print('[INFO] generation word frequency')
        
        return cnt
    
def gen_example(text_path, word_list):
    '''
    text_path : list, text file paths
    word : str, generate example
    
    ==================================
    
    return : dic {'word', 'sentence'}
    '''
    
    example = {}
    
    max_len = len(word_list)
    
    for path in text_path:
        f = open(path,"r")

        text = f.readline()
        
        sent_tokenize_list = sent_tokenize(text)
        
        for sentence in sent_tokenize_list:
            for word in word_list:
                if word in sentence:
                    example[word] = sentence
                    word_list.remove(word)
                    break
                
        if len(example) == max_len:
            break
                
    return example



if __name__ == "__main__":

    input_path = ['Hsueh, Li, Wu - 2018 - Stochastic Gradient Descent with Hyperbolic-Tangent Decay.pdf']

    result = Counter('')
    text_path = []


    for path in input_path:
        pdf = preprocessing(path)
        output_path = pdf.pdf2txt()
        text_path.append(output_path)

        pdf.clean_text()
        cnt = pdf.word_Frequency()

        result += cnt


    sorted_cnt = sorted(result.items(), key=lambda t: t[1], reverse=True)
    sorted_values = sorted(result.values(), reverse=True)
    sorted_keys = sorted(result, key=result.get, reverse=True)

    print(sorted_keys[:50])


    example = gen_example(text_path, sorted_keys[:50])
    print(example)

