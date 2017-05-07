import sys
import argparse
import os
from train import Trainer
from predict import Predict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--train", action="store_true")
    parser.add_argument("-r", "--train_path", action="store")
    parser.add_argument("-e", "--test_path", action="store")
    parser.add_argument("-s", "--save_path", action="store")
    parser.add_argument("-p", "--predict", action="store_true")
    args = parser.parse_args()

    if args.train:
        config = {"train_path": args.train_path,
                  "test_path": args.test_path,
                  "save_path": args.save_path}
        trainer = Trainer(config)
        trainer.train()
        trainer.save()
        return

    if args.predict:
        config = {"test_path": args.test_path,
                  "save_path": args.save_path}
        predict = Predict(config)
        predict.predict()

        return


if __name__ == '__main__':
    main()
