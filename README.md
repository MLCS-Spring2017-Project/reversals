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
