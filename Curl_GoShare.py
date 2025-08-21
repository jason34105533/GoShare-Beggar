import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

HOST_LINK = "https://www.ptt.cc/bbs"
SECTION = "Lifeismoney"
QUEST = "goshare"

ATTACH_LINK = "https://go.ridegoshare.com"

DO_SEARCH = True
DO_ATTACH = True


SEARCH_PAGE = (HOST_LINK + "/" + SECTION + "/search?q=" + QUEST) if (DO_SEARCH == True) else (HOST_LINK + "/" + SECTION + "/index.html")


def Retreive_Text(link: str) -> str:
    response = requests.get(link)

    if(response.status_code == requests.codes.ok):
        soup = BeautifulSoup(response.text, 'html.parser')
        
    soup = soup.find("div", class_="bbs-screen bbs-content")

    for meta in soup.find_all("div", class_=["article-metaline", "article-metaline-right", "push"]):
        meta.decompose()

    for meta in soup.find_all("span"):
        meta.decompose()
        
    return soup.text.strip()
 
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
                
    return article_link, article_title

def Mail_It(Title: str ,Content: str) -> set :
    
    Content = (Content + "\n\n" + ATTACH_LINK)if DO_ATTACH else Content

    # xnhe dhkt ysia srne
    msg = MIMEText(Content, 'plain', 'utf-8') # 郵件內文
    # msg['Subject'] = '快搶！ 有新的GoShare優惠卷！'            # 郵件標題
    msg['Subject'] = Title            # 郵件標題
    msg['From'] = 'GoShare Beggar'                  # 暱稱或是 email
    msg['To'] = 'a20040108jason@gmail.com'   # 收件人 email
    # msg['Cc'] = 'a20040108jason@gmail.com'   # 副本收件人 email ( 開頭的 C 大寫 )
    # msg['Bcc'] = 'a20040108jason@gmail.com'  # 密件副本收件人 email

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('a20040108jason@gmail.com','xnhedhktysiasrne')
    status = smtp.send_message(msg)    # 改成 send_message
    if status == {}:
        print('郵件傳送成功！')
    else:
        print('郵件傳送失敗！')
    smtp.quit()

def CheckNewPost(Titles :list, Links: list, Link_Set: set) :
    for (title, link) in zip(Titles, Links):
        if(link not in Link_Set):
            tmp_Content = Retreive_Text(link)
            Mail_It(title, tmp_Content)
            Link_Set.add(link)
    
    return Link_Set

Links, Titles = Curl_LinkAndTitle(SEARCH_PAGE)

Content_of_1 = Retreive_Text(Links[0])
Title_of_1 = Titles[0]

print([Title_of_1, Content_of_1])

Link_Set = set({'https://www.ptt.cc/bbs/Lifeismoney/M.1754649135.A.018.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1750074707.A.EC4.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1752833242.A.509.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1752030784.A.B2F.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1751022759.A.72F.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1753438483.A.1D1.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1752240299.A.6E5.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1754039089.A.D23.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1752980809.A.486.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1752624603.A.4B9.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1751900624.A.530.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1751627929.A.43B.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1755252333.A.475.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1752390321.A.DAE.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1754205551.A.400.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1751548003.A.5FF.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1751282995.A.DDC.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1751469142.A.B51.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1752834550.A.AC6.html', 'https://www.ptt.cc/bbs/Lifeismoney/M.1750414475.A.E9C.html'})
# Link_Set = CheckNewPost(Titles, Links, Link_Set)

print(Link_Set)

Mail_It(Title_of_1, Content_of_1)

