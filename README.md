# Court Reversals

This projects aims to predict whether a court case will be reversed or affirmed by higher court based on data available from lower court.

**Disclaimer**: This projects aims to predict the outcome, but it can never be guaranteed what will be the actual result. Authors are not liable for usage of this project and further consequences occurring on basis of that.

## Use cases

- People can check before making appeal in higher court for possible predicted outcome. See disclaimer first.
- Law firms can check to see how will a case perform in higher court and prepare accordingly.
- Lawyers can take an inside look into why a case gets affirmed or reversed.

## Goals
- Predict whether a case will be affirmed or reversed with probabilities based on the data available from lower court.

## Branches

There are two branches of project:

- District to Circuit
- Circuit to Supreme

## Running

Two kind of approaches have been used for classification and both of which are ran from separate scripts:
- Non-NN:
    - Train: `python main.py --train ngram_folder`, see `helpers/utils.py` to see what kind of ngrams files are expected for court case text.
    - Predict: `python main.py --predict test_ngram_folder`, same format for ngrams should be used for test data.
   
- DNN:
    - Train: `python dnn/main.py --train --train_path dnn_data/train_test/ --test_path dnn_data/test --save_path dnn_save`, train data is text (not ngrams), test data is used for calculating validation accuracy and save path is where magpie models, embeddings and scalar are saved.
    - Predict: `python dnn/main.py --predict --test_path /media/apsdehal/Media/mlproject-data/dnn_data/test --save_path dnn_save`, test_path are text files on which prediction for affirm/reverse is to be done and `dnn_save` is folder where magpie model, embeddiing and scalar were saved in training.


## Dependencies

- `scikit-learn`: Use the latest version of `scikit-learn` master, there are some issues with gradient boosting classifier in latest version available on pip.
- `magpie`: Use the forked version of [magpie](https://github.com/MLCS-Spring2017-Project/magpie) with some changes made to suit needs of the project

## Paper and Poster

- Paper: [Link](https://github.com/MLCS-Spring2017-Project/reversals/blob/master/paper.pdf)
- Poster: [Link](https://github.com/MLCS-Spring2017-Project/reversals/blob/master/poster.pdf)

## Authors

District to circuit:

- Amanpreet Singh
- Sharan Agarwal

Circuit to Supreme:

- Karthik Venkatesan
- Simranjyot Singh

Mentors:

- Daniel Chen
- Elliot Ash
