#!/usr/bin/env python3
import re


def filter_datum(field, redaction, message, separator):
    pattern = fr'(?<=\ {separator})({"|".join(field)})(?=(\ {separator}|$))'
    return re.sub(pattern, redaction, message)
