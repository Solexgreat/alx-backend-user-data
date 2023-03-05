#!/usr/bin/env python3
import re
import logging
from typing import List


PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')

def filter_datum(fields, redaction, message, separator):
    temp = message
    for field in fields:
        temp = re.sub(field + "=.*?" + separator, field + "=" + redaction + separator, temp)
    return temp

def get_logger() -> logging.Logger:
    """ Returns logger obj  """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: str) -> List:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        method to format the log message.

        """
        return filter_datum(self.fields, self.REDACTION, super(RedactingFormatter, self)
                            .format(record), self.SEPARATOR)