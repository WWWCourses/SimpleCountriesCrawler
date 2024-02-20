""" module setup_logging """

import logging

def setup_logger(name, level):
    """
    Set up and configure a logger with the specified name and logging level.

    Parameters:
        name (str): The name of the logger.
        level (int): The logging level to set for the logger.

    Returns:
        logging.Logger: A configured logger instance.

    Example:
        To set up a logger named 'my_logger' with INFO level:
        >>> my_logger = setup_logger('my_logger', logging.INFO)
    """
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a console handler and set the level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create a formatter and set the format
    format_str = '%(name)s:%(levelname)s:%(message)s'
    formatter = logging.Formatter(format_str)
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    # Modify the formatter to include path:lineno for DEBUG messages
    # if level == logging.DEBUG:
    #     format_str += '\n%(pathname)s:%(lineno)d'
    #     formatter = logging.Formatter(format_str)
    #     console_handler.setFormatter(formatter)

    return logger
