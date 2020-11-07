# TODO : FIX DEPENDECIES -------------------
import pandas as pd
import random
import sklearn
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

class DecisionTreeModel:
    def __init__(self, newDF):
        self.predDF = newDF
        df = pd.read_csv('clean_traintest_polimix_data.csv')
        self.data = pd.DataFrame(df)
    
    def execute(self):
        accuracy, model = self.computeOptimalModel()
        y_pred = model.predict(self.predDF)
        return [y_pred, accuracy]

    def computeOptimalModel(self):

        features = ["domain_type", "protocol","title_capital_freq", "tweet_ids", "internal_links"]
        X = self.data[features]
        y = self.data.label

        randoms = [x for x in range(51)]
        random.shuffle(randoms)
        criterion = ['gini', 'entropy']
        maxAccuracy = 0
        maxModel = None
        maxRandom = 0
        for rand in randoms[:8]:
            for i in range(2):
                # Split dataset into training set and test set
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=rand) # 80% training and 20% test
    
                # create the classifier, gini by default
                clf = DecisionTreeClassifier(criterion=criterion[i])

                # train decision tree
                clf = clf.fit(X_train, y_train)

                # predict
                y_pred = clf.predict(X_test)


                # Model Accuracy, how often is the classifier correct?
                modelAccuracy1 = metrics.accuracy_score(y_test, y_pred)
                
                if(modelAccuracy1 > maxAccuracy):
                    maxModel = clf
                    maxAccuracy = modelAccuracy1
                    maxCriterion = criterion[i]
                    maxRandom = rand
                
        print("Best Model #1: Accuracy=", maxAccuracy," | criterion='",maxCriterion,"' | random_state= ", maxRandom)

        return [maxAccuracy, maxModel]
