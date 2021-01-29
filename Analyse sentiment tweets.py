#Importation de librairies

import pandas as pd
import numpy as np
import re
import string
import nltk
#nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import  RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import StackingClassifier
from sklearn.svm import SVC
import mysql.connector
from mysql.connector import  Error
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS

stop_words = set(stopwords.words('english'))
sentiment = SentimentIntensityAnalyzer()

#Fonction pour charger le jeu de données
def load_dataset(filename):
    dataset = pd.read_csv(filename, encoding='latin-1')
    dataset['sentiment'] = dataset["Messages"].apply(lambda x: sentiment.polarity_scores(str(x))['compound'])
    dataset['sentiment_label'] = dataset["sentiment"].apply(lambda x: 4 if (x > 0) else (0 if (x < 0) else 2))
    return dataset

#Suppression des colonnes indesirables
def remove_unwanted_cols(dataset, columns):
    for column in columns:
        del dataset[column]
    return dataset

#Pré-traitements des tweets
def preprocess_tweet_text(tweet):
    str(tweet).lower()
    # suppressions des urls
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', str(tweet), flags=re.MULTILINE)
    # Suppression des utilisateurs @ de references et les '#' venant des tweets
    tweet = re.sub(r'\@\w+|\#', '', tweet)
    tweet = re.sub('[^A-Za-z0-9]+', ' ', tweet)
    # Suppressions des punctuations
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))
    # Suppression des mots vides
    tweet_tokens = word_tokenize(tweet)
    filtered_words = [w for w in tweet_tokens if not w in stop_words]

    ps = PorterStemmer()
    stemmed_words = [ps.stem(w) for w in filtered_words]
    lemmatizer = WordNetLemmatizer()
    lemma_words = [lemmatizer.lemmatize(w, pos='a') for w in stemmed_words]

    return " ".join(filtered_words)

#Conversion des tokens en vecteurs
def get_feature_vector(train_fit):
    vector = TfidfVectorizer(sublinear_tf=True)
    vector.fit(train_fit)
    return vector

#Ré-étiquetons en string les labels.
def int_to_string(sentiment):
    if sentiment == 0:
        return "Negative"
    elif sentiment == 2:
        return "Neutral"
    else:
        return "Positive"

def world_cloud(data,column):

    tweet_words = ''
    stopwords = set(STOPWORDS)


    for val in data[column]:


        val = str(val)

        # division de la phrase en mot
        tokens = val.split()

        # conversion des token en minuscule
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        tweet_words += " ".join(tokens) + " "
    wordcloud = WordCloud(width=800, height=800,
                              background_color='black',
                              stopwords=stopwords,
                              min_font_size=10).generate(tweet_words)

    # Affichage du nuage de mot
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()


######################## APPLICATION ################################
#######################################################################

#Fonction pour charger le jeu de données
dataset = load_dataset("Twitter_data.csv")

#dataset['sentiment'].to_csv("polarity.csv")


#Suppression des colonnes indésirables
n_dataset = remove_unwanted_cols(dataset, ['Unnamed: 0', '_Id', 'Id', 'Created_at', 'Name', 'Location','Followers', 'sentiment'])


#Pré-traitements des tweets
n_dataset.Messages = n_dataset['Messages'].apply(preprocess_tweet_text)
#n_dataset.to_csv("clean_data.csv")

                            ################ AFFICHAGE DU NUAGE DE MOTS ###########

world_cloud(n_dataset,"Messages")


                             ################## ENTRAINEMENT ######################

#Vectorisation des tweets en vecteurs numériques
tf_vector = get_feature_vector(np.array(n_dataset.iloc[:, 0]).ravel())
X = tf_vector.transform(np.array(n_dataset.iloc[:, 0]).ravel())
y = np.array(n_dataset.iloc[:, 1]).ravel()

# Création du modèle
estimators = [('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
              ('svr', LinearSVC(random_state=42)),
              ('NB', MultinomialNB()),
              ('SGDclassifier', SGDClassifier()),
              ('GBC', GradientBoostingClassifier()),

             ]
stack = StackingClassifier(estimators=estimators,
                           final_estimator=LogisticRegression()
                           )

#Division du jeu de données en Train, Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


stack.fit(X_train, y_train)
y_predict = stack.predict(X_test)
print(accuracy_score(y_test, y_predict))
'''
                        ################## TEST ######################

test_file_name = "Test_Twitter_data.csv"
test_ds = load_dataset(test_file_name)
test_ds['sentiment'].to_csv("test_polarity.csv")
test_ds = remove_unwanted_cols(test_ds,  ['Unnamed: 0', '_Id', 'Id', 'Created_at', 'Name', 'Location','Followers', 'sentiment'])

# Nettoyage des données de tests
test_ds["Messages"] = test_ds["Messages"].apply(preprocess_tweet_text)
test_feature = tf_vector.transform(np.array(test_ds.iloc[:, 1]).ravel())

# Prediction avec le modele de reference
test_prediction = stack.predict(test_feature)

# Creation de dataframe comportant le label et la prediction
test_result_ds = pd.DataFrame({'label': test_ds['sentiment_label'].apply(int_to_string), 'prediction':test_prediction})
test_result_ds.columns = ['label', 'predictions']
test_result_ds['predictions'] = test_result_ds['predictions'].apply(int_to_string)

print(test_result_ds)
'''

   ############################# INSERTION DES RESULTATS DE PREDICTION POUR LA VISUALISATION ###################################
"""
def DataFrameToSql(dataframe):

    try:

        conn = mysql.connector.connect(host='localhost', user='root', password='tito2010',database='employee')
        cur = conn.cursor()
        cur.execute(" delete from label")
        conn.commit()

        for (row, rs) in dataframe.iterrows():

            sentiment = rs[0]
            counts = str(int(rs[1]))

            query = " insert into label values('" + sentiment + "'," + counts + ");"
            cur.execute(query)
        conn.commit()
        cur.close()
    except  Error as e:
        print("Error in Mysql connection = " ,e)
    finally:
        conn.close()

#predictions = test_result_ds.groupby(['predictions'], as_index=False)['predictions'].agg({'count': 'count'})
label = test_result_ds.groupby(['label'], as_index=False)['label'].agg({'count': 'count'})

DataFrameToSql(label)

"""
