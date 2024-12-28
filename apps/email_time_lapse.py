#!/usr/bin/python3

import argparse
import smtplib
from pathlib import Path

import rca.emails
from rca.camera.time_lapse import TimeLapseCapture
from rca.logger import create_rca_logger, get_logger

logger = get_logger(__name__)


def main(args: argparse.Namespace) -> int:
    """
    Main function

    Returns 0 on successful execution, non-zero value indicates an error occured

    Args:
        args: CLI Arguments passed by the user
    """
    if not args.gmail:
        print("Missing -gmail argument")
        return 1

    if not args.password:
        print("Missing -password argument")
        return 1

    if not args.to:
        print("Missing -to argument")
        return 1

    create_rca_logger(log_file=args.logfile)

    builder = rca.emails.HtmlImageBody(args.to, args.gmail, "Greetings!")

    def send_callback(images: list[str]) -> None:
        """
        Callback function for TimeLapseCapture that sends the images in an email
        """
        msg = builder.build_msg(images)
        try:
            client = smtplib.SMTP("smtp.gmail.com", 587)
            client.ehlo()
            client.starttls()
            client.ehlo()
            client.login(user=args.gmail, password=args.password)
            client.sendmail(args.gmail, args.to, msg.as_string())
            logger.debug("Email sent successfully")
        except smtplib.SMTPException:
            logger.exception("SMTP Error occured")
        except OSError:
            logger.exception("OS Error occured")
        except Exception:
            logger.exception("Unknown Error occured")

    picture_taker = TimeLapseCapture(image_folder=args.folder, image_count=args.images, capture_delay=args.delay)

    while True:
        logger.debug("Starting picture taking")
        picture_taker.sync_capture(send_callback)
        logger.debug("Ending picture taking")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-to", "-t", type=str, help="Provide email to send to", default="", required=True)
    parser.add_argument("-gmail", "-g", type=str, help="Provide gmail to send from", default="", required=True)
    parser.add_argument("-password", "-p", type=str, help="Provide Google App password", default="", required=True)
    parser.add_argument("-delay", "-d", type=int, help="Provide delay between photos (sec)", default=10)
    parser.add_argument("-images", "-i", type=int, help="Provide the number of images per email", default=6)
    parser.add_argument(
        "-folder",
        "-f",
        type=Path,
        help="Provide directory to temporarily store photos (ex. /home/pi/Pictures/)",
        default="./",
    )
    parser.add_argument(
        "-logfile",
        "-lf",
        type=Path,
        help="Provide path to file for writing logs (ex. /home/pi/log.txt)",
        default=None,
        required=False,
    )

    main(parser.parse_args())
