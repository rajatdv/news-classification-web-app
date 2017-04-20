
# coding: utf-8

# <h1>NEWS HEADLINE CLASSIFICATION</h1>  
# 
# <p>In this notebook we will try to classify news using <b>MULTINOMIAL NAIVE BAYES</b>. We will convert text into vector by using <b>Bag Of Words</b> model. We will use two different datasets from two differrent sources and merge them.Our objective is to find maximum accuracy possible</p> 

# In[1]:

##Loading all the required libraries
import pandas as pd
import numpy as np

from sklearn.naive_bayes import MultinomialNB

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score
import time

#library for regular expretion
import re


# In[2]:

#Loading the data which is from Kaggle
#This dataset contains four news class -b for business, e- entertainment, -t for technology and science, -m for medical
data = pd.read_csv("uci-news-aggregator.csv",encoding='latin-1')


# In[3]:

#Loading another data which contain 5 different class of news
#Nature_Environment , Politics, Lifestyle, Business_finance and Health
data1 = pd.read_csv("ArticlesNewsSitesData_2382.csv",sep=';')
data1.columns = ['TITLE','CATEGORY']
#data1.head()


# In[4]:

#Extracting news haedline from urls 
for i in range(2382):
    data1.TITLE[i] = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))', '', data1.TITLE[i])
    data1.TITLE[i] = re.sub(r'(\/[0-9]*\/)*[0-9]*\/', '', data1.TITLE[i])
    data1.TITLE[i]=data1.TITLE[i].replace("-"," ")
    



# In[ ]:




# In[5]:

data1['TITLE'].replace('', np.nan, inplace=True)
#data1.tail()


# In[6]:

data1.dropna(subset=['TITLE'], inplace=True)
#data1.tail()


# In[7]:

data = data[['TITLE','CATEGORY']]


# In[8]:

#Merging both datasets
temp=[data,data1]
news_data = pd.concat(temp)
#Printing all different types of categories
#news_data.CATEGORY.unique()


# In[9]:

#news_data.groupby('CATEGORY').describe()


# In[10]:

#converting category column into numeric target NUM_CATEGORY column
news_data['NUM_CATEGORY']=news_data.CATEGORY.map({'b':0,'e':1,'m':2,'t':3,'Economy-Business_Finance':0,'Health':2,'Lifestyle_leisure':2,'Nature_Environment':4,'Politics':0,'Science_Technology':3})
#news_data.head()


# In[11]:

#Splitting dataset into 60% training set and 40% test set
x_train, x_test, y_train, y_test = train_test_split(news_data.TITLE, news_data.NUM_CATEGORY, random_state=50)


# In[12]:

#Here we convert our dataset into a Bag Of Word model using a Bigram model
#start = time.clock()

vect = CountVectorizer(ngram_range=(2,2))
#converting traning features into numeric vector
X_train = vect.fit_transform(x_train)
#converting training labels into numeric vector
X_test = vect.transform(x_test)

#print (time.clock()-start)



# In[13]:

#Training and Predicting the data

#start = time.clock()

mnb = MultinomialNB(alpha =0.2)

mnb.fit(X_train,y_train)

result= mnb.predict(X_test)

#print (time.clock()-start)


# In[14]:

#Printing accuracy of the our model
#accuracy_score(result,y_test)


# In[15]:

#This function return the class of the input news
def predict_news(news):
    test = vect.transform(news)
    pred= mnb.predict(test)
    if pred  == 0:
        return 'Business and Politics'
    elif pred == 1:
        return 'Entertainment'
    elif pred == 2:
        return 'Health and Lifestyle'
    elif pred == 3:
        return 'Science and Technology'
    else:
        return 'Environment'
    
    
#'Lifestyle_leisure':4,'Nature_Environment':5,'Politics':6,

