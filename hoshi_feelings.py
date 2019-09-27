import pickle
import nltk
from nltk.corpus import movie_reviews
from os.path import exists
from nltk.classify import apply_features
from nltk.tokenize import word_tokenize, sent_tokenize


class Feelings:
    def __init__(self,classifier):

        self.classifier= self.load_classifier(classifier)
        documents = [(list(movie_reviews.words(fileid)), category)
                     for category in movie_reviews.categories()
                     for fileid in movie_reviews.fileids(category)]

        all_words = []
        for w in movie_reviews.words():
            all_words.append(w.lower())
        all_words = nltk.FreqDist(all_words)
        word_features = list(all_words.keys())
        # print(word_features)

    def find_features(document):
        words = set(document)
        features = {}
        for w in word_features:
            features[w] = (w in words)
        return features


    def train(self):
        featuresets = [(find_features(rev), category) for (rev, category) in documents]
        numtrain = int(len(documents) * 90 / 100)
        training_set = apply_features(find_features, documents[:numtrain])
        testing_set = apply_features(find_features, documents[numtrain:])

        classifier = nltk.NaiveBayesClassifier.train(training_set)
        classifier.show_most_informative_features(15)





    def load_classifier(self,classify):
        classifier_f = open(classify, "rb")
        classifier = pickle.load(classifier_f)
        classifier_f.close()

        return classifier




    def classify(self,sentence):

        doc = word_tokenize(sentence.lower())
        featurized_doc = {c:True for c in sentence.split()}
        tagged_label = self.classifier.classify(featurized_doc)
        if tagged_label== 'neg':
            print('that comment is negative')
            return True
        else:
            print('that comment is positive or neutral')
            return False
        print(tagged_label)
