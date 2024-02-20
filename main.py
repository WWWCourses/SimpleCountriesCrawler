""" main.py """
import sys
import logging

from src.utils.setup_logging import setup_logger
from src.utils.config_loader import load_config

from src.gui.gui_app import MainApp

logger = setup_logger('app', logging.INFO)



if __name__=='__main__':
    data_processing_config = load_config('./src/config.ini', 'data_processing')
    target_url = data_processing_config['target_url']

    app = MainApp(sys.argv)
    sys.exit(app.exec())
