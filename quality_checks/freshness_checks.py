from datetime import datetime

def check_file_freshness(file_date):

    today = datetime.today().date()

    delay = (
        today - file_date
    ).days

    return delay