"""This module provides functions for loading configuration from a specified file."""

import configparser
import os
import logging


from src.utils.setup_logging import setup_logger

logger = setup_logger('config_loader', logging.DEBUG)

class ConfigError(Exception):
    """Custom exception for errors related to configuration loading and parsing."""

    def __init__(self, message):
        """ Initializes a new ConfigError object with a specific message.

            Args:
                message: A detailed description of the error encountered.
        """
        super().__init__(message)


def load_config(filename, section)->dict:
    """Loads configuration from a specified file, handling potential errors.

        Args:
            filename: Path to the configuration file.
            section: Name of the configuration section to load.

        Returns:
            Dictionary containing the configuration data for the specified section.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            ConfigError: If there are errors in configuration structure or content.
    """

    config = configparser.ConfigParser()

    try:
        # Check if the config file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Error: Configuration file '{filename}' not found")

        config.read(filename)

        return dict(config[section])
    except KeyError as e:
        message = f"Missing configuration section: {section} in {filename}"
        logger.error(message)
        raise ConfigError(message) from e
    except FileNotFoundError as e:
        message = f"Error: CONFIGURATION FILE '{os.path.abspath(filename)}' not found"
        logger.error(message)
        raise ConfigError(message) from e
    except configparser.Error as e:
        message = f"Error reading configuration file: {e}"
        logger.error(message)
        raise ConfigError(message) from e


