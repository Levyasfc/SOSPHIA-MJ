# app/utilidades/correos.py
import os
import ssl
import asyncio
from email.message import EmailMessage
from typing import Optional

#Instancias para mensajes

MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))        
MAIL_USERNAME = os.getenv("MAIL_USERNAME", None)
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", None)
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in ("1", "true", "yes")
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() in ("1", "true", "yes")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)

if not MAIL_USERNAME or not MAIL_PASSWORD:
    print("⚠️ Aviso: MAIL_USERNAME o MAIL_PASSWORD no configurados. El envío de correo fallará hasta configurarlos.")

async def enviar_email(destino: str, asunto: str, cuerpo: str, html: Optional[str] = None):

    def _send_sync():
        msg = EmailMessage()
        msg["From"] = MAIL_FROM or MAIL_USERNAME
        msg["To"] = destino
        msg["Subject"] = asunto
        if html:
            msg.set_content(cuerpo)
            msg.add_alternative(html, subtype="html")
        else:
            msg.set_content(cuerpo)

        # Elegir conexión
        if MAIL_USE_SSL or MAIL_PORT == 465:
            context = ssl.create_default_context()
            with __import__("smtplib").SMTP_SSL(MAIL_SERVER, MAIL_PORT, context=context) as smtp:
                smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
                smtp.send_message(msg)
        else:
           
            smtp = __import__("smtplib").SMTP(MAIL_SERVER, MAIL_PORT, timeout=30)
            try:
                smtp.ehlo()
                if MAIL_USE_TLS:
                    smtp.starttls(context=ssl.create_default_context())
                    smtp.ehlo()
                smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
                smtp.send_message(msg)
            finally:
                smtp.quit()

    await asyncio.to_thread(_send_sync)
