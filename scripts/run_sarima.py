import numpy as np
import pandas as pd
import os
from sklearn.metrics import mean_absolute_error
from prepare_data import get_data


def anomalies_bonds(series, window=4, scale=1.96):

    result = pd.DataFrame()
    rolling_mean = series.rolling(window=window).mean()
    result['predict_volume'] = rolling_mean
    mae = mean_absolute_error(series[window:], rolling_mean[window:])
    deviation = np.std(series[window:] - rolling_mean[window:])
    lower_bond = rolling_mean - (mae + scale * deviation)
    upper_bond = rolling_mean + (mae + scale * deviation)
    result['lower_bond'] = lower_bond
    result['upper_bond'] = upper_bond
    anomalies = pd.DataFrame(index=series.index, columns=series.columns)
    anomalies[series < lower_bond] = series[series < lower_bond]
    anomalies[series > upper_bond] = series[series > upper_bond]
    result['anomalies'] = anomalies

    return result


def db1_sarima_anomalies_detect(dataframe, table):
    print(f'Prepare catch_{table}_sarima_predict.csv')

    ids = pd.Series(dataframe[f'id_{table}']).unique()
    rate = pd.DataFrame()
    for id in ids:
        aggr_df = dataframe.loc[dataframe[f'id_{table}']==id].groupby("date")[["catch_volume"]].sum()
        if aggr_df.size > 20:
            anomalies = anomalies_bonds(aggr_df)    
            aggr_df[f'id_{table}'] = id
            aggr_df = pd.concat([aggr_df, anomalies], axis=1)
            aggr_df = aggr_df.reset_index()
            rate = pd.concat([rate, aggr_df], axis=0)

    rate.loc[(rate.anomalies > 0), 'anomalies']  = 1
    rate.loc[(rate.anomalies.isna()), 'anomalies']  = 0

    output_path = os.path.join('..','output',f'catch_{table}_sarima_predict.csv')
    rate.to_csv(output_path)



def db2_sarima_anomalies_detect(dataframe, table):
    print(f'Prepare ext_{table}_sarima_predict.csv')
    
    ids = pd.Series(dataframe[f'id_{table}']).unique()
    rate = pd.DataFrame()
    for id in ids:
        aggr_df = dataframe.loc[dataframe[f'id_{table}']==id].groupby("date_fishery_x")[["volume_x"]].sum()
        if aggr_df.size > 20:
            anomalies = anomalies_bonds(aggr_df)    
            aggr_df[f'id_{table}'] = id
            aggr_df = pd.concat([aggr_df, anomalies], axis=1)
            aggr_df = aggr_df.reset_index()
            rate = pd.concat([rate, aggr_df], axis=0)

    rate.loc[(rate.anomalies > 0), 'anomalies']  = 1
    rate.loc[(rate.anomalies.isna()), 'anomalies']  = 0

    output_path = os.path.join('..','output',f'catch_{table}_sarima_predict.csv')
    rate.to_csv(output_path)


################################################################################################################

catch=os.path.join('..','dataset','db1','catch.csv')
ext1=os.path.join('..','dataset','db2','Ext.csv')
ext2=os.path.join('..','dataset','db2','Ext2.csv')

df_catch, df_ext = get_data(catch_path=catch, ext_path=ext1, ext2_path=ext2)

catch_table = ('ves', 'own', 'fish')
ext_table = ('ves', 'own', 'fish_x', 'Plat')

for table in catch_table:
    db1_sarima_anomalies_detect(df_catch, table)

for table in ext_table:
    db2_sarima_anomalies_detect(df_ext, table) 