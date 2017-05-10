from magpie import MagpieModel

magpie = MagpieModel()
path = "./../../datalabel/train"
magpie.init_word_vectors(path, vec_dim=100)
labels = ['Affirmed', 'Reversed']
magpie.batch_train(path, labels, nb_epochs=30)
magpie.save_word2vec_model('./../../datalabel/embeddings', overwrite=True)
magpie.save_scaler('./../../datalabel/scaler', overwrite=True)
magpie.save_model('./../../datalabel/model.h5')