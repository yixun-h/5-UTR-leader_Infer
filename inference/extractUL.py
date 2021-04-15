#!/Users/apple/anaconda3/bin/python3
#!/usr/bin/env python3
'''
Title: extractUL.py
Author:Yixun Huang & Linnea Thörnqvist
Description:
    This script is a key step of 5'UTR-leader sequences inference. It achieved by filter.sh.
    It input the reads of one allele after filtering.The output is the inferred 5'UTR-leader sequences, and the plots if sequence logo and the frequency counting of the most popular nucleotide in each position
    The strategy of extracting UTR-leader seqs is as follows:
    1.	Read the sequences, flip them over and store them in a data frame (so that the 3' most base ends up in column 1, the second 3' most base ends up in column 2, an so on).
    2.	Identify the columns where less than 50% of the rows contain data. Any data 5' of this should not be used. (calculate the percentage of missing value for each colunm. clip this columns away)
    3.	Loop over the columns (stopping at the column identified in 2.), and check which nucleotide/nucleotides that are present in more than 30% of all rows. Missing data (that will occur in the 5' end of the sequences) should probably not be considered here, but the nucleotide should found in >30% of the rows where there actually is data. 
    	For most of easy cases, there will only be one nucleotide that is found in >30% for each position.
    	In the more difficult cases, there will be two different sequences that both are rather common. If they differ in more than one position. The solution would be to stop the loop whenever such a position is found and then divide the data frame into two data frames (based on the nucleotide found at this position). Then the analysis (step 2 and 3) can be re-performed on each of these data frames separately.   
Usage:
    python ../extractUL.py IGHV1-18\*01.txt IGHV1-18\*01_out IGHV1-18\*01 seqlogo_IGHV1-18\*01
'''

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Bio.Seq import Seq
from Bio import motifs, Alphabet
from Bio.Alphabet import IUPAC
if len(sys.argv) < 4:
    print("Error: too few arguments!")
    print("Usage: ./plot.py input_data_filename output_filename most_frequent_plot_filename seqlogo_filename")
    exit()
with open (sys.argv[1],'r') as fin, open('filpped.txt','w') as fout:
    print('seq', file=fout)
    for line in fin:
        columns=line.split('\t')
        print(columns[1][::-1].strip(), file=fout) #filpping seq over
final_out= open(sys.argv[2],'w')
plot_filename=sys.argv[3]
logo_name=sys.argv[4]
df = pd.read_csv('filpped.txt') #read flipping seq
seq_df = pd.DataFrame(df.seq.apply(list).tolist()) #store seq into a dataframe
#calculate the percentage of missing value for each colunm
consensus_sequence = ""
# Create an empty string where the consensus sequence can be saved
df_list = [seq_df] # I need the df to be in a list, in order to handle upcoming cases where I should loop over more than one list
not_done = True
restart = False
while not_done:
    consensus_sequence = [] # a list to be able to save MULTIPLE consensus sequences
    # Loop over all dataframes in the list
    for i in range(len(df_list)):
        consensus_sequence.append("")
        percent_missing = df_list[i].isnull().sum() * 100 / len(df_list[i])
        missing_value_df = pd.DataFrame({'column_name': df_list[i].columns, 'percent_missing': percent_missing})
        clip_pos_df= missing_value_df.loc[missing_value_df['percent_missing'] >= 50]
        clip_pos_list=clip_pos_df['column_name'].tolist()
        seq_clip_df=df_list[i].drop(clip_pos_list, axis=1)

        for col in seq_clip_df:
            count_series=seq_clip_df[col].value_counts(normalize=True) * 100
            bases = count_series[count_series > 30].index.tolist()
            if len(bases) == 1:
                consensus_sequence[i] += bases[0]
            else:
                # Split the dataframe into multiple dataframes based on their content in col
                for base in bases:
                    df_list.append(df_list[i][df_list[i][col] == base])
                # Remove the dataframe that we are currently working with, so that we do not run the same analysis again
                del df_list[i]
                restart = True
            if restart: # Break the inner for loop
                break
        if restart: # Break the outer for loop
            break
    if restart: # Restart the while loop
        restart = False
        continue
    else: #  Stop the while loop when we are done
        not_done = False

#plot 'the most frequent nucleotide in each position'

for i in range(len(df_list)):
    rows_list = []
    for col in df_list[i]:
        count=df_list[i][col].value_counts().max()
        indexs=df_list[i][col].value_counts()[:1].index.tolist()
        for index in indexs:
            rows_list.append([index,count])
    df1 = pd.DataFrame(rows_list[::-1])
    plt.clf()
    plot=df1.plot(y=[1],use_index=True)
    fig=plot.get_figure()
    plt.title('the most frequent nucleotide in each position')
    plt.xlabel('nucleatide position')
    plt.ylabel('number of reads')
    plt.legend([(plot_filename + '-' + str(i+1))])
    plt.locator_params(integer=True)
    fig.savefig(plot_filename + '-' + str(i+1) + ".png")
#plot seqlogo
for i in range(len(df_list)):
    seq_list=[]
    df_list[i].fillna('N', inplace=True)
    sequences=df_list[i][df_list[i].columns[0:]].apply(lambda x: ''.join(x.dropna().astype(str)),axis=1).tolist()
    for seq in sequences:
        seq_list.append(Seq(seq[::-1],IUPAC.protein))
    m = motifs.create(seq_list)
    plt.clf()
    m.weblogo(logo_name + '-' + str(i+1) + ".png", unit_name="probability", color_scheme="color_classic")
for seq in consensus_sequence:
    print(seq[::-1],file=final_out)
