import json
import re
import secrets
import string
from email.message import EmailMessage

import aiosmtplib

from fastapi import FastAPI
from fastapi.routing import APIRoute
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


def generate_public_id(prefix="org", random_length=16):
    alphabet = string.ascii_letters + string.digits
    random_part = "".join(secrets.choice(alphabet) for _ in range(random_length))
    return f"{prefix}-{random_part}"


def run_alembic_migration(DB_SQLALCHEMY_URI: str):
    from alembic.command import upgrade
    from alembic.config import Config

    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", DB_SQLALCHEMY_URI)
    upgrade(alembic_config, "head")

    # Rerun setup_logging due to alembic logging is interfere with the app logging
    setup_logging()


async def send_email_smtp(subject: str, body: str, recipient: str):
    message = EmailMessage()
    message["From"] = f"{settings.BRAND_NAME} <{mail_settings.MAIL_SMTP_USERNAME}>"
    message["To"] = recipient
    message["Subject"] = subject
    message.add_alternative(body, subtype="html")

    if mail_settings.MAIL_ENABLED:
        logger.debug(f"Sending SMTP {mail_settings.MAIL_SMTP_USERNAME}")
        await aiosmtplib.send(
            message,
            hostname=mail_settings.MAIL_SMTP_HOST,
            port=mail_settings.MAIL_SMTP_PORT,
            start_tls=True,
            username=mail_settings.MAIL_SMTP_USERNAME,
            password=mail_settings.MAIL_SMTP_PASSWORD,
        )
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


HTTP_METHOD_TO_VERB = {
    "get": "get",
    "post": "post",
    "put": "put",
    "patch": "patch",
    "delete": "delete"
}

def to_camel_case(parts: list[str]) -> str:
    return "".join(part.capitalize() for part in parts)

def generate_operation_id(path: str, method: str) -> str:
    parts = path.strip("/").split("/")
    version = None

    # Extract version like v1, v2
    for i, part in enumerate(parts):
        if re.fullmatch(r"v\d+", part):
            version = part.upper()  # V1, V2
            parts.pop(i)
            break

    # Remove "api" prefix if present
    parts = [p for p in parts if p != "api"]

    # Replace path parameters like {id} → ById
    processed_parts = []
    for p in parts:
        match = re.match(r"{(.*?)}", p)
        if match:
            param_name = match.group(1)
            processed_parts.append(f"By{to_camel_case([param_name])}")
        else:
            processed_parts.append(p)

    # Determine base resource (e.g., pets)
    base = processed_parts[0] if processed_parts else "resource"
    suffix = processed_parts[1:] if len(processed_parts) > 1 else []

    verb = HTTP_METHOD_TO_VERB.get(method.lower(), method.lower())
    operation_id = verb + to_camel_case([base] + suffix)

    if version:
        operation_id += version

    return operation_id

def set_operation_ids(app: FastAPI):
    for route in app.routes:
        if isinstance(route, APIRoute):
            if not route.operation_id:
                method = list(route.methods)[0].lower()
                route.operation_id = generate_operation_id(route.path, method)