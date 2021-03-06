# Natural Language Processing

#%% Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import keras
from keras import Sequential                     
from nltk.stem.porter import PorterStemmer

#%% Importing the dataset
dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)
# parameter delimiter = '\t': file được đọc ngăn cách bởi dấu tab => đọc file tsv
# .tsv nghĩa là: Tab Separated Values
# quoting = 3: bỏ qua các kí tự "",'',...

#%% Cleaning the texts
import re


#%% mở file chứa stopwords
stopwords = []
file = open('stopwords.txt', "r")
try:
    content = file.read()
    stopwords_list = content.split(",")
    for stopword in stopwords_list:
        s = stopword.replace('"','')
        s = s.strip()
        stopwords.append(s)
finally:
    file.close()
#%%

corpus = [] #chứa các reviews đã qua các bước lọc
for i in range(0, dataset.shape[0]):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i]) #loại bỏ các phần không phải
        #là chữ cái, thay thế bằng dấu spaces
        #^: not
        #a-zA-Z: a to z nor A to Z
        #' ': space
    review = review.lower() # all to lowercase
    review = review.split() # split to words
    ps = PorterStemmer() # ran => run,....
    review = [ps.stem(word) for word in review if not word in set(stopwords)] # chuyển về nguyên
    # mẫu các từ không có trong stopwords
    review = ' '.join(review) # nối lại các từ thành câu
    corpus.append(review)


#%% Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 2000) # chọn ra 2000 từ
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, -1].values

#%% Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 1)

#%% 

def preprocess_review_input(review):
    new_review = review
    new_review = re.sub('[^a-zA-Z]', ' ', new_review)
    new_review = new_review.lower()
    new_review = new_review.split()
    ps = PorterStemmer()
    new_review = [ps.stem(word) for word in new_review if not word in set(stopwords)]
    new_review = ' '.join(new_review)
    new_corpus = [new_review]
    new_X_test = cv.transform(new_corpus).toarray()
    return new_X_test

#%% ANN model
from keras import layers
model = Sequential()
input_dim = X_train.shape[1] # input đầu vào bằng với số từ của tập dữ liệu
model = Sequential()
model.add(layers.Dense(300, input_dim=input_dim, activation='relu'))
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(20, activation='relu'))
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid')) # đầu ra là giá trị từ 0 đến 1

model.compile(loss='binary_crossentropy',              
              optimizer='adam',               
              metrics=['accuracy'])

history = model.fit(X_train, y_train,
                     epochs=100,
                     verbose=1,
                     validation_data=(X_test, y_test),
                     batch_size=10)
loss1, accuracy1 = model.evaluate(X_train, y_train, verbose=1)
loss2, accuracy2 = model.evaluate(X_test, y_test, verbose=1)
print("Training Accuracy: {:.4f}".format(accuracy1))
print("Testing Accuracy:  {:.4f}".format(accuracy2))


#%% print 
# def weight_of_model(model):
#     weights = []
#     for layer in model.layers:
#         weights.append(np.array(layer.get_weights()))
#     return np.array(weights)
# w = weight_of_model(model)
#%%
# y_pred=model.predict(review_input('If I could I would’ve given it zero stars. I opened my veggie bowl and found a giant piece of hardened avocado which had gone bad. Sometimes this location does amazing, sometimes horrible.'))

def review_input(review):
    y_pred=model.predict(preprocess_review_input(review))
    print(y_pred)
    return y_pred[0][0]





#%% test


acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1,len(acc)+1)

plt.plot(epochs, acc,'bo', label='Training accuracy')

plt.plot(epochs, val_acc,'b', label='Validation accuracy')
plt.ylim([0,1])
plt.title('')
plt.legend()
plt.show()