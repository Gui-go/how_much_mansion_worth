#!/usr/bin/env python3

"""
Class for the Random Forest model on São José real estate data - Predicting house pricing
"""

import numpy as np
import pandas as pd 
import logging

LOG_FORMAT = "%(asctime)-24s [%(filename)s:%(lineno)d] %(levelname)-6s %(message)s"
logging.basicConfig(filename='logs/util_logs.log',
                    filemode='a',
                    format=LOG_FORMAT,
                    level=logging.DEBUG)


class ClassTransform:
    """
    Class to treat Viva Real real estate data
    """
    def __init__(self, deflator):
        self.df = pd.read_csv('data/brasilia_mansions.csv', index_col=0)
        self.deflator = deflator
        # logging.info('data to be treated loaded')
    
    def view_data(self):
        print(self.df)
        logging.info(self.df)

    def describe(self):
        print(self.df.describe(include="all"))
        logging.info(self.df.describe(include="all"))

    def transform(self):
        self.df = self.df[['price', 'area', 'bedrooms', 'bathrooms', 'garages']]
        self.df = self.df.loc[self.df['price'] != 'partir']
        self.df.bathrooms = self.df.bathrooms.astype('str').replace({"--": "0"})
        self.df.bathrooms = self.df.bathrooms.astype('str').replace({"1-2": "1.5"})
        self.df.bathrooms = self.df.bathrooms.astype('str').replace({"2-3": "2.5"})
        self.df.garages = self.df.garages.astype('str').replace({"--": "0"})
        self.df.garages = self.df.garages.astype('str').replace({"1-2": "1.5"})
        self.df.garages = self.df.garages.astype('str').replace({"2-3": "2.5"})
        self.df = self.df.apply(pd.to_numeric)
        logging.info('Data transformed')

    def deflate(self):
        self.df['price'] = self.df['price'] / self.deflator
        logging.info(f"Price deflated by {self.deflator}")

    def save(self):
        self.df.to_csv("data/brasilia_mansions_treated.csv")
        logging.info('Treated data saved at data/brasilia_mansions_treated.csv')
    
    def run(self):
        self.transform()
        self.deflate()
        self.save()
        logging.info('ClassTreat.run() completed')


