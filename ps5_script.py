import requests
import bs4
import smtplib
import syslog

url =  "https://www.mightyape.co.nz/product/sony-playstation-5-console/31675007"

def isInStock(productURL):
    res = requests.get(productURL)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    
    elems = soup.select('body > div.page-container > div.page.listing.details.not-in-trolley.category.category-games.category-consoles > div > main > section.product-summary-top > div > div > div.product-summary.unavailable > div.pricing-stock > div > div.status')
    status = elems[0].text.strip()
    if status == 'Unavailable':
        return False
    else:         
        return True 


def send_email():
     # create an email message with just a subject line,
        msg = 'Subject: Check Mighty Ape for the PS5!'
        # set the 'from' address,
        fromaddr = 'enter_email used to send' #Enter the email thats gonna send the mesasge. 
        # set the 'to' addresses,
        toaddrs  = ['',] #Enter the email address to send to

        # setup the email server,
        server = smtplib.SMTP('smtp.gmail.com', 587) #change if not gmail
        server.starttls()
        # add my account login name and password,
        server.login("ENTER_YOUR_SENDING_EMAIL_ADDRESS", "EMAIL_PASSWORD") #Enter your email address and password here

        # Print the email's contents
        print('From: ' + fromaddr)
        print('To: ' + str(toaddrs))
        print('Message: ' + msg)

        # send the email
        server.sendmail(fromaddr, toaddrs, msg)
        # disconnect from the server
        server.quit()

if isInStock(url):
    syslog.syslog("Ps5 is in stock... sending email")
    send_email()
    #cron job to run every 30min send email to ashley's email.
else:
    syslog.syslog('Ps5 is not in stock..')
    
