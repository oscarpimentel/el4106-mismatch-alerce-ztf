from __future__ import print_function
from __future__ import division
from . import C_

import numpy as np
import pandas as pd

###################################################################################################################################################

def get_object_features(features_ddf, labels_ddf, obj_name,
	band=None,
	bands=['1','2'],
	):
	df = features_ddf.loc[obj_name].compute() # FAST
	if band is None: # get all
		pass
	elif band>=0: # get band-wise features
		df = df[[c for c in df.columns if c[-2:]==f'_{band}']]
	else: # get non-band-wise features
		bands_ = [f'_{b}' for b in bands]
		df = df[[c for c in df.columns if not c[-2:] in bands_]]

	features = df.values[0]
	features_names = df.columns
	try:
		c = labels_ddf.loc[obj_name].compute()['classALeRCE'].values[0] # FAST
	except IndexError:
		c = None
	return features, c, features_names