import coloredlogs, logging
      
# create logger with 'spam_application'
logger = logging.getLogger("GameLitics")
coloredlogs.install(level='DEBUG')
coloredlogs.install(level='DEBUG', logger=logger)