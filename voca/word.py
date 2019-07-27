import re
import requests
from bs4 import BeautifulSoup

# 단어를 넣으면 뜻을 받아 옴
def getMeaning(word):
    if not word:
        return ""
    addr = "http://dic.daum.net/search.do?q=" + word + '&dic=eng'
    
    req = requests.get(addr)
    req.encoding = "utf-8"

    soup_raw = BeautifulSoup(req.text, "html.parser")
    #print(soup_raw)
    
    # 특정 검색의 경우, js를 사용하여 redirect 되기도 한다.
    # 이때는 단어의 번호(word_key)를 코드에서 찾아낼 수 있다.
    # 이것을 이용하여 특정한 경우에는 주소를 다시 바꾸어 크롤링한다.
    word_key = re.compile("((kew)|(ekw))\d{9}").search(soup_raw.text)         # 매칭되는 케이스가 있는지 검색한다
    if word_key:
        #print(word_key)
        addr = "http://dic.daum.net/word/view.do?wordid=" + word_key.group() + "&q=" + word       # 검색 결과로 redirect되는 주소를 알아낸다
        req = requests.get(addr)
        soup_raw = BeautifulSoup(req.text, "html.parser")
    
    search_word = soup_raw.find(class_= re.compile("txt_clean"))
    if not search_word:
        # 검색에 실패한 경우
        return

    soup = soup_raw.find(class_="search_box")
    search_list = None
    if not soup:
        # 페이지 형식이 다른 경우
        soup = soup_raw.find(class_="inner_top")

        # 검색 결과가 없는 경우
        if not soup:
            return
        search_list = soup.find(class_="list_mean").find_all(class_="txt_mean")

    else:    
        search_list = soup.find(class_="list_search").find_all(class_="txt_search")
        
    result = ''

    for mean in search_list:
        result += mean.text + ", "
    
    return result.strip(', ')
