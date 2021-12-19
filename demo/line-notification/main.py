import os

from dotenv import load_dotenv

from sender import LineSender

def main():

    load_dotenv(verbose=True)
    LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
    LINE_USER_ID = os.getenv("LINE_USER_ID")
    # Confirm Your Secrets Key
    # print(f'LINE_ACCESS_TOKEN{LINE_ACCESS_TOKEN}, LINE_USER_ID{LINE_USER_ID}')
    line_sender = LineSender(LINE_ACCESS_TOKEN, LINE_USER_ID)

    msg = 'Hello Beautifule world.'
    line_sender.send_to_line(msg)

if __name__ == "__main__":
    main()
