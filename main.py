#-*- coding:UTF-8 -*-
import requests
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

def get_detail_list(url):
  req = requests.get(url)

  pattern = re.compile(r'http://baijiahao.baidu.com\/s\?id=\d+')

  link_list = re.findall(pattern, req.text)

  return link_list

def get_detail_title(url):
  req = requests.get(url)

  title = re.search(r'<h2 class="index-module_articleTitle_28fPT">(.*?)</h2>', req.text).group(1)

  return title

if __name__ == '__main__':
    url = 'http://news.baidu.com/'

    detail_list = get_detail_list(url)

    title_list = []

    for i in detail_list:
      title_list.append(get_detail_title(i))

    mytext = " ".join(jieba.cut(str(title_list)))

    font = r'./simsun.ttf'

    wordcloud = WordCloud(background_color="white",font_path=font, width=1000, height=860, margin=2).generate(mytext)

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    wordcloud.to_file('test.png')

