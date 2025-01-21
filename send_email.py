import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from credentials import *

def login():
    global server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Mengamankan koneksi
        server.login(email_address, email_password)
        print("Login berhasil.")
    except Exception as e:
        print(f"Gagal login: {e}")

def send_email():
    global server

    # Cek apakah sudah login, jika belum maka login terlebih dahulu
    if server is None:
        print("Belum login, sedang melakukan login...")
        login()

    try:
        recipient_address = input("Masukkan alamat email penerima: ")
        if not recipient_address.strip():
            print("Alamat email penerima tidak boleh kosong. Kembali ke menu.")
            return
        subject = input("Masukkan subjek email: ")
        body = input("Masukkan isi email: ")

        print("\n--- Informasi ---")
        print(f"Pengirim: {email_address}")
        print(f"Penerima: {recipient_address}")
        print(f"Subjek: {subject}")
        print(f"Isi: {body}")
        print("Sedang memproses pengiriman email...\n")

        # Membuat objek MIME
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient_address
        msg['Subject'] = subject
        
        # Menambahkan isi email ke pesan MIME
        msg.attach(MIMEText(body, 'plain'))

        # Mengirim email
        server.sendmail(email_address, recipient_address, msg.as_string())
        print("Email berhasil dikirim!")

    except Exception as e:
        print(f"Gagal mengirim email: {e}")

def send_file():
    global server  # Deklarasikan server sebagai global

    # Cek apakah sudah login, jika belum maka login terlebih dahulu
    if server is None:
        print("Belum login, sedang melakukan login...")
        login()

    try:
        recipient_address = input("Masukkan alamat email penerima: ")
        if not recipient_address.strip():
            print("Alamat email penerima tidak boleh kosong. Kembali ke menu.")
            return
        subject = input("Masukkan subjek email: ")
        body = input("Masukkan isi email: ")

        # File to attach
        filename = input("Masukkan path file yang ingin dilampirkan: ").strip()

        # kondisi jika file tidak diisi
        if not filename:
            print("Tidak ada file yang dilampirkan")
        elif not (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.pdf')):
            print("File yang diizinkan hanya berupa gambar (.jpg, .jpeg, .png) dan PDF (.pdf).")
            return

        print("\n--- Informasi ---")
        print(f"Pengirim: {email_address}")
        print(f"Penerima: {recipient_address}")
        print(f"Subjek: {subject}")
        print(f"Isi: {body}")
        print(f"Melampirkan file: {filename}")
        print("Sedang memproses pengiriman email...\n")

        # Membuat objek MIME
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient_address
        msg['Subject'] = subject
        
        # Menambahkan isi email ke pesan MIME
        msg.attach(MIMEText(body, 'plain'))

        # Menambahkan file sebagai lampiran
        try:
            if filename:
                with open(filename, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={filename.split("/")[-1]}')
                    msg.attach(part)
                print(f"File '{filename}' berhasil ditambahkan sebagai lampiran.")
        except FileNotFoundError:
            print(f"File '{filename}' tidak ditemukan. Lampiran gagal ditambahkan.")
            return

        # Mengirim email
        server.sendmail(email_address, recipient_address, msg.as_string())
        print("Email berhasil dikirim!")
    except Exception as e:
        print(f"Gagal mengirim email dengan lampiran: {e}")