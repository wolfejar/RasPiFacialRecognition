from dateutil.tz import tzutc
from models.sql import SQL
from views.home_form import UserHomeForm
from models.table_data import TableData
from models.classification import Classification
from dateutil import tz, relativedelta
from datetime import datetime, timedelta


def build_home_form(model_id, time_frame):
    sql_instance = SQL()
    time_stamp = get_time_stamp(time_frame)
    classifications = sql_instance.load_model_classifications_since_time_stamp(model_id=model_id, time_stamp=time_stamp)
    # need to convert these classifications to actual classification objects
    table_data = TableData(classifications=classifications, time_frame=time_frame)
    chart_y_values = [data_point.confidence for data_point in table_data.data_points]
    chart_x_values = [data_point.timestamp for data_point in table_data.data_points]
    return UserHomeForm(table_data=table_data, chart_x_values=chart_x_values, chart_y_values=chart_y_values)


def get_time_stamp(time_frame):
    today = datetime.utcnow().date()
    if time_frame.name == 'week':
        today = datetime.now()
        start = today - timedelta((today.weekday() + 1) % 7)
        last_sunday = start + relativedelta.relativedelta(weekday=relativedelta.SU(-1))
        return last_sunday
    elif time_frame.name == 'month':
        return datetime(today.year, today.month, 0, tzinfo=tz.tzutc())
    elif time_frame.name == 'year':
        return datetime(today.year, 0, 0, tzinfo=tz.tzutc())
    else:
        # return timestamp for beginning of current day
        return datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
