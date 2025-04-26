from src.core.config import settings
from src.utils import send_email_smtp


async def send_welcome_email(recipient: str):
    subject = "Welcome!"
    body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Welcome Email</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 30px;">
  <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 20px;">
    <h2 style="color: #333;">Welcome to {settings.BRAND_NAME}!</h2>
    <p style="font-size: 16px; color: #555;">
      We're excited to have you on board. Click below to start using the app:
    </p>
    <p>
      <a href="{settings.APP_URL}" style="display: inline-block; background-color: #4CAF50;
      color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">
        Go to App
      </a>
    </p>
    <p style="font-size: 14px; color: #3c3f3c;">
      If you have any questions, feel free to reach out to our support team.
    </p>
  </div>
</body>
</html>
"""
    await send_email_smtp(subject, body, recipient)


async def send_password_reset_email(recipient: str, password_reset_token: str):
    url = f"{settings.APP_URL}/reset-password?token={password_reset_token}"
    subject = "Reset Password Requested!"
    body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Reset Password Requested!</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 30px;">
  <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 20px;">
    <h2 style="color: #333;">Reset Password Requested!</h2>
    <p style="font-size: 16px; color: #555;">
      We have received a password reset request for your account. Click below to reset your password:
    </p>
    <p>
      <a href="{url}" style="display: inline-block; background-color: #4CAF50; color: white;
      padding: 12px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">
        Reset password
      </a>
    </p>
    <p style="font-size: 14px; color: #3c3f3c;">
      If you have any questions, feel free to reach out to our support team.
    </p>
  </div>
</body>
</html>
"""
    await send_email_smtp(subject, body, recipient)


async def send_password_reset_succeed_email(recipient: str):
    subject = "Your password has been reset"
    body = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Reset Password Successful!</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 30px;">
  <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 20px;">
    <h2 style="color: #333;">Reset Password Successful!</h2>
    <p style="font-size: 16px; color: #555;">
      Your password has been reset
    </p>
    <p style="font-size: 14px; color: #3c3f3c;">
      If you have any questions, feel free to reach out to our support team.
    </p>
  </div>
</body>
</html>
"""
    await send_email_smtp(subject, body, recipient)
