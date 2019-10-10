import views.home_form as home_form
from models.sql import SQL
from views.home_form import UserHomeForm
from models.table_data import TableData
from models.classification import Classification


def build_home_form(model_id, time_frame):
    sql_instance = SQL()
    classifications = sql_instance.load_model_classifications_by_time_frame(model_id=model_id, time_frame=time_frame)
    table_data = TableData(classifications=classifications, time_frame=time_frame)
    chart_y_values = [data_point.confidence for data_point in table_data.data_points]
    chart_x_values = [data_point.timestamp for data_point in table_data.data_points]
    return UserHomeForm(table_data=table_data, chart_x_values=chart_x_values, chart_y_values=chart_y_values)
