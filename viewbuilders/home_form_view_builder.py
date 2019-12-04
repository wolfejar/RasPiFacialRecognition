from models.sql import SQL
from views.home_form import UserHomeForm
from models.table_data import TableData
from models.classification import Classification
from dateutil import tz, relativedelta
from datetime import datetime, timedelta


def build_home_form(user_id, time_frame):
    sql_instance = SQL()
    time_stamp = get_time_stamp(time_frame)
    active_model_id = sql_instance.get_active_model_id(user_id)
    print('Active model id:', active_model_id)
    if active_model_id is not None:
        results = sql_instance.load_model_classifications_since_time_stamp(model_id=active_model_id,
                                                                           time_stamp=time_stamp)
    else:
        results = []
    # need to convert these classifications to actual classification objects
    print(results)
    classifications = []
    for c in results:
        classifications.append(Classification(c[0], c[1], c[2], c[3], c[4], c[5]))
    table_data = TableData(classifications=classifications, time_frame=time_frame.name)
    chart_y_values = [data_point.confidence for data_point in table_data.data_points]
    chart_x_values = [data_point.timestamp for data_point in table_data.data_points]
    return UserHomeForm(table_data=table_data, chart_x_values=chart_x_values, chart_y_values=chart_y_values)


def get_time_stamp(time_frame):
    today = datetime.utcnow().date()
    if time_frame.name == 'Week':
        today = datetime.now()
        start = today - timedelta((today.weekday() + 1) % 7)
        last_sunday = start + relativedelta.relativedelta(weekday=relativedelta.SU(-1))
        return last_sunday
    elif time_frame.name == 'Month':
        return datetime(today.year, today.month, 1, tzinfo=tz.tzutc())
    elif time_frame.name == 'Year':
        return datetime(today.year, 1, 1, tzinfo=tz.tzutc())
    else:
        # return timestamp for beginning of current day
        return datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
