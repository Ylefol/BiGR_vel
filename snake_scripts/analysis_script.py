#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 11:02:58 2021

@author: yohanl
"""

#Import required functions
from snake_scripts.snake_functions import snake_utils as my_utils
from snake_scripts.snake_functions import snake_analysis_functions as my_func

#Import libraries
import os
import numpy as np
import pandas as pd
# import scipy.stats as stats
# import matplotlib.pyplot as plt


cell_lines={}
cell_lines['HaCat']='A_B'


cell_line='HaCat'
# cell_line=key
#Find replicates
replicates=os.listdir('data_files/confidence_intervals/'+cell_line)
replicates.remove('merged_results')
#Create layers
layers=['spliced','unspliced']


folder_to_use='A_B'
# folder_to_use=cell_lines[key]

# Load results
mean_dict,CI_dict,bool_dict,count_dict,boundary_dict=my_utils.get_CI_data (cell_line, layers, folder_to_use)
my_ranked_genes=pd.read_csv('data_files/data_results/rank/'+cell_line+'/'+folder_to_use+'_ranked_genes.csv')
my_delay_df=pd.read_csv('data_files/data_results/delay_genes/'+cell_line+'/'+folder_to_use+'_delay_genes.csv')
my_UTRs=pd.read_csv('data_files/data_results/UTR_length/'+cell_line+'/'+folder_to_use+'_UTR_length.csv')
vlm_dict=my_utils.get_vlm_values(cell_line, layers,folder_to_use )

#Find rankable genes and perform t-test statistic
rankable_genes=list(my_ranked_genes['gene_name'][np.where(np.asanyarray(my_ranked_genes['high_score'])>0)[0]])
t_test_res=pd.read_csv('data_files/data_results/rank/'+cell_line+'/'+folder_to_use+'_t_test_results.csv')

#Identify genes with padjusted < 0.01
#Remove NA from list, identify significant values, then significant genes
res = [i for i in t_test_res.padjusted if i != 'NA']
good_vals=[x for x in res if x<0.01]
significant_genes=list(t_test_res.loc[t_test_res['padjusted'] .isin(good_vals)].index)

if 'UNG'in mean_dict['spliced'].keys():
    gene_save_path='all_figures/'+cell_line+'/analysis_results/'+folder_to_use+'/gene_plots/'
    my_func.plot_layer_smooth_vel('UNG', mean_dict, bool_dict, CI_dict, count_dict,vlm_dict,boundary_dict,cell_line,save_path=gene_save_path+'layer_vel')
    my_func.plot_curve_count('UNG', mean_dict, bool_dict, CI_dict, count_dict,boundary_dict,cell_line,save_path=gene_save_path+'vel_count')

delay_save_path='all_figures/'+cell_line+'/analysis_results/'+folder_to_use+'/gene_delays'
#Plot delay of all genes
my_func.plot_raincloud_delay(my_delay_df,cell_line,save_path=delay_save_path,save_name='delay_all_genes.png')

#Plot delay of rankable genes
my_significant_delays=my_delay_df[my_delay_df["gene_name"].isin(rankable_genes)]
my_func.plot_raincloud_delay(my_significant_delays,cell_line,save_path=delay_save_path,save_name='delay_rankable_genes.png')

#Subset the delay dataframe with significant genes and plot
sub_delay=my_delay_df[my_delay_df['gene_name'] .isin(significant_genes)]
my_func.plot_raincloud_delay(sub_delay,cell_line,save_path=delay_save_path,save_name='delay_001_genes.png')


#Plot REAC results
REAC_save_path='all_figures/'+cell_line+'/analysis_results/'+folder_to_use+'/REAC_rankable'
REAC_dict=my_func.create_REAC_dict(vlm_dict,rankable_genes)
my_func.create_REAC_summary_plots(REAC_dict,boundary_dict,layer='spliced',second_layer='unspliced',plot_path=REAC_save_path)

#Plot REAC results significant genes
REAC_save_path='all_figures/'+cell_line+'/analysis_results/'+folder_to_use+'/REAC_significant'
REAC_dict=my_func.create_REAC_dict(vlm_dict,significant_genes)
my_func.create_REAC_summary_plots(REAC_dict,boundary_dict,layer='spliced',second_layer='unspliced',plot_path=REAC_save_path)

    

#Plot layer/vel and vel/count for all cc genes


# #Print all CC genes
# for phase in list(pd.unique(cc_genes_df['phase'])):
#     for gene in list(cc_genes_df[cc_genes_df['phase']==phase]['gene']):
#         if gene in mean_dict['spliced'].keys():
#             my_func.plot_layer_smooth_vel(gene, mean_dict, bool_dict, CI_dict, count_dict,vlm_dict,boundary_dict,cell_line,save_path='cc_genes/'+cell_line+'/vel/'+phase,single_rep=False)
#             my_func.plot_curve_count(gene, mean_dict, bool_dict, CI_dict, count_dict,boundary_dict,cell_line,save_path='cc_genes/'+cell_line+'/count/'+phase)


