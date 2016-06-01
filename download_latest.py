import requests
from parse_html import MyHTMLParser
import json

POSTHEADERS={
'Content-Type': 'application/x-www-form-urlencoded',
}

BASE_URL="https://hrafdeling.ctbps.nl/"
LOGIN="Login?returnUrl=/"
PAYMENTS="PaymentsModule/GetPaymentsInYear?year=2016"

LOGIN_DATA={'UserName': 'techno.leut@technolution.nl', 'Password' : 'geheim'}
SUBMIT="Inloggen"


class CobraDownloader(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = True
        self.session.max_redirects = 30
        self.payments_in_year = None

    def init(self):
        init = self.session.get(BASE_URL+LOGIN)
        
        parser = MyHTMLParser(remove_tags=[], set_tags=LOGIN_DATA, submit=SUBMIT)
        parser.feed(init.text)
        post_data = parser.get_post_data()
        
        data = self.session.post(BASE_URL+LOGIN, 
                            data=post_data,
                            headers=POSTHEADERS)
                            
        data = self.session.get(BASE_URL+PAYMENTS)
        self.payments_in_year = json.loads(data.text)
                            
    def save_latest_payments(self):
       
        download_payment = self.payments_in_year["Items"][0]
        filename = download_payment['PeriodHeader'] + ".pdf"
        
        data = self.session.get(BASE_URL + download_payment['PdfUrl'],
                                stream=True)
        
        with open(filename, 'wb') as pdffile:
            while True:
                buf_data = data.raw.read(1024)
                if len(buf_data) == 0 or buf_data == None:
                    break
                pdffile.write(buf_data)
        
        print "Saved latest payment as " + filename
        

def main():
    downloader = CobraDownloader()
    downloader.init()
    downloader.save_latest_payments()

if __name__ == "__main__":
    main()
