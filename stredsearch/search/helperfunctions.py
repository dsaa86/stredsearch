import re
import zoneinfo
from datetime import datetime

from django.utils.dateparse import parse_datetime


def removeBlankParams(keys_to_delete: list, params_dict: dict) -> dict:
        for key in keys_to_delete:
            del params_dict[key]

        return params_dict
def processFilters(params_dict: dict) -> dict:
    keys_to_delete = []

    # " " indicates a param not used in this search on the
    # part of the user.
    for key, value in params_dict.items():
        if value == " ":
            keys_to_delete.append(key)

        # Stack Exchange expects semi-colon delimited list
        if key in ["nottagged","tagged", "ids"]:
            params_dict[key] = value.replace(",", ";")

        # These elems must be int
        if key in ["answers", "views", "page", "pagesize", "answers", "user", "views"] and value != " ":
            invalid_chars_in_value = re.findall("[^0-9]", value)
            if len(invalid_chars_in_value) > 0:
                raise ValueError(f"Invalid value for {key}, none-int value provided")
            # This should never reach an exception after the regex check above....*should*
            try:
                params_dict[key] = int(params_dict[key])
            except ValueError:
                return {"error": { "ValueError" : f"Invalid value for {key}" }}

    params_dict = removeBlankParams(keys_to_delete, params_dict)

    return params_dict


def convertListToString(list_to_convert: list, delimiter: str = None) -> str:

    if not isinstance(list_to_convert, list):
        raise TypeError("list_to_convert must be of type list")
    if delimiter != None and not isinstance(delimiter, str):
        raise TypeError("delimiter must be of type string")
    if delimiter != None and delimiter != ",":
        raise TypeError("Delimiter must be None (default) or comma (',')")

    return_string = ""
    for index, value in enumerate(list_to_convert):
        return_string += value
        if delimiter != None and index + 1 != len(list_to_convert):
            return_string += f"{delimiter} "

    return return_string


def convertMSToDateTime(ms_value: int) -> object:

    if not isinstance(ms_value, int):
        raise TypeError("ms_value must be of type int")

    converted_value = datetime.fromtimestamp(ms_value)
    converted_value = converted_value.strftime("%Y-%m-%d %H:%M:%S")
    converted_value = parse_datetime(converted_value)
    converted_value.replace(tzinfo=zoneinfo.ZoneInfo("Asia/Dubai"))
    return converted_value
