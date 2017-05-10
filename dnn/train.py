from magpie import MagpieModel
import os
import logging
log = logging.getLogger(__name__)


class Trainer:
    def __init__(self, config):
        self.config = config
        embeddings_path = os.path.join(self.config["save_path"], "embeddings", "embeddings")
        scaler_path = os.path.join(self.config["save_path"], "scaler", "scaler")

        if os.path.exists(embeddings_path):
            self.magpie = MagpieModel(word2vec_model=embeddings_path)
        else:
            self.magpie = MagpieModel()

        if os.path.exists(scaler_path):
            self.magpie.load_scaler(scaler_path)

    def train(self):
        if not self.magpie.word2vec_model:
            log.info("Init work vectors, start")
            self.magpie.init_vectors(self.config["train_path"])
            log.info("Init work vectors, done")

        if not self.magpie.scaler:
            log.info("Starting scaler")
            self.magpie.fit_scaler(self.config["train_path"])
            log.info("Starting scaler")

        self.labels = ["Affirmed", "Reversed"]
        log.info("Starting training")
        self.magpie.batch_train(self.config["train_path"], self.labels, test_dir=self.config["test_path"], nb_epochs=30)
        log.info("Trained")

    def save(self):
        embeddings_path = os.path.join(self.config["save_path"], "embeddings", "embeddings")
        scaler_path = os.path.join(self.config["save_path"], "scaler", "scaler")
        model_path = os.path.join(self.config["save_path"], "model", "model.h5")
        # self.magpie.save_word2vec_model(embeddings_path, overwrite=True)
        self.magpie.save_scaler(scaler_path, overwrite=True)
        self.magpie.save_model(model_path)
