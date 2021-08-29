import os
import logging
import cli_ui

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Default actions
actions = ['mining', 'fishing', 'woodcutting']
def is_local():
    if os.environ.get('local'):
        return True
    else:
        return False

class BotAction():
    def __init__(self):
        self.action = ''


class ScrapingArguments():
    """
    ScrapingArguments - Basic handlers for arguments passed to the application at startup

    """
    def __init__(self):
        logger.info("Beginning to parse arguments")
        botActions = BotAction()
        self.__process_bot_actions(botActions)
        self.botAction = botActions

    def __process_bot_actions(self, botActions):
        if os.environ.get('action'):
            botActions.action = os.environ.get('action')
        else:
            botActions.action = cli_ui.ask_choice("Choose a botting action to take", choices=actions)

