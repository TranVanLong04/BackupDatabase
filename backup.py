import os
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()
sender_email = os.getenv('SENDER_EMAIL')
app_password = os.getenv('APP_PASSWORD')
receiver_email = os.getenv('RECEIVER_EMAIL')

def send_email(subject, body):
    try:
        # Tao messenger
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Them noi dung email
        message.attach(MIMEText(body, 'plain'))

        # Ket noi den server Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)

        # Gui Gmail
        server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email voi tieu de '{subject}' da duoc gui thanh cong.")

        # Dong ket noi
        server.quit()

    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

def backup_database():
    try:
        #path goc va path folder backup
        src_folder = "./database"
        backup_folder = "./backup"

        # Check folder nguon
        if not os.path.exists(src_folder):
            raise Exception(f"Thuc muc goc {src_folder} khong ton tai.")

        # Check va sao luu file sql
        backed_up_files = []  # luu cac file da sao luu
        for file_name in os.listdir(src_folder):
            if file_name.endswith(".sql") or file_name.endswith(".sqlite3"):
                path_goc = os.path.join(src_folder, file_name)
                path_backup = os.path.join(backup_folder, file_name)
                shutil.copy(path_goc, path_backup)
                backed_up_files.append(file_name)

        # Neu khong co file nao de backup
        if not backed_up_files:
            raise Exception("Khongó file .sql or .sqlite3 trong folder goc.")

        # Thong bao va gui Mail
        success_message = f"Backup thanh cong. Cac file duoc sao luu: {', '.join(backed_up_files)}"
        print(success_message)
        send_email("Backup thsnh cong", success_message)
    except Exception as e:
        # Thong bao loi va gui mail that bai
        error_message = f"Loi khi backup: {e}"
        print(error_message)
        send_email("Backup that bai", error_message)

def main_loop():
    while True:
        now = datetime.now()
        print(f"Thoi gian thuc: {now.strftime('%H:%M:%S')}")

        # Check time backup co dung hay khong
        if now.hour == 20 and now.minute == 35 and now.second == 0:
            print("Den gio backup, bat dau sao luu...")
            backup_database()
            print("Backup thanh cong.")
        time.sleep(1)

if __name__ == "__main__":
    main_loop()