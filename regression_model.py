#Import libraries

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#import data
data = pd.read_csv("movie_ml_data.csv")

#train/test split - Full model

X = data.drop(columns=['vote_average', ])
y = data['vote_average']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

reg_full = LinearRegression().fit(X_train, y_train)

#Coefficent of Determination full model
print(reg_full.score(X_test, y_test))

#Based on feature engineering, we select the most important features, dir_max_rating, dir_avg_rating,
#log_vote_count, is_adult, and log_revenue. From this, we will make a smaller model and test the residual squared values against each other

X_train_small_model = X_train[["dir_max_rating", "dir_avg_rating", "log_vote_count", "is_adult", "log_revenue" ]]
X_test_small_model = X_test[["dir_max_rating", "dir_avg_rating", "log_vote_count", "is_adult", "log_revenue" ]]

reg_small = LinearRegression().fit(X_train_small_model, y_train)

#Coefficent of Determination Small Model
print(reg_small.score(X_test_small_model, y_test))

#The coefficent for the small model is 0.86 when compared to 0.9 from the large model. The decrease in
# the two indicates that the small model can explain 0.04% less of the data than the full, however, this is a small decrease
# for a more versatile model and one less susceptible to overfitting that is a worthwhile tradeoff.

#Assuming that the film gets 500000 votes and makes 800M in revenue
nolan_odyssey = pd.DataFrame([{ "dir_max_rating": 9.0,  "dir_avg_rating": 8.1, "log_vote_count": np.log(500000), "is_adult": 0, "log_revenue": np.log(800000000)
}])

predicted_rating = reg_small.predict(nolan_odyssey)
print(predicted_rating)

#Our linear regression model predicts that Nolan's film will earn a 8.79 rating, which is a significant rating for his film.

