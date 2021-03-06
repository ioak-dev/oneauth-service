import smtplib, ssl, dkim, base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# smtp_mail_server = "smtp.yandex.com"
port = 465
sender_email = str(Header('Ioak support <no-reply@dev.ioak.org>'))
# password = "PDXC9MLzgfrVnk6"
domain = b'dev.ioak.org'
dkim_selector = b'email'
dkim_private_key_path = "library/dkimkey.pem"
smtp_mail_server = "smtp.gmail.com"
# port = 587
username = 'ioakdevteam@gmail.com'
password = "oilfvbezqsuculep"

def send_mail_bkp(to, subject, body):
    with open(dkim_private_key_path) as fh:
        dkim_private_key = fh.read()
    print(dkim_private_key)
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to
    headers = ["To", "From", "Subject"]
    message.attach(MIMEText(body, "html"))
    sig = dkim.sign(
            message=message.as_string(),
            selector=dkim_selector,
            domain=domain,
            privkey=dkim_private_key.encode(),
            include_headers=headers,
        )
    message["DKIM-Signature"] = sig.lstrip("DKIM-Signature: ")
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_mail_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to, message.as_string())

def send_mail(to, subject, body):
    # sender_domain = sender_email.split("@")[-1]
    # msg = MIMEMultipart("alternative")
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "html", "utf-8"))
    # msg.attach(MIMEText(body, "plain", "utf-8"))
    # msg = MIMEText(body, "plain", "utf-8")
    msg["To"] = to
    msg["From"] = sender_email
    msg["Subject"] = subject

    if dkim_private_key_path and dkim_selector:
        with open(dkim_private_key_path) as fh:
            dkim_private_key = fh.read()
        headers=[b'From', b'To', b'Subject']
        sig = dkim.sign(
            message=msg.as_bytes(),
            # selector=base64.b64encode(bytes(dkim_selector, encoding='utf-8')),
            # domain=base64.b64encode(bytes(sender_domain, encoding='utf-8')),
            selector=dkim_selector,
            domain=domain,
            privkey=bytes(dkim_private_key, encoding='utf-8'),
        )
        msg["DKIM-Signature"] = sig.decode().lstrip("DKIM-Signature: ")
    context = ssl.create_default_context()
    # print(msg)
    with smtplib.SMTP_SSL(smtp_mail_server, port, context=context) as server:
        server.login(username, password)
        server.sendmail(sender_email, to, msg.as_string())
