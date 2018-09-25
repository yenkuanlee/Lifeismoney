# -*- coding: UTF-8 -*-
# Kevin Yen-Kuan Lee 
import urllib2
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

UrlSet = set()
f = open('url.index','r')
while True:
    line = f.readline()
    if not line:
        break
    line = line.replace("\n","")
    line = line.split("\t")[0]
    UrlSet.add(line)
f.close()

def GetUinfo(Url):
    content = requests.get(
        url= Url,
        cookies={'over18': '1'}
    ).content.decode('utf-8')
    try:
        tmp = content.split("<div id=\"main-content\" class=")[1].split("<span class=\"article-meta-value\">")
        content = tmp[len(tmp)-1].split("</span></div>")[1].split("--\n<span class=\"f2\">")[0]
    except Exception as e:
        return str(e)
    return content

def send_email(recipient, subject, body):
    import smtplib
    user = ""
    pwd = ""
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        print 'successfully sent the mail'
    except Exception,e:
        print "failed to send mail"

def getLastPage(board):
        content = requests.get(
            url= 'https://www.ptt.cc/bbs/' + board + '/index.html',
        ).content.decode('utf-8')
        first_page = re.search(r'href="/bbs/' + board + '/index(\d+).html">&lsaquo;', content)
        if first_page is None:
            return 1
        return content,int(first_page.group(1)) + 1

ThisSet = set()
content0,pid = getLastPage("Lifeismoney")
tmp = content0.split("<div class=\"title\">")
for i in range(1,len(tmp),1):
    try:
        tmpp = tmp[i].split("<a href=\"")[1].split("</a>")[0].split("\">")
        lower_name = tmpp[1].lower()
        OO = tmp[i].split("<a href=\"")[1].split("</a>")[0].split("\">")
        url = "https://www.ptt.cc"+OO[0]
        title = OO[1]
        ThisSet.add(url+"\t"+title)
        if url not in UrlSet:
            send_email("yenkuanlee@gmail.com",title,url+"\n\n"+GetUinfo(url))
            #print "https://www.ptt.cc"+OO[0]+"\t"+OO[1]
    except:
        pass

fw = open('url.index','w')
for x in ThisSet:
    fw.write(x+"\n")
fw.close()
