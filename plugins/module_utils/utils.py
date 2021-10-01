from datetime import datetime


def convert_str_to_datetime(time: str):

    """
    convert string time to datetime object.
    :param time: example "2021-12-01"
    :return:
    """
    try:
        return datetime.strptime(time, '%Y-%m-%d')
    except ValueError:
        return None
