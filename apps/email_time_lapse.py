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
    """
    Main function

    Parameters:
    -----------
    args
        Arguments returned by argparser.ArgumentParser.parse_args()

    Return:
    -------
        0 on successful execution, non-zero value indicates an error occured
    
    """
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
        msg = builder.build_msg(images)
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
    picture_taker.image_folder = args.folder
    picture_taker.image_count = args.images
    picture_taker.capture_delay = args.delay #seconds

    while True:
        picture_taker.sync_capture(send_callback)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-to", "-t", type=str, help="Provide email to send to", default="", required=True)
    parser.add_argument("-gmail", "-g", type=str, help="Provide gmail to send from", default="", required=True)
    parser.add_argument("-password", "-p", type=str, help="Provide gmail password", default="", required=True)
    parser.add_argument("-delay", "-d", type=int, help="Provide delay between photos (sec)", default=10)
    parser.add_argument("-images", "-i", type=int, help="Provide the number of images per email", default=6)
    parser.add_argument("-folder",
            "-f",
            type=str,
            help="Provide directory to temporarily store photos (ex. /home/pi/Pictures/)",
            default="")

    args = parser.parse_args()

    main(args)
