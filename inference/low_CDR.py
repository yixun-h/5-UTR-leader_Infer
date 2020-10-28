#!/Users/apple/anaconda3/bin/python3
#!/usr/bin/env python
'''
Title: barcode_remove
Author:Yixun Huang
Description:
    This script was used as one step in filter.sh. 
    It will remove the alleles which is in "low_CDR.txt" because their CDR3 is lower than 75.
Usage:
    python low_CDR.py low_CDR.txt 5_UL_empty_remove.txt 6_lowCDR_remove.txt
'''
import sys
alleles=[]
output=''
with open (sys.argv[1],'r') as fin1, open(sys.argv[2],'r') as fin2, open(sys.argv[3],'w') as fout:
    for line in fin1:
        alleles.append(line.rstrip())
    for line in fin2:
        if not line.split('\t')[0] in alleles:
            fout.write(line)

