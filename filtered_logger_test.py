#!/usr/bin/env python3
import re
import logging
from typing import List
from mysql.connector import connection
from os import environ


PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')

def filter_datum(fields, redaction, message, separator):
    temp = message
    for field in fields:
        temp = re.sub(field + "=.*?" + separator, field + "=" + redaction + separator, temp)
    return temp


def get_logger() -> logging.Logger:
    """
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))

def get_db() -> connection.MySQLConnection:
    username = environ.get("PERSONAL_DATA_DB_USERNAME", 'root') 
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", '')
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    connector = connection.MySQLConnection(
        user = username,
        password=password,
        host= db_host,
        database= db_name
    )
    return

def main():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")

    for row in cursor:
        name = row[1]
        email = row[2]
        phone = row[3]
        ssn = row[4]
        password = row[5]
        ip = row[6]
        last_login = row[7]
        user_agent = row[8]

        # Format the output string
        output_str = f'[HOLBERTON] user_data INFO: name={name[:3]}***; email={email[:3]}***; phone={phone[:3]}***; ssn={ssn[:3]}***; password={password[:3]}***; ip={ip}; last_login={last_login}; user_agent={user_agent};\nFiltered fields:\n\nname\nemail\nphone\nssn\npassword'

        # Print the output string
        print(output_str)

    db.close()

if __name__ == '__main__':
    main()


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