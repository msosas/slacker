from config import Config
from slacker import Slacker
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send Slack notifications')
    parser.add_argument('message', help='The message you want to send')
    parser.add_argument('channel', type=str, help='The Slack channel where you want the message to be sent: #channel or @user')
    parser.add_argument('--log_level', '-l', help='The log level', default='INFO')
    parser.add_argument('--parser', '-p', help='The message parser', default=None)
    args = parser.parse_args()

    # from static import SLACK_WEB_HOOK
    
    config = Config(slack_channel=args.channel)
    slacker = Slacker(config)

    slacker.send_message(
        message=args.message, log_level=args.log_level, parser=args.parser
    )
