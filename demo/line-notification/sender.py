import os

from linebot import LineBotApi
from linebot.models import TextSendMessage


class LineSender():
    '''
    This class is used to configure the settings for sending messages to LINE.
    Example:
    >>> load_dotenv(verbose=True)
    >>> LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
    >>> LINE_USER_ID = os.getenv("LINE_USER_ID")
    >>> line_sender = LineSender(LINE_ACCESS_TOKEN, LINE_USER_ID)

    >>> msg = 'Hello Beautifule world.'
    >>> line_sender.send_to_line(msg)
    '''

    def __init__(self, LINE_ACCESS_TOKEN, LINE_USER_ID):
        self.LINE_ACCESS_TOKEN = LINE_ACCESS_TOKEN
        self.LINE_USER_ID = LINE_USER_ID

    def send_to_line(self, msg):
        '''
        This function actually sends a message to the line.
        :param str: Message to send to line.
        :return: none
        '''

        texts = ['不審者発見！！！']

        #TODO(shota.nishiyama44@gmail.com): send jpg

        line_bot = LineBotApi(self.LINE_ACCESS_TOKEN)
        # line_bot.multicast(
        #     self.LINE_USER_ID.split(","), TextSendMessage(texts)
        # )

        line_bot.push_message(
            os.getenv("LINE_USER_ID"), TextSendMessage(text="\n".join(texts))
        )