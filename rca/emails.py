"""
Classes and functions for sending emails

"""

import logging
import mimetypes
import smtplib
from abc import ABC, abstractmethod
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

logger = logging.getLogger(__name__)


def send_text_email(receiver: str, sender: str, password: str, subject: str, body: str) -> None:
    """
    Send a email, whose body is text, using SMTP

    Args:
        receiver : Email address of receiver
        sender : Gmail address of sender
        password : Google App password of sender
        subject : Email subject line
        body : Email body text
    """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(body)

    try:
        client = smtplib.SMTP("smtp.gmail.com", 587)
        client.ehlo()
        client.starttls()
        client.ehlo()
        client.login(user=sender, password=password)
        client.sendmail(sender, receiver, msg.as_string())

    except smtplib.SMTPException:
        logger.exception("An error occured sending an email using SMTP")


class ImageBody(ABC):
    """
    An interface that defines building an EmailMessage object that contains
    images within the message

    Methods:
    --------
    build_msg
        Return EmailMessage containing images that can be sent
    """

    @abstractmethod
    def build_msg(self, images: list[Path]) -> EmailMessage:
        """
        Return an EmailMessage object containing the images that can be sent

        Args:
            images : a list of image file paths
        """
        pass


class HtmlImageBody(ImageBody):
    """
    This class uses embedded html to place images within the body of the email

    """

    def __init__(self, receiver: str, sender: str, subject: str):
        """
        Initialize the email receiver, sender, and subject
        """
        self._receiver = receiver
        self._sender = sender
        self._subject = subject

    def build_msg(self, images: list[Path]) -> EmailMessage:
        msg = EmailMessage()
        msg["Subject"] = self._subject
        msg["From"] = self._sender
        msg["To"] = self._receiver

        # start html with opening tags
        html_str = """
                <html>
                    <body>

                    """

        # store image cids for formatting the string later
        image_cids = []
        for i in range(0, len(images)):
            cid = make_msgid(idstring="kappa")
            html_str += """
                        <img src="cid:{image_cid}">
                        <br />
                        """.format(image_cid=cid[1:-1])
            image_cids.append(cid)

        # add closing tags
        html_str += """
                    </body>
                </html>
                """
        msg.add_alternative(html_str, subtype="html")

        for i in range(0, len(images)):
            with open(images[i], "rb") as img:
                maintype, subtype = mimetypes.guess_type(img.name)[0].split("/")
                msg.get_payload()[0].add_related(img.read(), maintype=maintype, subtype=subtype, cid=image_cids[i])

        return msg
