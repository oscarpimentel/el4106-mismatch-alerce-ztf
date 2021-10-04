from __future__ import print_function
from __future__ import division
from . import _C

import numpy as np
import pandas as pd
from dask import dataframe as dd

N_DASK = _C.N_DASK

###################################################################################################################################################

def isin_filter_df(df, index, objs,
	inverse=False,
	):
	df = df.reset_index()
	df = df[~df[index].isin(objs) if inverse else df[index].isin(objs)]
	df = df.set_index(index)
	return df

def get_train_test_split(df, labels_df, index):
	train_objs = list(set(labels_df.index.values))
	train_df = isin_filter_df(df, index, train_objs)
	test_df = isin_filter_df(df, index, train_objs, inverse=True)
	return train_df, test_df

def filter_by_valid_objs(df, valid_objs):
	return df[df.index.isin(valid_objs)]

def keep_only_valid_objs(df, valid_objs):
	return df[df.index.isin(valid_objs)]
	
def drop_duplicates(df,
	npartitions=N_DASK,
	):
	ddf = dd.from_pandas(df, npartitions=npartitions)
	return ddf.drop_duplicates().compute() # FAST
	
###################################################################################################################################################

def process_df_detections(df, index_name, new_index_name):
	assert df.index.name==index_name
	df.index.rename(new_index_name, inplace=True) # rename index
	df = df.reset_index()
	df = drop_duplicates(df)
	df = df.set_index([new_index_name])
	objs = list(set(df.index))
	return df, objs

def process_df_labels(df, new_index_name, det_objs):
	df = drop_duplicates(df)
	df = df.set_index([new_index_name])
	df = filter_by_valid_objs(df, det_objs) # clean labels dataframe
	objs = list(set(df.index))
	return df, objs