#!/Users/apple/anaconda3/bin/python3
#!/usr/bin/env python
'''
Title: haplotyping.py
Author:Yixun Huang
Description:
    This script will infer the haplotypes of heterozogous indivuduals by explore the assocaition between IGHV gene and IGHJ6 genes.
Usage:
    python ~/haplotyping.py IGHV4-4-2\*02 splitting/output/IGHV4-4_02 
'''
import pandas as pd
import sys
seqs=[]
df = pd.read_csv("3_merged.tab", sep = '\t')
new_df=df[df['V_gene'] == sys.argv[1]]
df1 = new_df[['J_gene','UTR_leader']]
print(sys.argv[1])

with open (sys.argv[2]) as fin:
    for line in fin:
        line = line.rstrip()
        print(line)
        seqs.append(line)

J1_seq1=new_df[(new_df['J_gene'].str.match('IGHJ6\*02'))& new_df["UTR_leader"].str.endswith(seqs[0])]
J1_seq2=new_df[(new_df['J_gene'].str.match('IGHJ6\*02'))& new_df["UTR_leader"].str.endswith(seqs[1])]
J2_seq1=new_df[(new_df['J_gene'].str.match('IGHJ6\*03'))& new_df["UTR_leader"].str.endswith(seqs[0])]
J2_seq2=new_df[(new_df['J_gene'].str.match('IGHJ6\*03'))& new_df["UTR_leader"].str.endswith(seqs[1])]

print('J1_seq1:',len(J1_seq1),'\nJ1_seq2:',len(J1_seq2),'\nJ2_seq1:',len(J2_seq1),'\nJ2_seq2:',len(J2_seq2))
