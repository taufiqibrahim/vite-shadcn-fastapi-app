import json
from email.message import EmailMessage

from src.core.config import mail_settings, settings
from src.core.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


def stream_json(records):
    yield "["
    first = True
    for row in records:
        if not first:
            yield ","
        else:
            first = False
        yield json.dumps(dict(row))
    yield "]"


async def send_email_smtp(subject: str, body: str, recipient: str):
    message = EmailMessage()
    message["From"] = f"{settings.BRAND_NAME} <{mail_settings.MAIL_SMTP_USERNAME}>"
    message["To"] = recipient
    message["Subject"] = subject
    message.add_alternative(body, subtype="html")

    if mail_settings.MAIL_ENABLED:
        logger.debug(f"SMTP {mail_settings.MAIL_SMTP_USERNAME}")

        # await aiosmtplib.send(
        #     message,
        #     hostname=mail_settings.MAIL_SMTP_HOST,
        #     port=mail_settings.MAIL_SMTP_PORT,
        #     start_tls=True,
        #     username=mail_settings.MAIL_SMTP_USERNAME,
        #     password=mail_settings.MAIL_SMTP_PASSWORD,
        # )
    else:
        print(
            f"""
*********************************************************
EMAIL PRINTED (MAIL_ENABLED={mail_settings.MAIL_ENABLED})
---------------------------------------------------------
    From        = f"{settings.BRAND_NAME} <{mail_settings.MAIL_SMTP_USERNAME}>"
    To          = {recipient}
    Subject"]   = {subject}
    Body        = {body}
*********************************************************
"""
        )
