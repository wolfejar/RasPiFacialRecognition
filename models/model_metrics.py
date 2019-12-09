from sklearn import metrics


class ModelMetrics:
    def __init__(self, model_id, y_true, y_pred, labels, loss_data):
        self.model_id = model_id
        self.y_true = y_true
        self.y_pred = y_pred
        self.labels = labels
        self.loss_data = loss_data
        self.confusion_matrix = self.gen_confusion_matrix()
        self.classification_report = self.set_precision_recall_accuracy()

    def gen_confusion_matrix(self):
        return metrics.confusion_matrix(y_true=self.y_true, y_pred=self.y_pred, labels=self.labels)

    def set_precision_recall_accuracy(self):
        return metrics.classification_report(y_true=self.y_true, y_pred=self.y_pred, labels=self.labels, digits=3,
                                             output_dict=True)
