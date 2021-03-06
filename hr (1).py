# -*- coding: utf-8 -*-
"""HR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/alishayakmal/HR-attrition-and-budgeting-/blob/master/HR.ipynb

# Importing files into Google Colabs
"""

#upload the file from running this code (importing the dataset)
#from google.colab import files
#files.upload()

"""# Installing Environment"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd   
import numpy as np    
import io
import matplotlib.pyplot as plt 
# %matplotlib inline
# %config InlineBackend.figure_formats = ['retina']
import seaborn as sns
import time
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import cross_val_score, KFold, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVC, SVC
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, auc, roc_curve, log_loss
SEED = 42
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# %matplotlib inline
import pylab as pl
from sklearn.metrics import roc_curve, auc

# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

# data visualisation and manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
import missingno as msno

#configure
# sets matplotlib to inline and displays graphs below the corressponding cell.
# % matplotlib inline  
style.use('fivethirtyeight')
sns.set(style='whitegrid',color_codes=True)

#import the necessary modelling algos.
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB

#model selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix,roc_curve,roc_auc_score
from sklearn.model_selection import GridSearchCV

from imblearn.over_sampling import SMOTE

#preprocess.
from sklearn.preprocessing import MinMaxScaler,StandardScaler,LabelEncoder,OneHotEncoder


from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

"""# Exploratory Data Analysis

