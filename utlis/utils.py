import datetime
from datetime import timedelta
import pytz


class DateTimeUtils:
    """
    A utility class for handling date and time operations.

    """

    @staticmethod
    def get_current_utc_time() -> datetime.datetime:
        """
        Returns the current time in UTC.

        Returns:
            datetime.datetime: The current time in UTC.
        """
        local_now = datetime.datetime.now(pytz.timezone("UTC"))
        return DateTimeUtils.format_time(local_now)

    @staticmethod
    def format_time(date_time: datetime.datetime) -> datetime.datetime:
        """
        Formats a datetime object to the format '%Y-%m-%d %H:%M:%S'.

        Args:
            date_time (datetime.datetime): The datetime object to format.

        Returns:
            datetime.datetime: The formatted datetime object.
        """

        return date_time.replace(microsecond=0)
