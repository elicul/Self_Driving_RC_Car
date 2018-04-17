from PIL import Image
import requests
import numpy as np
from io import BytesIO
from os import listdir
from os.path import isfile, join
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import json

X = []
y = []

def status_to_number(status):
    if status['forward'] and status['left']:
        return 5
    if status['forward'] and status['right']:
        return 6
    if status['backward'] and status['left']:
        return 7
    if status['backward'] and status['right']:
        return 8
    if status['forward']:
        return 1
    if status['backward']:
        return 2
    if status['left']:
        return 3
    if status['right']:
        return 4
    return 0

files_name = [f for f in listdir('collector/data') if isfile(join('collector/data', f)) and f != '.DS_Store']
for name in files_name:
    try:
        if len(name) is 17: # if .jpg
            image_as_array = np.asarray(
                np.ndarray.flatten(
                    np.array(Image.open(join('collector/data', name)).convert('L'))
                )
            )
            with open(join('./collector/data', name.split('.')[0] + '.json')) as statusFile:
                status = json.loads(statusFile.read())
            X.append(image_as_array)
            y.append(status_to_number(status))
    except Exception as inst:
        print(name)
        print(inst)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, random_state=1)

clf.fit(X_train, y_train)
clf.score(X_test, y_test)

joblib.dump(clf, 'model.pkl')