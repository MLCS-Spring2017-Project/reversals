from magpie import MagpieModel
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from glob import glob
import logging
import os

log = logging.getLogger(__name__)


class Predict:
    def __init__(self, config):
        self.config = config
        embeddings_path = os.path.join(self.config["save_path"], "embeddings", "embeddings")
        scaler_path = os.path.join(self.config["save_path"], "scaler", "scaler")
        model_path = os.path.join(self.config["save_path"], "model", "model.h5")

        if os.path.exists(embeddings_path) and os.path.exists(scaler_path) and os.path.exists(model_path):
            self.magpie = MagpieModel(
                keras_model=model_path,
                word2vec_model=embeddings_path,
                scaler=scaler_path,
                labels=['Affirmed', 'Reversed']
            )
        else:
            raise Exception("Model, scaler and embedded must be generated before predicting")

    def predict(self):
        test_path = os.path.join(self.config['test_path'], "**", "*.txt")
        files = glob(test_path, recursive=True)
        y = []
        predicted = []
        for fname in files:
            lab = fname[:-4] + ".lab"
            with open(lab, "r") as f:
                status = f.read()

            prediction = self.magpie.predict_from_file(fname)[0][0]
            predicted.append(prediction)
            y.append(status)

        encoder = LabelEncoder()
        y = encoder.fit_transform(y)
        predicted = encoder.transform(predicted)
        fpr, tpr, thresholds = metrics.roc_curve(y, predicted)

        log.info(metrics.f1_score(y, predicted, average="weighted"))
        log.info(metrics.accuracy_score(y, predicted))
        log.info(metrics.confusion_matrix(y, predicted))
