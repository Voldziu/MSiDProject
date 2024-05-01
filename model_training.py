import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
import numpy as np
import constants
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def create_df(folder_rank_directory):
    data_list = []
    for file in os.listdir(folder_rank_directory):
        file_path = os.path.join(folder_rank_directory, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
            data_list.append(data)

    df = pd.DataFrame(data_list)
    return df


def all_ranks_list_df(path):

    folder_names = constants.SUMMONERS_TO_CHECK.keys()
    list_of_dfs=[]

    for name in folder_names:
        folder_path = os.path.join(path,name)
        rank_df = create_df(folder_path)
        list_of_dfs.append(rank_df)

    return list_of_dfs


def make_big_df(ldf):

    return pd.concat(ldf)

def get_X_y():
    ldf = all_ranks_list_df("MatchData")
    big_df = make_big_df(ldf)
    return process(big_df)


def process(big_df):
    features_scaler = MinMaxScaler()
    big_df.pop('literal level')
    shuffled_df = big_df.sample(frac=1, random_state=42).reset_index(drop=True)
    shuffled_df.pop('id')
    target_vector = shuffled_df.pop('lvl')
    features_df = shuffled_df
    # Fit and transform the features DataFrame
    features_normalized = features_scaler.fit_transform(features_df)
    return features_normalized , target_vector




def model_training(X_train, X_test, y_train, y_test,regressors:dict):


    for name, regressor in regressors.items():
        regressor.fit(X_train, y_train)  # Training the regressor
        y_pred = regressor.predict(X_test)  # Making predictions
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # Calculating Mean Squared Error
        print(f"{name} Mean Squared Error: {rmse}")


if __name__ == "__main__":
    big_df = make_big_df(all_ranks_list_df("MatchData"))

    X,y = process(big_df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33,
                                                        random_state=42)
    regressors = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(),
        "Random Forest": RandomForestRegressor(),
        "Support Vector Machine": SVR(),
        "K-Nearest Neighbors": KNeighborsRegressor()
    }

    model_training(X_train,X_test,y_train,y_test,regressors)







