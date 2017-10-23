import pandas as pd
import numpy as np
import numpy.random as npr
from classifier import TrumpClassifier
import matplotlib.pyplot as plt

def get_reviews(path):
    data = pd.read_json(path, lines=True)

    positive = data[data.overall >= 5].reviewText.values
    neutral = data[data.overall == 3].reviewText.values
    negative = data[data.overall <= 1].reviewText.values

    return neutral[0:1000], positive[0:1000], negative[0:1000]


def split_data(X, y, ps=[0.8, 0.2]):
    I = npr.permutation(X.shape[0])
    X = X[I]
    y = y[I]
    Xsets = []
    Ysets = []
    start = 0
    for p in ps:
        end = start + round(len(X)*p)
        Xsets.append(X[start:end])
        Ysets.append(y[start:end])
        start = end
    return (Xsets[0], Ysets[0], Xsets[1], Ysets[1])
    

def main():

    neut, pos, neg = get_reviews('reviews.json')

    X = np.hstack([pos, neg, neut])
    y = np.hstack([np.zeros(len(pos)), np.ones(len(neg)), np.ones(len(neut))+1])
    classes = {0 : 'positive', 1 : 'negative', 2 : 'neutral'}

    X_train, y_train, X_test, y_test = split_data(X, y)

    trump = TrumpClassifier()
    trump.set_classes(classes)
    trump.train(X_train, y_train)

    data = pd.read_json('./tweets.json')
    predictions = trump.predict(data.text, numeric=False)
    data['sentiment'] = predictions
    print(data)

    plt.hist(predictions[predictions == 0], bins=5, color='green', edgecolor='black')
    plt.hist(predictions[predictions == 1], bins=5, color='red', edgecolor='black')
    plt.hist(predictions[predictions == 2], bins=5, color='yellow', edgecolor='black')
    plt.show()

    print("SCORE ON TEST SET: %f" % trump.score(X_test, y_test))
    
    while True:
        print("Enter a sentece to be evaluated...")
        sentence = input()
        print("\t%s" % trump.predict([sentence]))

if __name__ == '__main__':
    main()
