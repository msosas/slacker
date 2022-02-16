from config import Config
from slacker import Slacker

if __name__ == '__main__':

    from message import message
    from static import SLACK_WEB_HOOK
    
    config = Config(slack_web_hook=SLACK_WEB_HOOK, slack_channel='@matias')
    slacker = Slacker(config)

    slacker.send_message(
        message='Todo caido', log_level='warning'
    )
