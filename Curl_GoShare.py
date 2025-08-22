import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import json
import os
import datetime

# Curl Usage
HOST_LINK = "https://www.ptt.cc/bbs"
SECTION = os.environ.get("SECTION")
QUEST = os.environ.get("QUEST")

ATTACH_LINK = os.environ.get("ATTACH_LINK")

# Personal Info
MY_MAIL = os.environ.get("MY_MAIL")
SECURTIYCODE = os.environ.get("SECURTIYCODE")

# Options
DO_SEARCH = True
DO_ATTACH = True
DO_MAIL = True

SEARCH_PAGE = (HOST_LINK + "/" + SECTION + "/search?q=" + QUEST) if (DO_SEARCH == True) else (HOST_LINK + "/" + SECTION + "/index.html")

# Function Implementation
def Retreive_TextAndTimestamp(link: str) -> str:
    response = requests.get(link)

    if(response.status_code == requests.codes.ok):
        soup = BeautifulSoup(response.text, 'html.parser')
        
    Timestamp =  soup.find_all("span", class_="article-meta-value")[3].text.strip() # Suppose in this format : "Fri Aug 22 10:27:20 2025"
    
    soup = soup.find("div", class_="bbs-screen bbs-content")

    for meta in soup.find_all("div", class_=["article-metaline", "article-metaline-right", "push"]):
        meta.decompose()

    for meta in soup.find_all("span"):
        meta.decompose()
        
    return soup.text.strip(), Timestamp
 
 
# BS4 is used for parsing HTML and XML documents
def Curl_LinkAndTitle(SEARCH_PAGE :str) -> tuple :
    response = requests.get(SEARCH_PAGE)

    if(response.status_code == requests.codes.ok):
        soup = BeautifulSoup(response.text, 'html.parser')
        
    soup = soup.find_all("div", class_="title")

    article_title = []
    article_link = []
    for i in soup:
        if i:
            try:
                i = i.find("a")
                article_link.append("https://www.ptt.cc" + i["href"])
                article_title.append(i.text.strip())
                # print(i.name)
            except:
                article_link.append("Article Have been removed")
                article_title.append("Article Have been removed")
                
    return article_title, article_link


def Mail_It(Title: str ,Content: str, Timestamp: str) -> set :
    
    Content = (Timestamp + "\n\n" + Content + "\n" + ATTACH_LINK)if DO_ATTACH else (Timestamp + "\n\n" + Content)

    msg = MIMEText(Content, 'plain', 'utf-8') # 郵件內文
    # msg['Subject'] = '快搶！ 有新的GoShare優惠卷！'            # 郵件標題
    msg['Subject'] = Title            # 郵件標題
    msg['From'] = 'GoShare Beggar'                  # 暱稱或是 email
    msg['To'] = MY_MAIL   # 收件人 email
    # msg['Cc'] = MY_MAIL   # 副本收件人 email ( 開頭的 C 大寫 )
    # msg['Bcc'] = MY_MAIL  # 密件副本收件人 email

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(MY_MAIL,SECURTIYCODE)
    status = smtp.send_message(msg)    # 改成 send_message
    if status == {}:
        print('郵件傳送成功！')
    else:
        print('郵件傳送失敗！')
    smtp.quit()


def Check_NewPost(Titles :list, Links: list, Link_Set: set, Mail : bool) :
    for (title, link) in zip(Titles, Links):
        if((link not in Link_Set) and (link != "Article Have been removed")) :
            if Mail:
                tmp_Content, tmp_Timestamp = Retreive_TextAndTimestamp(link)
                Mail_It(title, tmp_Content, tmp_Timestamp)
            Link_Set.add(link)
    
    return Link_Set

def Load_Data():
    jsonFile = open(".store/history.json", "r")
    data = json.load(jsonFile)
    jsonFile.close()
    
    return {i["Link"] for i in data["data"]}


def Flush_Back(Titles :list, Links: list) :
    Dic = dict()
    Dic["updated_at"] = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    
    Data = []
    for (title, link) in zip(Titles, Links):
        Data.append({"Title" : title, "Link" : link})
        
    Dic["data"] = Data
    
    jsonFile = open('./.store/history.json','w', encoding="utf-8")
    json.dump(Dic, jsonFile, indent=4, ensure_ascii=False)
    jsonFile.close()
    
    
def INIT():
    if(os.path.exists(".store") == False):
        directory_name = ".store"
        os.mkdir(directory_name)
        

if __name__ == "__main__":

    INIT()
    Link_Set = Load_Data()
    
    Titles, Links = Curl_LinkAndTitle(SEARCH_PAGE)
    Link_Set = Check_NewPost(Titles, Links, Link_Set, DO_MAIL)

    Flush_Back(Titles, Links)