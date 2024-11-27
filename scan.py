import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import socket

# SMTP Configuration
SMTP_SSL_WEB_URL = "smtp.bodhee.io"  # Add your SMTP server URL
SMTP_SSL_PORT = 465
SMTP_SSL_LOGIN_ID = "support@bodhee.io"  # Add your login ID
SMTP_SSL_LOGIN_PASSWORD = ""  # Add your login password
SMTP_SENDER_EMAIL = "support@bodhee.io"  # Add your sender email
SMTP_MAIL_PASSWORD = ""  # Add your mail password
RECIPIENTS_EMAIL = "somu.sekhar@neewee.ai","c102fb6b.neewee.ai@apac.teams.ms","aniket.kinekar@neewee.ai"  # Add the recipient email

# Get current date, time, and hostname
current_date_time = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
hostname = socket.gethostname()

# Read the log file
log_file_path = "/root/clamscan.txt"
infected_files_found = False

# Check the number of infected files in the log
with open(log_file_path, "rb") as f:
    for line in f:
        if b"Infected files" in line:
            infected_files_count = int(line.strip().split(b':')[1])
            if infected_files_count > 0:
                infected_files_found = True
            break  # No need to check further after finding infected files count

# Set the subject based on the infected files count
if infected_files_found:
    SUBJECT = f"Infected files detected for {hostname} on {current_date_time}"
else:
    SUBJECT = f"Scan completed for {hostname} on {current_date_time}"

# Create the email message
msg = MIMEMultipart()
msg['From'] = SMTP_SENDER_EMAIL
msg['To'] = ", ".join(RECIPIENTS_EMAIL)
msg['Subject'] = SUBJECT

# Attach the log file
part = MIMEBase('application', "octet-stream")
with open(log_file_path, "rb") as attachment:
    part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename="{log_file_path.split("/")[-1]}"')
msg.attach(part)

# Create email body text
body = "Please find the attached clamscan report."
msg.attach(MIMEText(body, 'plain'))

# Sending the email
try:
    s = smtplib.SMTP_SSL(SMTP_SSL_WEB_URL, SMTP_SSL_PORT)
    s.login(SMTP_SSL_LOGIN_ID, SMTP_SSL_LOGIN_PASSWORD)
    s.sendmail(SMTP_SENDER_EMAIL, RECIPIENTS_EMAIL, msg.as_string())
    print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    s.quit()
