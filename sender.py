from linebot import LineBotApi
from linebot.models import TextSendMessage

class LineSender():
    '''
    This class is used to configure the settings for sending messages to LINE.
    example
    LineSender(LINE_ACCESS_TOKEN, LINE_USER_ID)
    '''

    def __init__(self, LINE_ACCESS_TOKEN, LINE_USER_ID):
        self.LINE_ACCESS_TOKEN = LINE_ACCESS_TOKEN
        self.LINE_USER_ID = LINE_USER_ID

    def send_to_line(self, dfg):
        '''
        This function actually sends a message to the line.
        :param dfg: DataFrame
        :return: none
        '''
        texts = ['不審者発見！！！']

        #TODO(shota.nishiyama44@gmail.com): send jpg

        line_bot = LineBotApi(self.LINE_ACCESS_TOKEN)
        line_bot.multicast(
            self.LINE_USER_ID.split(","), TextSendMessage(text="\n".join(texts))
        )