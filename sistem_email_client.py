from credentials import *
from send_email import send_email, send_file
from read_email import read_email

# Menu utama
while True:
    print("\nMenu Klien Email")
    print("1. Kirim Email")
    print("2. Kirim Email dengan File Lampiran")
    print("3. Baca Email")
    print("4. Keluar")

    choice = input("Masukkan pilihan Anda: ")

    if choice == '1':
        send_email()
    elif choice == '2':
        send_file()
    elif choice == '3':
        read_email()
    elif choice == '4':
        if server is not None:
            server.quit()
        if mail is not None:
            mail.close()
            mail.logout()
        print("Keluar dari program.")
        break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
