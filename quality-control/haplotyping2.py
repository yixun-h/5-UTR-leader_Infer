#!/Users/apple/anaconda3/bin/python3
#!/usr/bin/env python
# If you have two different leader/5'UTR sequences for one specific allele,
# you could support their existence by showing that one of the sequences are only found on one chromosome
# while the other is only found on the other allele.

# descripting: this script is used to do the hapltyping for one allele from a individual
#  ./haplotyping.py IGHV4-30-2*01 IGHV4-30-2_01
import pandas as pd
import sys
df = pd.read_csv("3_merged.tab", sep = '\t')
new_df=df[df['V_gene'].str.startswith(sys.argv[1])]
#print(df1[df1['J_gene'].str.match('IGHJ6\*03')])
with open (sys.argv[2]) as fin:
    for line in fin:
        seq = line.rstrip()
J1_seq=new_df[(new_df['J_gene'].str.match('IGHJ6\*02'))& new_df["UTR_leader"].str.endswith(seq)]
J2_seq=new_df[(new_df['J_gene'].str.match('IGHJ6\*03'))& new_df["UTR_leader"].str.endswith(seq)]

print(',{},{},{}'.format(sys.argv[1],len(J1_seq),len(J2_seq)))
