"""
utilities for training logistic regression models on MitoCheck single-cell dataset
"""

import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from typing import List 

# set numpy seed to make random operations reproduceable
np.random.seed(0)


def get_dataset(
    features_dataframe: pd.DataFrame, data_split_indexes: pd.DataFrame, label: str
) -> pd.DataFrame:
    """get testing data from features dataframe and the data split indexes
    Args:
        features_dataframe (pd.DataFrame): dataframe with all features data
        data_split_indexes (pd.DataFrame): dataframe with split indexes
        label (str): label to get data for (train, test, holdout)
    Returns:
        pd.DataFrame: _description_
    """
    indexes = data_split_indexes.loc[data_split_indexes["label"] == label]
    indexes = indexes["labeled_data_index"]
    data = features_dataframe.loc[indexes]

    return data


def get_X_y_data(
    labeled_data: pd.DataFrame,
    feature_type: str,
):
    """generate X (features) and y (labels) dataframes from training data
    Args:
        labeled_data (pd.DataFrame):
            training dataframe
        feature_type : str
            which dataset columns to get feature data for
            can be one of ["CP", "DP", "CP_and_DP", "CP_zernike_only", "CP_areashape_only"]
    Returns:
        pd.DataFrame, pd.DataFrame: X, y dataframes
    """
    all_cols = labeled_data.columns.tolist()

    # get DP,CP, or both features from all columns depending on desired dataset
    if feature_type == "CP_and_DP":
        feature_cols = [col for col in all_cols if "P__" in col]
    elif feature_type == "DP":
        feature_cols = [col for col in all_cols if "DP__" in col]
    else:
        feature_cols = [col for col in all_cols if "CP__" in col]
        if "zernike_only" in feature_type:
            feature_cols = [col for col in feature_cols if "Zernike" in col]
        if "areashape_only" in feature_type:
            feature_cols = [col for col in feature_cols if "AreaShape" in col]

    # extract features
    X = labeled_data.loc[:, feature_cols].values

    # extract phenotypic class label
    y = labeled_data.loc[:, ["Mitocheck_Phenotypic_Class"]].values
    # make Y data
    y = np.ravel(y)

    # shuffle data because as it comes from MitoCheck same labels tend to be in grou
    X, y = shuffle(X, y, random_state=0)

    return X, y
