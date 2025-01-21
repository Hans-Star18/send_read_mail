import imaplib
import email
from email.header import decode_header
import time
import os
from credentials import *

download_folder = "downloads"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Fungsi login untuk membaca email
def read_login():
    global mail  # Mengakses variabel mail dari credentials
    try:
        # Connect to the IMAP server using SSL
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        # Log in to the server
        mail.login(email_address, email_password)
        print("Login berhasil untuk membaca email.")
    except Exception as e:
        print(f"Gagal login: {e}")

# Fungsi untuk membaca email
def read_email():
    try:
        if mail is None:
            print("Belum login untuk membaca email, sedang melakukan login...")
            read_login()

        # Select the mailbox you want to use
        mail.select("inbox")  # Select inbox by default

        # Search for all emails in the inbox
        status, messages = mail.search(None, "ALL")

        # Get the list of email IDs
        email_ids = messages[0].split()
        print(f"Jumlah email: {len(email_ids)}")

        # Fetch the latest email (you can loop through all emails if you want)
        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

        # Get the email content
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg.get("From")
                print(f"Subjek: {subject}")
                print(f"Dari: {from_}")

                # If the email message is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                            try:
                                body = part.get_payload(decode=True).decode()
                                print("Isi:", body)
                            except Exception as e:
                                print("Error decoding body:", e)

                        # Cek apakah ada lampiran
                        if part.get_content_disposition() == "attachment":
                            filename = part.get_filename()
                            if filename:
                                # Decode the filename
                                filename, encoding = decode_header(filename)[0]
                                if isinstance(filename, bytes):
                                    filename = filename.decode(encoding or "utf-8")
                                print("Lampiran:", filename)

                                # Simpan lampiran
                                timestamps = round(time.time())
                                filepath = os.path.join(download_folder, f"{timestamps}_{filename}")
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                    print(f"File berhasil diunduh: {filepath}")
                else:
                    body = msg.get_payload(decode=True).decode()
                    print("Isi:", body)
    except Exception as e:
        print(f"Gagal menerima email: {e}")
