from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.musinsa.com/")  

bsObject = BeautifulSoup(html, "html.parser") 


print(bsObject) # 웹 문서 전체가 출력됩니다. 