import re
import time
import requests
from bs4 import BeautifulSoup

## urlを入力して本文を取り出す
def get_Honbun(novel_url, headers):

    honbun_corpus = {}
    
    novel_url = 'https://ncode.syosetu.com/N4212GT'
    novel_req = requests.get(novel_url,headers = headers)
    novel_soup = BeautifulSoup(novel_req.text, 'html.parser')

    html = novel_soup.select("dd.subtitle")
    update = novel_soup.select("dt.long_update")

    title_list = [each.find("a").text for each in html]
    page_list = [f"https://ncode.syosetu.com{each.find('a').get('href')}" for each in html]

    for i in range(len(page_list)):
        time.sleep(0.1)
        page_url = page_list[i]
        page_req = requests.get(page_url,headers = headers)
        page_soup = BeautifulSoup(page_req.text, 'html.parser')
        p = page_soup.find_all("p",id=re.compile("^L.*"))
        text = "\n".join([each.text for each in p if each.text!=""]).strip()

        honbun_corpus[title_list[i]] = text 
    
    return honbun_corpus


## 小説の感想コメントを取り出す
def get_Comments(novel_url,headers):
    req = requests.get(novel_url,headers=headers)
    soup = BeautifulSoup(req.text,"html.parser")

    comment_url = re.findall('https://.+?感想',str(soup.find('ul',id='head_nav')))[0].replace('">感想','')
    comment_req = requests.get(comment_url, headers=headers)
    comment_soup = BeautifulSoup(comment_req.text,"html.parser")

    contents = []

    if comment_soup.select("div.waku"):
        try:
            head = comment_soup.find('div',class_='naviall').find_all('a')
            if head[-1].text == "Next >>":
                final_page = head[-2].text
            elif head[-1].text == "1":
                final_page = head[-1].text
            else:
                final_page = head[-1].text.replace('[','').replace(']','')

        except Exception as e:
            final_page = "1"

        print("final_page:",final_page)


        for i in range(int(final_page)):
            page_url= comment_url + '?p=' + str(i+1)
            time.sleep(0.1)
            page_req = requests.get(page_url,headers=headers)
            page_soup = BeautifulSoup(page_req.text,"html.parser")

            waku = page_soup.select("div.waku")

            for each in waku:
                dic = {}
                h2 = [h.text.strip() for h in each.select("div.comment_h2")]
                comments = [com.text.strip() for com in each.select("div.comment")]
                info = each.find('div',class_='comment_info').text.strip()
                dic["info"] = info
                if not each.select('div.res'):
                    for i in range(len(h2)):
                        dic[h2[i]] = comments[i]
                else:
                    comment = []
                    response = []
                    res_comment = [res.text.strip() for res in each.find('div',class_='res').select("div.comment")]
                    for each in comments:
                        if each not in res_comment:
                            comment.append(each)
                        else:
                            response.append(each)
                    try:
                        for i in range(len(h2)):
                            dic[h2[i]] = comment[i]
                        dic["response"] = "\n".join(response)
                    except Exception as e:
                        dic = {}

                contents.append(dic)
    else:
        pass

    return contents