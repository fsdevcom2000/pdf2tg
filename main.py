import email
import imaplib
import logging
import os
import requests
from datetime import datetime
from email.header import decode_header

import config  # import settings from config.py

# === Logging Setup ===
LOG_FILE = os.path.join(config.SAVE_FOLDER, "mail_to_telegram.log")
logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s :: %(levelname)s :: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
)


def log(msg):
    print(msg)
    logging.info(msg)


def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendDocument"
    with open(file_path, 'rb') as f:
        response = requests.post(url, data={"chat_id": config.TELEGRAM_CHAT_ID}, files={"document": f})
    return response.ok


def decode_mime_words(s):
    decoded_words = decode_header(s)
    return ''.join([
        str(t[0], t[1] or 'utf-8') if isinstance(t[0], bytes) else t[0]
        for t in decoded_words
    ])


def process_mail():
    try:
        mail = imaplib.IMAP4_SSL(config.IMAP_SERVER)
        mail.login(config.EMAIL_ACCOUNT, config.EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, f'(UNSEEN FROM "{config.SENDER_EMAIL}")')

        if status != "OK":
            log("No messages found.")
            return

        for num in messages[0].split():
            status, data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                log("Failed to fetch message.")
                continue

            msg = email.message_from_bytes(data[0][1])
            subject = decode_mime_words(msg.get("Subject", ""))
            log(f"Found message: {subject}")

            for part in msg.walk():
                content_disposition = part.get("Content-Disposition", "")
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        filename = decode_mime_words(filename)
                        if filename.lower().endswith(".pdf"):
                            file_path = os.path.join(config.SAVE_FOLDER, filename)
                            with open(file_path, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            log(f"Saved: {file_path}")

                            if send_to_telegram(file_path):
                                log("Sent to Telegram.")
                            else:
                                log("Failed to send to Telegram.")

                            os.remove(file_path)
                            log("File deleted.")

            # Mark email as read
            mail.store(num, '+FLAGS', '\\Seen')

        mail.logout()

    except Exception as e:
        logging.error(f"Script error: {e}")
        log(f"Script error: {e}")


if __name__ == "__main__":
    log("Script started.")
    process_mail()
    log("Script finished.")
