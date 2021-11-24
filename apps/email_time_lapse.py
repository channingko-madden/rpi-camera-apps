#!/usr/bin/python3

##
# file: email_time_lapse.py
# date: 2021-11-23
# author: Channing Ko-Madden
#
# description: This app takes pictures at a given time interval, and emails the pictures to you!

import argparse
import smtplib
from rca.camera.time_lapse import TimeLapseCapture
import rca.emails

def main(args):
    if not args.gmail:
        print("Missing -gmail argument")
        return 1

    if not args.password:
        print ("Missing -password argument")
        return 1

    if not args.to:
        print("Missing -to argument")
        return 1

    def send_callback(images):
        builder = rca.emails.HtmlImageBody(args.to, args.gmail, "Greetings!")
        msg = builder.buildMsg(images)
        try:
            client = smtplib.SMTP('smtp.gmail.com', 587)
            client.ehlo()
            client.starttls()
            client.ehlo()
            client.login(user=args.gmail, password=args.password)
            client.sendmail(args.gmail, args.to, msg.as_string())

        except smtplib.SMTPException as error:
            print("Error occured" + str(error))

    picture_taker = TimeLapseCapture()
    picture_taker.image_folder = "/home/pi/Pictures/"
    picture_taker.image_count = 10
    picture_taker.capture_delay = 5 #seconds

    while True:
        picture_taker.sync_capture(send_callback)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-to", "-t", type=str, help="Provide email to send to", default="", required=True)
    parser.add_argument("-gmail", "-g", type=str, help="Provide gmail to send from", default="", required=True)
    parser.add_argument("-password", "-p", type=str, help="Provide gmail password", default="", required=True)

    args = parser.parse_args()

    main(args)
