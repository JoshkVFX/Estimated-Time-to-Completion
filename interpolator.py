import numpy as np
from sklearn import preprocessing


def generate_normalised_values(dataFrame):
    dataFrame['normalised_index_value'] = 0
    for nodeType, df in dataFrame.groupby('type'):
        min_max_scaler = preprocessing.MinMaxScaler()
        sorted_values = sorted(range(len(df['values'])), key=lambda k: df['values'].values[k])
        sorted_values = np.array(sorted_values).reshape(-1, 1)
        x_scaled = min_max_scaler.fit_transform(sorted_values)
        dataFrame.loc[dataFrame['type'] == nodeType, 'normalised_index_value'] = x_scaled
    return dataFrame


def generate_relative_normalised_values(nodesDataFrame, scriptsDataFrame):
    for (script_id, nodeType), df in nodesDataFrame.groupby(['script_id', 'type']):
        scriptsDataFrame.at[script_id, nodeType] = sum(df['normalised_index_value'].values)
    return scriptsDataFrame
