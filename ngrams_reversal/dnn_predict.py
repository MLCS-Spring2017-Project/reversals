from magpie import MagpieModel
import os
from sklearn import metrics

model = MagpieModel(
    keras_model='./../../datalabel/model.h5',
    word2vec_model='./../../datalabel/embeddings',
    scaler='./../../datalabel/scaler',
    labels=['Affirmed', 'Reversed']
)

test_path = './../../datalabel/test'

y_true = []
y_pred = []

for root, dirs, files in os.walk(test_path):
    for file in files:
        if file.endswith('.txt'):
            caseid = file.replace('.txt', '')
            test_label = caseid + '.lab'
            with open(os.path.join(root, test_label), 'r') as f:
                status = f.read()
                # print(status)
                if status == 'Affirmed':
                    y_true.append(0)
                else:
                    y_true.append(1)
            prediction_probability = model.predict_from_file(os.path.join(root,file))
            # print(prediction_probability)
            prediction = prediction_probability[0][0]            
            if prediction == 'Affirmed':
                y_pred.append(0)
            else:
                y_pred.append(1)
            if prediction == 'Affirmed' and status == 'Reversed':
                print(caseid)
                print(prediction_probability)

print('Accuracy: ', metrics.accuracy_score(y_true,y_pred))
print('AUC-ROC: ', metrics.roc_auc_score(y_true, y_pred))
print('Confusion matrix: \n', metrics.confusion_matrix(y_true, y_pred))
print('F1 score: ', metrics.f1_score(y_true, y_pred))

