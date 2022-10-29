import requests
from bs4 import BeautifulSoup
import json
from flask_mail import Message
from package.models import User
import pytz
import random
from datetime import datetime
from package import mail, userStrings
from flask_login import current_user


s = ""

def getAnsManually(block, index, url):
    try:
        global s
        e = json.loads(block.next)
        y = e['mainEntity']
        s += ("\n\n")
        s += ("Question "+ str(index)+ " : "+ y["name"] + "\n")
        s += ("\n\n")

        i = 1
        if "suggestedAnswer" in y:
            s += ("Suggested Answer: \n\n")
            for ans in y["suggestedAnswer"]:
                s += ("Ans "+ str(i)+ ":\n\n"+ ans["text"]+ "\n")
                s += ("\n\n")
                i += 1

        j = 1
        if "acceptedAnswer" in y:
            s += ("Accepted Answer: \n\n")
            ans = y['acceptedAnswer']
            s += ("Ans "+ str(j)+ ":\n\n"+ ans["text"]+ "\n")
            s += ("\n\n")

    except Exception as e:
        sendAckEmail(current_user, url)
        sendProblemEmail(current_user, url)
        s = ("Error occurred! The problem has been logged. \n\n      The details has been sent to Admin. You can expect a fix within 24 hours.")



def printAnsFromURL(url):
    global s
    s = ""
    prefix = "http://webcache.googleusercontent.com/search?q=cache:"
    full_url = prefix + url
    response = requests.get(full_url, headers={"User-Agent": str(random.choice(userStrings)).rstrip("\n")})
    soup = BeautifulSoup(response.text, "html.parser")
    titleBlock = soup.find("title")
    title = titleBlock.contents[0]
    if "Error 404 (Not Found)!!" in title:
        response = requests.get(url, headers={"User-Agent": str(random.choice(userStrings).rstrip("\n"))})
        soup = BeautifulSoup(response.text, "html.parser")

    res = soup.find(type="application/ld+json")
    try:
        y = json.loads(res.next)
        s += ("\n\n")
        s += ("Question "+ ": "+ y[0]["text"]+ "\n")
        s += ("\n\n")

        i = 1
        if "suggestedAnswer" in y[0]:
            s += ("Suggested Answer: \n\n")
            for ans in y[0]["suggestedAnswer"]:
                s += ("Ans "+ str(i)+ ":\n\n"+ ans["text"] + "\n")
                s += ("\n")
                i += 1

        j = 1
        if "acceptedAnswer" in y[0]:
            s += ("Accepted Answer: \n\n")
            for ans in y[0]["acceptedAnswer"]:
                s += ("Ans "+ str(j)+ ":\n\n"+ ans["text"] + "\n")
                s += ("\n\n")
                j += 1
    except Exception as e:
        mainBlock = res
        getAnsManually(mainBlock,1, url)
        
        
def main(url):
    printAnsFromURL(url)
    return s


def getCurrTime():
    tz = pytz.timezone('Asia/Kolkata')
    time = datetime.now(tz)
    return time

    
def sendProblemEmail(user, url):
    admin = User.query.filter_by(email="shuvamg73@gmail.com").first()
    message = Message('Problem in Your App', sender='noreply@getanssg.com', recipients=[admin.email])
    message.body = f'''Hi { admin.name.split(" ")[0] },

There is an error in your app reported by { user.email }

Please fix this bug ASAP.

----------------------
Error Details:
----------------------

URL       : {url}
User      : {user.name}
User-Mail : {user.email}
Time      : {getCurrTime()}


Please fix the bug and let the user know.



Cheers,
GetAnsSG Team  
'''
    mail.send(message)


def sendAckEmail(user, url):
    message = Message('Problem Submission Confirmation', sender='noreply@getanssg.com', recipients=[user.email])
    message.body = f'''Hi { user.name.split(" ")[0] },

Please be notified that your problem has been logged and developer has been notified about this. Please find the problem details below -

---------------------
Error Details:
---------------------

URL          :  {url}
User         :  {user.name}
User-Mail    :  {user.email}
Time         :  {getCurrTime()}


You will be notified once the bug is fixed.



Cheers,
GetAnsSG Team  
'''
    mail.send(message)