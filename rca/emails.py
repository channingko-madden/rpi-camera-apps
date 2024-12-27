"""
Classes and functions for sending emails

Classes:
"""

import mimetypes
import smtplib
from abc import ABC
from email.message import EmailMessage
from email.utils import make_msgid


def send_text_email(receiver, sender, password, subject, body):
    """
    Send a email, whose body is text, using SMTP

    Parameters:
    -----------
    receiver : str
        Email address of receiver
    sender : str
        Email address of sender
    password : str
        Google App password of sender
    subject : str
        Email subject line
    body : str
        Email body text
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

    except smtplib.SMTPException as error:
        print("Error occured" + str(error))


class ImageBody(ABC):
    """
    An interface that defines building an EmailMessage object that contains
    images within the message

    Methods:
    --------
    build_msg
        Return EmailMessage containing images that can be sent
    """

    def build_msg(self, images):
        """
        Return an EmailMessage object containing the images that can be sent

        Parameters
        ----------
            images : list of str
                file names of images
        """
        pass


class HtmlImageBody(ImageBody):
    """
    This class uses embedded html to place images within the body of the email

    """

    def __init__(self, receiver, sender, subject):
        """
        Initialize the email receiver, sender, and subject
        """
        self._receiver = receiver
        self._sender = sender
        self._subject = subject

    def build_msg(self, images):
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
