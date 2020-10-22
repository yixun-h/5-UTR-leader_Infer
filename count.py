#!/Users/apple/anaconda3/bin/python3
#!/usr/bin/env python3
# this script is used to sum frequency of the same sequences with different lengths
# and keep the shortest one.
# ./count.py IGHV4-4_07.fasta sum_IGHV4-4_07.fasta
# cd fasta/
# for f in *; do ./../count.py $f ../2_sum_80/$f; done
#
import sys
count=[]
seq_list=[]
seq_remove=[]
seq_short=[]
seq_final=[]
seq_dict={}
seqc_dict={}
with open (sys.argv[1],'r') as fin, open (sys.argv[2],'w') as fout:
    for line in fin:
        line=line.rstrip()
        if line.startswith('>'):
            count.append(int(line[1:]))
        else:
            seq_list.append(line[::-1])
    seq_dict=dict(zip(seq_list,count))
    seq_list.sort(key=len) # sorts by Ascending length

    #print(seq_list)
    #print(seq_dict)
    #for i in range(len(seq_list)):
    for seq in seq_list:
        counter=0
        for seq2 in seq_list:
            if seq2.startswith(seq):
                counter+=seq_dict[seq2]
                seqc_dict[seq]=counter
    #print(seqc_dict)
    for i in range(len(seq_list)):
        for j in range(len(seq_list)):
            if i !=j and seq_list[i].startswith(seq_list[j]):
                seq_remove.append(seq_list[i])

    for seq in seq_list:
        if not seq in seq_remove:
            seq_short.append(seq)
    for i in range(len(seq_short)):
        seq_list_split=[]
        for seq in seq_list:
            if seq.startswith(seq_short[i]):
                seq_list_split.append(seq)
        seq_list_split.sort(key=len,reverse=True) # sorts by descending length
        #print(seq_list_split)
        seq_final.append(seq_list_split)
    for i in range(len(seq_final)):
        for j in range(len(seq_final[i])):
            if seqc_dict[seq_final[i][j]] > seqc_dict[seq_final[i][-1]] * 80/100:
                print('>{}\n{}'.format(seqc_dict[seq_final[i][-1]],seq_final[i][j][::-1]),file=fout)
                break
'''
if len(seq_list)>1 and len(seq_list[0])+10<len(seq_list[1]):
    del seq_dict[seq_list[0]]
    seq_list.pop(0)
        #print(seqc_dict[seq_final[i][-1]])
###
#!the final count should consider the ones shorter than itself.
###
'''
