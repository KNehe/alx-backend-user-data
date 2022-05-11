#!/usr/bin/env python3
"""
Module filtered_logger
"""
from typing import List
import re
import logging


PII_FIELDS = ('name', 'email', 'phone', 'password', 'ssn')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated"""
    msg = message
    for field in fields:
        pattern = field + "=.*?" + separator
        replace = field + "=" + redaction + separator
        msg = re.sub(pattern, replace, msg)
    return msg


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        return filter_datum(
                self.fields, self.REDACTION,
                super(RedactingFormatter, self).format(record),
                self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""

    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)
    return logger
