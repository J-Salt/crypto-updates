import re
import smtplib
import requests
from datetime import datetime
import time
import credentials

def main():
    user = credentials.login['user']
    password = credentials.login['password']
    destination = credentials.login['destination']
    request_link_BTC = 'https://api.coinbase.com/v2/prices/BTC-USD/buy'
    alert_price = 58300
    can_send = True
    sent_time = 0
    while True:
        send_timer_cur = int(time.time())
        can_send = send_timer_cur-sent_time > 60

        if send_timer_cur % 15 == 0:
            print(can_send)
            text_time = datetime.now()
            current_time = text_time.strftime("%H:%M:%S")

            try:
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.ehlo()
                smtp_server.login(user, password)
                text = re.sub(':', ' ', str(requests.get(request_link_BTC).text))
                text = text.replace('base', '').replace('}', '').replace('\"', '').replace(',', ' : ').replace('{', '').replace('data', '').replace('USD : amount ', '-USD : $').replace(' : currency ', '')
                price = float(text.split()[2].replace('$', ''))
                if price < alert_price and can_send:
                    sent_time = send_timer_cur
                    text = '\n' + text + '\n' + current_time
                    smtp_server.sendmail(user, destination, text)
                    smtp_server.close()
                    print('email sent. ' + current_time)
                else:
                    print('not sent')

            except Exception as e:
                print('something went wrong...', e)


if __name__ == "__main__":
    main()
