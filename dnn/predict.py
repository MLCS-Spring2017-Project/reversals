from magpie import MagpieModel
from sklearn import metrics


class Predict:
    def __init__(self, config):
        self.config = config
        embeddings_path = os.path.join(self.config["save_path"], "embeddings", "embeddings")
        scalar_path = os.path.join(self.config["save_path"], "scalar", "scalar")
        model_path = os.path.join(self.config["save_path"], "model", "model.h5")

        if os.path.exists(embeddings_path) and os.path.exists(scalar_path) and os.path.exists(model_path):
            self.magpie = MagpieModel(
                keras_model=model_path,
                word2vec_model=embeddings_path,
                scaler=scalar_path,
                labels=['Affirmed', 'Reversed']
            )
        else:
            raise Exception("Model, scalar and embedded must be generated before predicting")

    def predict(self):
        curr_dir = os.getcwd()
        os.chdir(config["test_path"])

        files = glob("./**/*.txt")
        y = []
        predicted = []
        for fname in files:
            lab = fname[-4] + ".lab"
            with open(lab, "r") as f:
                status = f.read()

            prediction = self.magpie.predict_from_file(fname)[0]
            predicted.append(prediction)
            y.append(status)

        os.chdir(curr_dir)
        fpr, tpr, thresholds = metrics.roc_curve(y, predicted_status)

        print(metrics.auc(fpr, tpr))
        print(metrics.confusion_matrix(y, predicted_status))
