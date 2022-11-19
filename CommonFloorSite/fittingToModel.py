import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sklearn
sns.set() # for plot styling (seaborn) 
from termcolor import colored as cl # text customization

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression # OLS algorithm
from sklearn.linear_model import Ridge # Ridge algorithm
from sklearn.linear_model import Lasso # Lasso algorithm
from sklearn.linear_model import BayesianRidge # Bayesian algorithm
from sklearn.linear_model import ElasticNet # ElasticNet algorithm
from sklearn.metrics import explained_variance_score as evs # evaluation metric
from sklearn.metrics import r2_score as r2 # evaluation metric

#Notes

# Furnishing - 
    # 1- Not Furnished or Unfurnished 
    # 2 - Semi Furnished
    # 3 - Fully Furnished
    
def mae(y_true, predictions):
    y_true, predictions = np.array(y_true), np.array(predictions)
    return np.mean(np.abs(y_true - predictions))

#---------------------------Read CSV with pandas----------------------------
df = pd.read_csv(r'C:\Users\nipriya\Desktop\ML\project\Hyd_Housing\commonFloor\New\common_floor_cleanData.csv')

# cols = ['Bedrooms', 'Bathrooms', 'Furnishing', 'Area', 'Price','Locality', 'Parking', 'Power' , 'Pool', 'Security']
# print(df.head())

# TRAINING DATA 

labels = df['Price']
train1 = df.drop(['Locality', 'Price' , 'Parking', 'Power' , 'Pool', 'Security' ] , axis=1)
X_train , X_test, y_train, y_test = train_test_split(train1 , labels , test_size=0.2, random_state=10)
print(train1.head())


param_grid =  {'n_estimators':[200, 300, 400, 500, 600],
               'max_features':[0.1, 0.3,0.6,0.5]
              }

# Initialise the random forest model 
RandForest = RandomForestRegressor(n_jobs= -1, random_state = 0, bootstrap=True)

# Initialise Gridsearch CV with 5 fold corssvalidation and neggative root_mean_squared_error
Tuned_RandForest = GridSearchCV(estimator=RandForest, param_grid=param_grid, scoring='neg_root_mean_squared_error', cv=30) #initial 5 variance .35 , 10 -> 0.39, 30 -> 0.438

# Fit model & Time the process for training the model
#start_time = time.process_time()
Tuned_RandForest.fit(X_train, y_train)
# End of fit time
#print(time.process_time() - start_time, "Seconds")

# Record the results for all models in a pandas dataframe and keep only the best model
Results = pd.DataFrame(Tuned_RandForest.cv_results_)
Results_Best = Results.loc[Results.rank_test_score==1]
    
print('Random Forest Regressor')
Results = Results.loc[Results.rank_test_score==1]
tuned_yhat=Tuned_RandForest.predict(X_test)
print(cl('Explained Variance Score of RandForest model is {}'.format(evs(y_test, tuned_yhat))))
#single_house = train1.drop('Price',axis=1).iloc[0]
print(mae(y_test,tuned_yhat))


# MODELING

# 1. Ordinary least squares Linear Regression
ols = LinearRegression()
ols.fit(X_train, y_train)
ols_yhat = ols.predict(X_test)

# 2. Ridge
ridge = Ridge(alpha = 0.5)
ridge.fit(X_train, y_train)
ridge_yhat = ridge.predict(X_test)

# 3. Lasso
lasso = Lasso(alpha = 0.01)
lasso.fit(X_train, y_train)
lasso_yhat = lasso.predict(X_test)

# 4. Bayesian
bayesian = BayesianRidge()
bayesian.fit(X_train, y_train)
bayesian_yhat = bayesian.predict(X_test)

# 5. ElasticNet
en = ElasticNet(alpha = 0.01)
en.fit(X_train, y_train)
en_yhat = en.predict(X_test)

# EVALUATION

# 1. Explained Variance Score
print(cl('EXPLAINED VARIANCE SCORE:'))
print('-------------------------------------------------------------------------------')
print(cl('Explained Variance Score of OLS model is {}'.format(evs(y_test, ols_yhat))))
print('-------------------------------------------------------------------------------')
print(cl('Explained Variance Score of Ridge model is {}'.format(evs(y_test, ridge_yhat))))
print('-------------------------------------------------------------------------------')
print(cl('Explained Variance Score of Lasso model is {}'.format(evs(y_test, lasso_yhat))))
print('-------------------------------------------------------------------------------')
print(cl('Explained Variance Score of Bayesian model is {}'.format(evs(y_test, bayesian_yhat))))
print('-------------------------------------------------------------------------------')
print(cl('Explained Variance Score of ElasticNet is {}'.format(evs(y_test, en_yhat))))
print('-------------------------------------------------------------------------------')

# 2. R-squared
print(cl('R-SQUARED:'))
print('-------------------------------------------------------------------------------')
print(cl('R-Squared of OLS model is {}'.format(r2(y_test, ols_yhat))))
print('-------------------------------------------------------------------------------')
print(cl('R-Squared of Ridge model is {}'.format(r2(y_test, ridge_yhat))))
print('-------------------------------------------------------------------------------')
print(cl('R-Squared of Lasso model is {}'.format(r2(y_test, lasso_yhat))))
print('-------------------------------------------------------------------------------')
print(cl('R-Squared of Bayesian model is {}'.format(r2(y_test, bayesian_yhat))))
print('-------------------------------------------------------------------------------')
print(cl('R-Squared of ElasticNet is {}'.format(r2(y_test, en_yhat))))
print('-------------------------------------------------------------------------------')