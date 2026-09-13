#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[7]:


#url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet'

#df = pd.read_parquet(url)


# In[9]:


df.head()


# In[10]:


#len(df)


# In[12]:


#df.dtypes


# In[24]:


from sqlalchemy import create_engine


# In[23]:


#!uv add "psycopg[binary,pool]"


# In[28]:


engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')


# In[30]:


#print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[36]:


url='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz'


# In[32]:


df.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[34]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


# In[54]:


df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000,
    nrows = 545000
)


# In[55]:


#!uv add tqdm


# In[56]:


from tqdm.auto import tqdm


# In[57]:


for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[ ]:




