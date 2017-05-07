from magpie import MagpieModel
import os


class Trainer:
    def __init__(self, config):
        self.config = config
        self.magpie = MagpieModel()

    def train(self):
        print("Init work vectors, start")
        self.magpie.init_word_vectors(self.config["train_path"], vec_dim=200)
        print("Init work vectors, done")
        self.labels = ["Affirmed", "Reversed"]
        print("Starting train")
        self.magpie.batch_train(self.config["train_path"], labels, test_dir=self.config["test_path"], nb_epochs=1)
        print("Trained")

    def save(self):
        embeddings_path = os.path.join(self.config["save_path"], "embeddings", "embeddings")
        scalar_path = os.path.join(self.config["save_path"], "scalar", "scalar")
        model_path = os.path.join(self.config["save_path"], "model", "model.h5")
        self.magpie.save_word2vec_model(embeddings_path, overwrite=True)
        self.magpie.save_scaler(scalar_path, overwrite=True)
        self.magpie.save_model(model_path, overwrite=True)
