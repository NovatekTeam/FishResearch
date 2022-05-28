from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import os
import numpy as np
import pandas as pd
from prepare_data import get_data
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

eps=1.8
catch_path=os.path.join('..','dataset','db1','catch.csv')
ext_path=os.path.join('..','dataset','db2','Ext.csv')
ext2_path=os.path.join('..','dataset','db2','Ext2.csv')

db1, db2 = get_data(catch_path,ext_path,ext2_path)
db2['id_fish']=db2['id_fish_x']

df_regime_dummies = pd.get_dummies(db1['id_regime'])
df_regime_dummies.columns = ['regime%s'%col for col in df_regime_dummies.columns]

df_region_dummies = pd.get_dummies(db1['id_region'])
df_region_dummies.columns = ['regime%s'%col for col in df_region_dummies.columns]

db1 = db1.drop(columns=['id_regime','id_region'])
db1 = pd.concat([db1,df_regime_dummies,df_region_dummies],axis=1)

db2['hour_vsd']=db2['date_vsd_x'].astype('datetime64[ns]').dt.hour
prods = pd.DataFrame({'hour':range(1, 25)})

b = [0,4,8,12,16,20,24]
l = ['Late Night', 'Early Morning','Morning','Noon','Eve','Night']
db2['date_session'] = pd.cut(db2['hour_vsd'], bins=b, labels=l, include_lowest=True)
session_dummies = pd.get_dummies(db2['date_session'])
df_db2=pd.concat([db2.drop(columns=['date_session']),session_dummies],axis=1)

groups = ['id_own','id_ves','id_fish', 'id_Plat']

df_group_1_regime_sum = db1[df_regime_dummies.columns]
df_group_1_region_sum = db1[df_region_dummies.columns]

for group_by in groups:
    df_group_2 = df_db2.groupby(group_by).agg({
        'id_own':['count', pd.Series.nunique],
        'id_ves': pd.Series.nunique,
        'id_fish': pd.Series.nunique,
        'id_Plat': pd.Series.nunique,
        'fish_x': pd.Series.nunique,
        'volume_x': ['mean','min','max','sum'],
        'Late Night': 'sum', 
        'Early Morning': 'sum', 
        'Morning': 'sum', 
        'Noon': 'sum', 
        'Eve': 'sum',
        'Night': 'sum'
    })

    df_group_2.drop(columns=(group_by, 'nunique'),inplace=True)
    df_group_2.columns = ['_'.join(col).strip() for col in df_group_2.columns.values]

    if(group_by!='id_Plat'):
        df_group_1_sum=pd.concat([db1[group_by],df_group_1_regime_sum,df_group_1_region_sum], axis=1).groupby(group_by).sum()
        df_group_1 = db1.groupby(group_by).agg({
            'id_own':['count', pd.Series.nunique],
            'id_ves': pd.Series.nunique,
            'id_fish': pd.Series.nunique,
            'catch_volume': ['mean','min','max','sum']
        })
        df_group_1.drop(columns=(group_by, 'nunique'),inplace=True)
        df_group_1=pd.concat([df_group_1,df_group_1_sum], axis=1)

        df_group = pd.merge(df_group_1,df_group_2,how='outer',left_index=True, right_index=True)

        df_group_db2_only = df_group[df_group['regime0'].isna()]
        df_group_db1_only = df_group[df_group['volume_x_sum'].isna()]
        df_group_1 = df_group_db1_only[df_group_1.columns]
        df_group_2 = df_group_db2_only[df_group_2.columns]
        df_group_all = df_group.drop(df_group_1.index).drop(df_group_2.index)
        df_groups=[df_group_1,df_group_2,df_group_all]
    else:
        df_group=df_group_2
        df_groups=[df_group]

    for df in df_groups:
        scaler = StandardScaler()
        X_scale = scaler.fit_transform(df.values)
        pca = PCA (n_components=3)
        X_reduced = pca.fit_transform(X_scale)
        pred = DBSCAN(eps=1.8, min_samples=3).fit_predict(X_reduced)
        values, counts = np.unique(pred, return_counts=True)
        most = values[np.argmax(counts)]
        df['anomaly']=[1 if each else 0 for each in pred!=most]
        df_group.loc[df.index,'anomaly']=df['anomaly']
    
    output_path = os.path.join('..','output','%s.csv'%group_by)
    df_group.to_csv(output_path)
