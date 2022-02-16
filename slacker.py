from loguru import logger
from datetime import datetime
from config import Config


from requests import post as requests_post

class Slacker:
    """
    A Slack notifications class
    """
    def __init__(self, config: Config): 
        self.config = config
        self.slack_channel = config.get_slack_channel()
        self.slack_username = config.get_slack_username()

    # def log_level_to_icons(self, log_level: str='DEBUG'):      
    #     return logger.level(log_level.upper()).icon

    log_level_to_icons = {
        logger.level('CRITICAL').no: ":skull:",
        logger.level('ERROR').no: ":x:",
        logger.level('WARNING').no: ":warning:",
        logger.level('INFO').no: ":information_source:",
        logger.level('DEBUG').no: ":beetle:",
    }

    log_level_to_colors = {        
        logger.level('CRITICAL').no: "#FF3333",
        logger.level('ERROR').no: "#99004C",
        logger.level('WARNING').no: "#FF8000",
        logger.level('INFO').no: "#0080FF",
        logger.level('DEBUG').no: "#9733EE",
    }


    log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    def log_level_to_int(self, log_level):
        return (self.log_levels.index(log_level) + 1)*10

    def validate_message(self, message):
        if not message:
            logger.warning('Empty message. Request not sent')
            return False
        else:
            if not 'channel' in message.keys():
                message['channel'] = self.slack_channel

        return True



    ## Begin of Parsers:

    def default_parser(self, message, log_level: int):
        # https://api.slack.com/messaging/composing/layouts
        if not isinstance(message, str):
            logger.critical('DataType')
            raise TypeError(f'{message} is not a string. Try using a different parser')

        date = datetime.now()
        date_string = date.strftime("%Y-%m-%d %H:%M:%S%z")

        parsed_msg = {
            "icon_emoji": ":construction:",
            "username": self.get_slack_username(),
            "channel": self.get_slack_channel(),
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{self.log_level_to_icons[log_level]} *{self.log_levels[log_level//10 - 1 ]}*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "`" + date_string + "`"
                    }
                },                
                
                
            ],
            "attachments": [
                {
                    "color": f"{self.log_level_to_colors[log_level]}",
                    "fallback": "Ups, looks like something is not well",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": message
                            }
                        },
                        {
                            "type": "divider"
                        },
                    ], 

                }
            ]
        }
        return parsed_msg

    def parse_icinga2_msg(self, message, log_level: int=20):
        pass
    def parse_ubuntu_watchdog_msg(self, message, log_level: int=20):
        pass
    
    
    ## End of parsers 


    def send_message(self, message, log_level: str=20, parser=None):
        if isinstance(log_level, str):
            log_level = log_level.upper()
            log_level = self.log_level_to_int(log_level)
        if parser is None:
            message =self.default_parser(message, log_level)
        else:
            message = parser(message, log_level)

        if self.validate_message(message):
           result = requests_post(
                url=self.config.get_slack_hook(),
                json = message,
                headers={"Content-Type": "application/json"},
            )
        logger.debug(result)

    def get_slack_username(self) -> str:
        return self.slack_username 

    def get_slack_channel(self) -> str:
        return self.slack_channel







    