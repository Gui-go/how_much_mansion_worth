#!/usr/bin/env python3

"""
Class to model Brasilia real estate data and predict mansion price
"""

import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import logging

LOG_FORMAT = "%(asctime)-24s [%(filename)s:%(lineno)d] %(levelname)-6s %(message)s"
logging.basicConfig(filename='logs/util_logs.log',
                    filemode='a',
                    format=LOG_FORMAT,
                    level=logging.DEBUG)


class ClassModel:
    """
    Class to model Viva Real real estate data and predict mansion price
    """
    def __init__(self, rf_n_estimators, rf_random_state):
        self.df = pd.read_csv('data/brasilia_mansions_treated.csv', index_col=0)
        self.rf_n_estimators = rf_n_estimators
        self.rf_random_state = rf_random_state
        # logging.info('data to be treated loaded')
    
    def view_data(self):
        print(self.df)
        logging.info(self.df)

    def set_label(self):
        self.labels = np.array(self.df.price)
        logging.info('label set')

    def set_feature(self):
        self.features = np.array(self.df[['area', 'bedrooms', 'bathrooms', 'garages']])
        logging.info('features set')

    def fit_model(self):
        self.rf = RandomForestRegressor(n_estimators = self.rf_n_estimators, random_state = self.rf_random_state)
        self.rf.fit(self.features, self.labels)
        self.r2 = self.rf.score(self.features, self.labels)
        logging.info(f'Model scored {self.r2} R2')

    def make_prediction(self, pred_feat):
        self.prediction = self.rf.predict(np.array([pred_feat]))[0].astype(int)
        self.prediction_txt = f'{self.prediction} reais'
        logging.info(f'For parameters {pred_feat}, model predicted {self.prediction} reais for this home')

    def make_pickle(self):
        joblib.dump(self.rf, 'data/rf_model.pkl')

    def run(self):
        """
        run() method applies methods in an orderlly manner
        """
        self.set_label()
        self.set_feature()
        self.fit_model()
        logging.info('ClassModel.run() completed')

