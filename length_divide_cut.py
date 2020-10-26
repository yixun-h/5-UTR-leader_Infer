#go to 3_filter2 and do
# python length_divide_cut.py ~/5_allele/2_sum_fasta/IGHV4-4_02.fasta IGHV4-4\*02
# python length_divide_cut.py ~/5_allele/2_sum_fasta/IGHV1-18_01.fasta IGHV1-18\*01

# maximum 8 lines in one plot

import glob
import pandas as pd
import sys
import matplotlib.pyplot as plt

filenames=glob.glob('**/6_CDR3_lowCDR_remove.txt', recursive=True)

seqs=[]
ids=[]
labels=["-A","-B","-C","-D","-E","-F"]
with open (sys.argv[1]) as fin:
    for line in fin:
        line = line.rstrip()
        if line.startswith(">"):
            ids.append(line[1:])
        else:
            seqs.append(line)
count= [0] * len(seqs)

colors=['aquamarine','coral','black','gold','purple','wheat']
fig, axs = plt.subplots(len(seqs), sharex=True)
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor="none", bottom=False, left=False)

for f in filenames:
    print(f)
    df=pd.read_csv(f, sep = '\t')
    new_df=df[df['V_gene'] == sys.argv[2]]
    new_df["CDR3 length"]= new_df["CDR3_aa"].str.len()
    seq=[]
    len_occu=[]
    len_sort_occu=[]
    for i in range(len(seqs)):
        seq.append(new_df[new_df["UTR_leader"].str.endswith(seqs[i], na=False)])
        len_occu.append(seq[i]['CDR3 length'].value_counts().to_frame().reset_index().rename(columns={'index':'CDR3 length', 'CDR3 length':'occurance'}))
        len_sort_occu.append(len_occu[i].sort_values('CDR3 length'))
        x=len_sort_occu[i]["CDR3 length"]
        y=len_sort_occu[i]['occurance']
        #print(i,"before:",count[i])
        if len(len_sort_occu[i])>1:
            #print(len_sort_occu[i])
            count[i]+=1
            #print(i,"after:",count[i])
            if count[i]<=8:
                if len(seqs)==1:
                    axs.plot(x,y,color=colors[i])
                else:
                    axs[i].plot(x,y,color=colors[i])
if len(seqs)==1:
    axs.legend([(sys.argv[2]+labels[i])],loc="upper right")
    axs.locator_params(integer=True)
else:
    for i,ax in enumerate(axs):
        axs[i].legend([(sys.argv[2]+labels[i])],loc="upper right")
        axs[i].locator_params(integer=True)
plt.xlabel('CDR3 length')
plt.ylabel('number of different entries')
fig.suptitle(("CDR3 length of sequences associated to \n the 5'UTR-leader sequence of " + sys.argv[2]))
plt.savefig(sys.argv[2] + "_cut.png")

