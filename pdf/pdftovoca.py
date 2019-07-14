# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 18:55:35 2019

@author: JM
"""

import os
import re
import nltk
import numpy as np
from tqdm import tqdm
from collections import Counter
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.tokenize import sent_tokenize
from tkinter.filedialog import askopenfilename 
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter,resolve1
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter


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

    def word_Frequency(self):
        '''
        ===============================
        return : Counter object {'word' : 'freq'}
        '''
        
        f = open(self.output_path,"r")

        text = f.readline()

        # 단어의 빈도수
        shortword = re.compile(r'\W*\b\w{1,2}\b')
        text = shortword.sub('', text)

        stop_words = set(stopwords.words('english')) 
        word_tokens = word_tokenize(text)

        result = [] 

        # 불용어 제거
        for w in word_tokens: 
            if w not in stop_words: 
                parsing = ''.join([i for i in w if not i.isdigit()]) 
                parsing = re.sub('[-=+,#/\?:^$.@*\"※~&%}{ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', parsing)


                if parsing and parsing.isdigit() == False and len(parsing) > 2:
                    result.append(w)  

        cnt = Counter(result)
        
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

'''
input_path = ['C:/Users/JM/Desktop/MCNN.pdf','C:/Users/JM/Desktop/YOLO.pdf']

result = Counter('')
text_path = []


for path in input_path:
    pdf = preprocessing(path)
    output_path = pdf.pdf2txt()
    text_path.append(output_path)
    
    pdf.clean_text()
    cnt = pdf.word_Frequency()
    
    result += cnt
    
example = gen_example(text_path, result)
'''
