#!/usr/bin/env python3
import re
import logging
from typing import List


def filter_datum(fields, redaction, message, separator):
    temp = message
    for field in fields:
        temp = re.sub(field + "=.*?" + separator, field + "=" + redaction + separator, temp)
    return temp

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