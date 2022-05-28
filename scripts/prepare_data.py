import pandas as pd

def get_data(catch_path, ext_path, ext2_path):
    df_catch = pd.read_csv(catch_path)
    df_ext = pd.read_csv(ext_path)
    df_ext2 = pd.read_csv(ext2_path)

    print('Prepare df_catch')
    df_db1 = df_catch.drop(columns='permit')

    print('Prepare df_ext')
    df_ext.drop(columns=['numPart'], inplace=True)
    df_ext_descr = df_ext[(df_ext['Name_Plat'] != '\\N') | (df_ext['Product_period'] != '\\N') | (df_ext['Region_Plat'] != '\\N')]
    df_ext_wo_data=df_ext.drop(df_ext_descr.index)
    df_ext_merged = pd.merge(
        pd.DataFrame(df_ext['id_vsd'].unique(), columns=['id_vsd']),
        df_ext_wo_data[['id_vsd','id_own','id_ves','date_fishery','id_Plat']],
        on='id_vsd',
        how="left"
    )
    df_ext_merged = pd.merge(
        df_ext_merged,
        df_ext_descr[['id_vsd','date_fishery']],
        on='id_vsd',
        how="left"
    )
    df_ext_merged.loc[~df_ext_merged['date_fishery_y'].isna(),'date_fishery_x']=df_ext_merged['date_fishery_y']
    df_ext_merged.drop(columns='date_fishery_y',inplace=True)

    print('Prepare df_ext2')
    df_ext2_w_fish_id = df_ext2[df_ext2['id_fish']!=-1]
    df_ext2_wo_fish_id = df_ext2.drop(df_ext2_w_fish_id.index)
    df_ext2_merged = pd.merge(
        pd.DataFrame(df_ext2['id_vsd'].unique(), columns=['id_vsd']),
        df_ext2_w_fish_id[['id_vsd','id_fish','fish','volume','unit','date_vsd']],
        on='id_vsd',
        how="left"
    )
    df_ext2_merged = pd.merge(
        df_ext2_merged,
        df_ext2_wo_fish_id[['id_vsd','fish','date_vsd','volume','unit']],
        on='id_vsd',
        how="left"
    )
    len(df_ext2_merged)

    if_fish_na = df_ext2_merged['id_fish'].isna()
    df_ext2_merged.loc[if_fish_na,'fish_x']=df_ext2_merged['fish_y']
    df_ext2_merged.loc[if_fish_na,'volume_x']=df_ext2_merged['volume_y']
    df_ext2_merged.loc[if_fish_na,'unit_x']=df_ext2_merged['unit_y']
    df_ext2_merged.loc[if_fish_na,'date_vsd_x']=df_ext2_merged['date_vsd_y']
    df_ext2_merged=df_ext2_merged.drop(columns=['fish_y','volume_y','unit_y','date_vsd_y'])
    df_ext2_merged.loc[df_ext2_merged['unit_x']=='\\N','volume_x']/=1000
    df_ext2_merged.loc[df_ext2_merged['unit_x']=='кг','volume_x']/=1000
    fish_class = df_ext2_merged[df_ext2_merged['id_fish']>=0][['id_fish','fish_x']].drop_duplicates()
    df_ext2_merged=pd.merge(
        df_ext2_merged,
        fish_class,
        on='fish_x',
        how='left'
    )
    df_ext2_merged.loc[df_ext2_merged['id_fish_x'].isna(),'id_fish_x']=df_ext2_merged['id_fish_y']
    df_ext2_merged.drop(columns=['id_fish_y','unit_x'], inplace=True)
    df_db2 = pd.merge(df_ext_merged,df_ext2_merged,on='id_vsd')
    return df_db1, df_db2
