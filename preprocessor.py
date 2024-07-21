import pandas as pd



def preprocess(df,region_df):
    
    #filtering for summer olympics
    df=df[df["Season"]=="Summer"]
    #merge with region df
    df=df.merge(region_df,on="NOC",how="left")
    #drop duplicates
    df.drop_duplicates(inplace=True)
    #One-hot encodding medals
    df=pd.concat([df,pd.get_dummies(df['Medal']).replace([False,True],[0,1])],axis=1)
    
    return df