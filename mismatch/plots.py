from __future__ import print_function
from __future__ import division
from . import _C

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math

PLOT_FIGSIZE = _C.PLOT_FIGSIZE
PLOT_GRID_ALPHA = _C.PLOT_GRID_ALPHA
PLOT_DPI = _C.PLOT_DPI

###################################################################################################################################################

def plot_hist_bins(data_dict:dict,
	bins:int=500,
	linewidth:float=2,
	uses_density:bool=False,
	uses_annotation:bool=True,
	annotation_size:int=9,
	annotation_alpha:float=1,
	histtype:str='step', # step, bar, stepfilled
	return_legend_patches:bool=False,
	lw:float=1.5,
	xrange=None,
	add_bins_title:bool=False,

	fig=None,
	ax=None,
	figsize:tuple=PLOT_FIGSIZE,
	xlabel:str='values',
	ylabel:str='population',
	title:str='plot_hist_bins',
	xlim:tuple=[None, None],
	ylim:tuple=[None, None],
	grid:bool=True,
	grid_alpha:float=PLOT_GRID_ALPHA,
	legend_loc:str='upper right',
	cmap=None,
	alpha:float=0.5,
	verbose:int=0,
	**kwargs):
	if histtype in ['step']:
		alpha=1

	fig, ax = plt.subplots(1,1, figsize=figsize, dpi=PLOT_DPI) if fig is None else (fig, ax)
	if not isinstance(data_dict, dict):
		data_dict = {'distribution':data_dict} # transform in a dummy dict
	keys = list(data_dict.keys())
	cmap = cc.get_default_cmap(len(keys)) if cmap is None else cmap

	legend_patches = []
	for k,key in enumerate(keys):
		x = np.array(data_dict[key].copy())
		if verbose>0:
			x_samples, x_mean, x_std, x_min, x_max = len(x), np.mean(x), np.std(x), np.min(x), np.max(x)
			print(f'key={key}; N={x_samples:,}; x_mean={x_mean:.5f}; x_std={x_std:.5f}; x_min={x_min:.5f}; x_max={x_max:.5f}')

		c = cmap.colors[k]
		hist_kwargs = {
			'density':uses_density,
			'color':c,
			'label':None,
			'alpha':alpha,
			'histtype':histtype,
			'range':xrange,
			'linewidth':linewidth,
		}
		n, new_bins, patches = ax.hist(x, bins, **hist_kwargs)

		p5 = np.percentile(x, 5)
		p50 = np.percentile(x, 50)
		p95 = np.percentile(x, 95)
		#label = f'{key}'+', $N='+f'{len(x):,}'+'$'+', $p_{50}='+f'{p50:.2f}'+'_{-'+f'{p50-p5:.2f}'+'}^{+'+f'{p95-p50:.2f}'+'}$'
		label = f'{key}'+'; $N='+f'{len(x):,}'+'$'+'; $p_{50}='+f'{p50:.2f}'+'_{-'+f'{p50-p5:.2f}'+'}^{+'+f'{p95-p50:.2f}'+'}$'
		#label = f'{key}'+'; $N='+f'{len(x):,}'+'$'+'; $p50_{p5-p50}^{p95-p50}='+f'{p50:.2f}'+'_{-'+f'{p50-p5:.2f}'+'}^{+'+f'{p95-p50:.2f}'+'}$'
		legend_patches.append(mpatches.Patch(color=c, label=label))

	ax.set_xlabel(xlabel)
	ax.set_ylabel('density' if uses_density and not ylabel is None else ylabel)
	bins_text = f' (bins={bins:,})' if add_bins_title else ''
	ax.set_title(f'{title}{bins_text}')
	ax.set_xlim(xlim)
	ax.set_ylim(ylim)
	ax.legend(handles=legend_patches, loc=legend_loc, fontsize=12)

	if grid:
		xax = ax.set_axisbelow(True); ax.xaxis.grid(True, alpha=grid_alpha)
		yax = ax.set_axisbelow(True); ax.yaxis.grid(True, alpha=grid_alpha)

	if uses_annotation:
		magic_offset = 0.15
		max_ylim = ax.get_ylim()[1]
		new_max_ylim = max_ylim*(1+(len(keys))*magic_offset)
		ax.set_ylim([ax.get_ylim()[0], new_max_ylim])

		for k,key in enumerate(keys):
			x = np.array(data_dict[key].copy())
			c = cmap.colors[k]
			p50 = np.median(x)
			ann_y = new_max_ylim*0.9; (k+1)*new_max_ylim*0.1
			#ann = ax.annotate(f'{ann_x:.4f}', xy=(ann_x, ann_y), xytext=(0, annotation_size), fontsize=5, ha='center',
			#		textcoords='offset points',
			#		size=annotation_size, va='center', color='w',
			#		bbox=dict(boxstyle='round', fc=c, ec='none', alpha=annotation_alpha),
			#		#arrowprops=dict(arrowstyle='wedge,tail_width=1.0', fc=c, ec='none', patchA=None, patchB=None, relpos=(0.5, 0.2), alpha=annotation_alpha),
			#		)
			ax.axvline(x=p5, ls='--', c=c, label=None, lw=lw)
			ax.axvline(x=p50, ls='-', c=c, label=None, lw=lw)
			ax.axvline(x=p95, ls='--', c=c, label=None, lw=lw)

	if return_legend_patches:
		return fig, ax, legend_patches
	return fig, ax