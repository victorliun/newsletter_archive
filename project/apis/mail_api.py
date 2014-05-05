"""
This model provide a way to process mail.
see class ZMailAPI
"""
import re
import json
import logging
import imaplib, email
from dateutil import parser
from datetime import datetime

from email.parser import HeaderParser
from bs4 import BeautifulSoup

class ZMailAPI():
    """
    This class will built an api connected to mail server and extract sender, subject, header, 
    and newsletter url from each mail.

    Usage : init this api with your and account and password,
        call select method. the call search method.
    """
    def __init__(self, address, password):
        """
        Given a address and password to Gmail(default)
        """
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(address, password)

    def select(self,box="INBOX"):
        """
        This method select which box to choose, default is inbox.
        """
        return self.mail.select(box)

    def search(self, criteria="(UNSEEN)"):
        """
        This function will search email match the criteria.
        """
        return self.mail.search(None, criteria)

    def process_email(self, mail_id):
        """
        extract subject, sender, header, body, newsletters_url if any from emails.
        This will dict of sender,subject,header and newsletters_url
        """
        newsletter = {}
        msg = self.fetch(mail_id)
        newsletter['sender'] = email.utils.parseaddr(msg['from'])
        newsletter['subject'] = msg['subject']
        newsletter['header'] = json.dumps(dict(msg.items()), ensure_ascii=False)
        try:
            publish_date = parser.parse(msg['date'])
        except Exception, exp:
            publish_date = datetime.now()
        newsletter['publish_date'] = publish_date
        newsletters_url = self.get_newsletter_url(msg)
        print "Process email:id:%s, sender:%s, subject:%s" % (mail_id, newsletter['sender'],
            newsletter['subject'])
        print "newsletter url: %s", newsletters_url
        if msg.is_multipart() or not newsletters_url or len(newsletters_url) > 200:
            logging.error("Process Failed, this may not be a newsletter.")
            return None

        
        newsletter['url'] = newsletters_url
        self.mail.store(mail_id, '+FLAGS', '(SEEN)')
        return newsletter
 
    def fetch(self, mail_id):
        """
        this method will the get message instance of the id.
        > mail_id: mail id:
        > return: message instance
        """
        resp, data = self.mail.fetch(mail_id, "(RFC822)")
        if resp != 'OK':
            logging.warning("Unexpect response:%s", resp)
            return False
        try:
            data = data[0][1]
        except IndexError, err:
            logging.error("Tuple out of index")
            return False

        return HeaderParser().parsestr(data)

    def get_newsletter_url(self, msg):
        """
        This function will try to extract newsletter url from newsletter body
        args:
            > msg: email.message.Message isinstance
            > return: newsletter url or None
        """

        shit_html = msg.get_payload()
        #Remove characaters before pass to bs4 or the result will be ugly.
        htm = re.sub("=0A|=\r\n|\r\n",'',shit_html)
        ht = re.sub('=3D', '=', htm)
        soup = BeautifulSoup(ht)
        #newsletters_link_text_pa = re.compile("view.*?(it|email).*?(browser|webpage|see it online|web version)", re.IGNORECASE)
        newsletters_link_text_pa = re.compile("(view.*?(it|email).*?(browser|webpage))|(Web version)|(SEE IT ONLINE)", re.IGNORECASE)
        # the url link text to newsletter may be 'click here'
        click_here_pa = re.compile(r'click here', re.IGNORECASE) 
        res = soup.findAll('a', text=newsletters_link_text_pa)        
        for tag in res:
            if tag.attrs['href']:
                # consider this is the url to webpage newsletter.
                return tag.attrs['href']
        res_click_here = soup.findAll('a', text=click_here_pa)
        for label in res_click_here:
            parent = label.find_parent()
            if parent.text.lower().find('view') != -1:
                #In this case, we found view .* click here. That is more like a newsletter than only consider 'click here'
                if label.attrs['href']:
                    # consider this is the url to webpage newsletter.
                    return label.attrs['href']
        return None

    def logout(self):
        """
        logout mail server
        """

        return self.mail.logout()