Below we are reading the document to see the summary of the data .In this dataset it contains **1470 **rows and **35 **columns. 
It also shows the average of each column such as average age in the company is **36** with **2.7 rating **for job statisfaction.The least amount of budget spent on  an employee is **1009 **with a minimum  increase of  **3% **in their salary per year.Standhours in this company an employee spent is **80 hours**  per week who  would   remain in the same role for **less than** 8 years. On average employees remain in the company for **7 years **spending **4 years** with the current managers
```
"""

HR = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition (1).csv')


HR.describe()

"""There is no missing data and there are 35 attribute in which **74%** are integers and **25%** are object"""

HR.isnull().values.any()

"""**Life Science** are mostly hired , there are **more** male than female .Sales department has the **largest number **of employees in the company"""

#Print all of the object data types and their unique values 
for column in HR.columns: 
  if HR[column].dtype == object:
     print(str(column) + ':' + str(HR[column].unique()))
     print(HR[column].value_counts())
     print('_____________________________')

"""Several numerical features are rightly skewed therefore data transformation methods may be required to approach a normal distrubituon prior to fitting a model to the data.

This also shows most employees in this company are between **25 and 45 years** old
"""

HR.hist(figsize = (20,20),color = 'Purple')

"""There are total of **1470** employee in which **16%** of them left the company. Below we are going to visualize  different attribute to understand what caused the employees to leave"""

print(HR.Attrition.value_counts())
print(HR.Attrition.value_counts(normalize=True))
HR['Attrition'].value_counts().plot(kind= 'bar', color=('Purple','green')).set_title('Attrition')

"""This figure show most employee who leave have a job role in  either **Sales Executives** or **Research Scientist **"""

#job role has the most impact on attrition  we can sales attirition has the most job role 
print(HR.JobRole.value_counts().mean())
print(HR.JobRole.value_counts().mean())

sns.axes_style('whitegrid')
sns.catplot('JobRole', data=HR, aspect=3, kind='count', hue='Attrition', palette=['purple', 'green']).set_ylabels('Number of Employees')

"""On average employee who leave the company are between **29 and 31**

*   List item
*   List item
"""

plt.subplots(figsize =(13,4))
sns.countplot(x='Age', hue ='Attrition',data = HR ,palette = ('purple','green'))

"""This shows employee count and standard hours needs to be removed"""

corr=HR.corr()
corr=(corr)
plt.figure(figsize=(10, 10))
sns.heatmap(corr,
           xticklabels=corr.columns.values,
           yticklabels=corr.columns.values,cmap='Purples')
#Monthly income,Job level are dependent upon the TotalWorkingYears
#PerformanceRating is highly correlated with PercentSalaryhikeing

"""Dropping irrelavant columns:

1) All employees are over18 therefore this column is irrelavant

2)Employee numbers are unique identifier hence doesnt have any value 

3)Standhours in the company for each employee is 80

4) Employee count brings doesnt add value
"""

HR = HR.drop('Over18', axis =1 )
HR = HR.drop('EmployeeNumber', axis = 1 )
HR = HR.drop('StandardHours',axis =1 )
HR = HR.drop('EmployeeCount', axis =1 )

"""This shows the number of years worked decide  the job level of the employees and the monthly income.The higher job level,higher performance rating  then higher the salary increase."""

corr=HR.corr()
corr=(corr)
plt.figure(figsize=(12, 12))
sns.heatmap(corr,annot= True,fmt='.0%',
           xticklabels=corr.columns.values,
           yticklabels=corr.columns.values,cmap='Purples')

"""Change the catogerical data type into numerical data type

# Feature Selection
"""

from sklearn.preprocessing import LabelEncoder
for column in HR.columns:
   if HR[column].dtype == np.number:
    continue 
   HR[column] = LabelEncoder().fit_transform(HR[column])

"""Ensure the changes have been made"""

HR

"""In order to split data accurately its important to move the attrition column to first column"""

HR['Age_Years'] = HR['Age']

HR = HR.drop('Age',axis = 1 )

HR

X = HR.iloc[:,[0] + list(range(2,31))].values
y = HR.iloc[:,1].values
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X_1 = LabelEncoder()
X[:,1] = labelencoder_X_1.fit_transform(X[:,1])
X[:,3] = labelencoder_X_1.fit_transform(X[:,3])
X[:,6] = labelencoder_X_1.fit_transform(X[:,6])
X[:,10] = labelencoder_X_1.fit_transform(X[:,10])
X[:,14] = labelencoder_X_1.fit_transform(X[:,14])
X[:,16] = labelencoder_X_1.fit_transform(X[:,16])
X[:,20] = labelencoder_X_1.fit_transform(X[:,20])
X[:,21] = labelencoder_X_1.fit_transform(X[:,21])
y = labelencoder_X_1.fit_transform(y)

model = RandomForestClassifier()
model.fit(X,y) # Output shown below

list_importances=list(model.feature_importances_)
indices=sorted(range(len(list_importances)), key=lambda k
               :list_importances[k])
feature_selected=[None]*34
k=0
for i in reversed(indices):
    if k<=33:
        feature_selected[k]=i
        k=k+1
X_selected = X[:,feature_selected[:18]]
l_features=feature_selected
i=0
for x in feature_selected:
    l_features[i] = HR.columns[x]
    i=i+1
l_features = np.array(l_features)
#Extracting 17 most important features among 34 features
l_features[:18] #Output shown below

model = RandomForestClassifier()
model.fit(X,y) # Output shown below

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
rfe = RFE(model, 18)
fit = rfe.fit(X, y)
print("Num Features: %s" % (fit.n_features_))
print("Selected Features: %s" % (fit.support_))
print("Feature Ranking: %s" % (fit.ranking_))

"""Selected attributes suggestion : 1)Daily rate  2)Education field 3) Enivornment satisfication
4)Hourly Rate  5)Job invovlement , 6Job role , 7)job  statisfcation  8)Monthly income 9) Monthly rate  10) Perecent salary hike 11)Perfomance rating 12)relationshipsatisfaction 
13)Training time last year 14)yearssincelastpromotion 15)yearsincurrentrole  16)worklifebalance 17) YearswithCur Manager  18)Years at company  19)Stockoptionlevel
"""

HR = HR.drop('Education', axis =1 )

"""# Algorithms

Dropped the following columns :  Education,Employee count ,Over18,EmployeeNumber and StandardHours
"""

X = HR.iloc[:,1:HR.shape[1]].values
Y = HR.iloc[:,0].values

#Split the data into 80% training and 20% testing 

X_train ,X_test,Y_train , Y_test = train_test_split(X,Y , test_size = 0.20 , random_state = 40 )

"""**Using Random forest Classifier**"""

forest = RandomForestClassifier(n_estimators = 10 , criterion = 'entropy', random_state = 0)
forest.fit(X_train, Y_train )

"""**This shows the accuracy of model is 86% **"""

#show the confusion matrix and accuracy score for the model on the test data

from sklearn.metrics import confusion_matrix
import seaborn as sn
cm = confusion_matrix(Y_test,forest.predict(X_test))

TN = cm[0][0]
TP = cm[1][1]
FN = cm[1][0]
FP = cm[0][1]


print(cm)

print('Model Testing Accuracy = {}'.format((TP + TN)/(TP + TN + FN +FP)))

sn.heatmap(cm, annot=True)
plt.show()

predictions=forest.predict(X_test)
print(classification_report(Y_test,predictions))

"""**Using Logistic Regression**"""

X = HR.iloc[:,1:HR.shape[1]].values
Y = HR.iloc[:,0].values
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                   test_size=0.20, random_state= 40)

clf = LogisticRegression(class_weight="balanced")

#Training the Model
clf_trained = clf.fit(X_train, Y_train) #Output shown below

clf_trained.score(X_train,Y_train) # Output shown below

clf_trained.score(X_test,Y_test) # Output shown below

predictions=clf_trained.predict(X_test)
print(classification_report(Y_test,predictions))

from sklearn.metrics import confusion_matrix
import seaborn as sn
cm = confusion_matrix(Y_test,clf_trained.predict(X_test))

TN = cm[0][0]
TP = cm[1][1]
FN = cm[1][0]
FP = cm[0][1]


print(cm)

print('Model Testing Accuracy = {}'.format((TP + TN)/(TP + TN + FN +FP)))

sn.heatmap(cm, annot=True)
plt.show()

"""KNNeighborsClassifier"""

from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split( 
    X, y, test_size = 0.25, random_state = 40)

from sklearn.neighbors import KNeighborsClassifier 
neighbors = [] 
cv_scores = [] 
	
from sklearn.model_selection import cross_val_score 
# perform 10 fold cross validation 
for k in range(1, 40, 2): 
	neighbors.append(k) 
	knn = KNeighborsClassifier(n_neighbors = k) 
	scores = cross_val_score( 
		knn, X_train, y_train, cv = 10, scoring = 'accuracy') 
	cv_scores.append(scores.mean()) 
error_rate = [1-x for x in cv_scores] 
	
# determining the best k 
optimal_k = neighbors[error_rate.index(min(error_rate))] 
print('The optimal number of neighbors is % d ' % optimal_k) 
	
# plot misclassification error versus k 
plt.figure(figsize = (10, 6)) 
plt.plot(range(1, 40, 2), error_rate, color ='green', linestyle ='dashed', marker ='o', 
		markerfacecolor ='purple', markersize = 10) 
plt.xlabel('Number of neighbors') 
plt.ylabel('Misclassification Error') 
plt.show()

from sklearn.model_selection import cross_val_predict, cross_val_score 
from sklearn.metrics import accuracy_score, classification_report 
from sklearn.metrics import confusion_matrix 

def print_score(clf, X_train, y_train, X_test, y_test, train = True): 
	if train: 
		print("Train Result:") 
		print("------------") 
		print("Classification Report: \n {}\n".format(classification_report( 
				y_train, clf.predict(X_train)))) 
		print("Confusion Matrix: \n {}\n".format(confusion_matrix( 
				y_train, clf.predict(X_train)))) 

		res = cross_val_score(clf, X_train, y_train, 
							cv = 10, scoring ='accuracy') 
		print("Average Accuracy: \t {0:.4f}".format(np.mean(res))) 
		print("Accuracy SD: \t\t {0:.4f}".format(np.std(res))) 
		print("accuracy score: {0:.4f}\n".format(accuracy_score( 
				y_train, clf.predict(X_train)))) 
		print("----------------------------------------------------------") 
				
	elif train == False: 
		print("Test Result:") 
		print("-----------") 
		print("Classification Report: \n {}\n".format( 
				classification_report(y_test, clf.predict(X_test)))) 
		print("Confusion Matrix: \n {}\n".format( 
				confusion_matrix(y_test, clf.predict(X_test)))) 
		print("accuracy score: {0:.4f}\n".format( 
				accuracy_score(y_test, clf.predict(X_test)))) 
		print("-----------------------------------------------------------") 
		
knn = KNeighborsClassifier(n_neighbors = 7) 
knn.fit(X_train, y_train) 
print_score(knn, X_train, y_train, X_test, y_test, train = True) 
print_score(knn, X_train, y_train, X_test, y_test, train = False)

"""# Conclusion

Spliting the data for testing
"""

X = HR.iloc[:,1:HR.shape[1]].values
Y = HR.iloc[:,0].values
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, 
                                   test_size=0.20, random_state= 40)

"""As the dataset imbalance in order to get higher accurate SMOTE is used"""

oversampler=SMOTE(random_state=42)
x_train_smote,  y_train_smote = oversampler.fit_sample(X_train,Y_train)

def compare(model):
    clf=model
    clf.fit(x_train_smote,y_train_smote)
    pred=clf.predict(X_test)
    
    # Calculating various metrics
    
    acc.append(accuracy_score(pred,Y_test))
    prec.append(precision_score(pred,Y_test))
    rec.append(recall_score(pred,Y_test))
    auroc.append(roc_auc_score(pred,Y_test))

"""Comparing models to see which perform well."""

acc=[]
prec=[]
rec=[]
auroc=[]
models=[SVC(kernel='rbf'),RandomForestClassifier(),GradientBoostingClassifier(),AdaBoostClassifier(),KNeighborsClassifier(),GaussianProcessClassifier(), MLPClassifier(),QuadraticDiscriminantAnalysis(),XGBClassifier()
]
model_names=['rbfSVM','RandomForestClassifier','GradientBoostingClassifier','AdaBoostClassifier','KNeighborsClassifier','GaussianProcessClassifier', 'MLPClassifier','QuadraticDiscriminantAnalysis','XGBClassifier']

for model in range(len(models)):
    compare(models[model])
    
d={'Modelling Algo':model_names,'Accuracy':acc,'Precision':prec,'Recall':rec,'Area Under ROC Curve':auroc}
met_df=pd.DataFrame(d)
met_df

def comp_models(met_df,metric):
    sns.set_palette("cool")   
    sns.factorplot(data=met_df,x=metric,y='Modelling Algo',size=5,aspect=2,kind='bar')
    sns.factorplot(data=met_df,y=metric,x='Modelling Algo',size=10,aspect=2,kind='point')

comp_models(met_df,'Accuracy')

comp_models(met_df,'Precision')

comp_models(met_df,'Recall')

comp_models(met_df,'Area Under ROC Curve')