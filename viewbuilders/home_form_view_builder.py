import views.home_form as home_form
from models.sql import SQL
from views.home_form import UserHomeForm
from models.graph_data import GraphData
from models.classification import Classification


def build_home_form(model_id, time_frame):
    sql_instance = SQL()
    classifications = sql_instance.load_model_classifications_by_time_frame(model_id=model_id, time_frame=time_frame)
    graph_data = GraphData(classifications=classifications, time_frame=time_frame)
    return UserHomeForm(graph_data=graph_data)
