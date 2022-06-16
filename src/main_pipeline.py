#!/usr/bin/env python3

"""
Purpose: Get predictions of mansion prices in Brasilia, DF, Brazil
"""

import os
import logging
import pandas as pd
import json
from src.class_extract import ClassExtract
from src.class_transform import ClassTransform
from src.class_model import ClassModel

LOG_FORMAT = "%(asctime)-24s [%(filename)s:%(lineno)d] %(levelname)-6s %(message)s"
logging.basicConfig(filename='logs/util_logs.log',
                    filemode='a',
                    format=LOG_FORMAT,
                    level=logging.DEBUG)

# Main function
def main(
    input_first_page,
    input_n_pages_run,
    input_deflator_inplicito,
    input_pred_feat,
    input_rf_n_estimators,
    input_rf_random_state
):
    """
    Main function
    """
    print(f"Current directory is: {os.getcwd()}")

    # Extract
    if not os.path.isfile('data/brasilia_mansions.csv'):
        ce = ClassExtract(input_first_page)
        ce.run(input_n_pages_run)

    # Transform
    ct = ClassTransform(deflator=input_deflator_inplicito)
    ct.run()

    # Model
    cm = ClassModel(rf_n_estimators=input_rf_n_estimators, rf_random_state=input_rf_random_state)
    cm.run()
    cm.make_prediction(input_pred_feat)
    logging.info(f"Mansion with estimated price of {cm.prediction_txt}")

    return cm.prediction


# Parameters
with open("conf/util_parameters.json", 'r') as f:
    parameters = json.load(f)
parameters.keys()
pred_feat = [parameters["pred_feat_area"], parameters["pred_feat_bedrooms"],
             parameters["pred_feat_bathrooms"], parameters["pred_feat_garages"]]

main(
    input_n_pages_run=parameters["n_pages_run"],
    input_deflator_inplicito=parameters["deflator_inplicito"],
    input_pred_feat=pred_feat,
    input_first_page=parameters["first_page"],
    input_rf_n_estimators=parameters["rf_n_estimators"],
    input_rf_random_state=parameters["rf_random_state"]
)


# if __name__ == '__main__':
#     main()
