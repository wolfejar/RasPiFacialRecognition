import model_train_pipeline as mtp
from views.metrics_form import MetricsForm
import pickle
import os


def build_metrics_form(home_user_id):
    active_model_id = mtp.get_active_id(home_user_id)
    metrics_dir = os.path.abspath('./static/models/metrics/' + str(home_user_id) + '/' + str(active_model_id)
                                  + '.pickle')
    metrics = pickle.loads(open(metrics_dir, "rb").read())
    return MetricsForm(metrics)
