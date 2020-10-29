'''
Title: align.py
Author:Yixun Huang
Description:
    This script will format txt files into fasta files.
    This is a step of allele.sh.
Usage:
    see allele.sh
'''
#format txt files into fasta files
import sys
with open (sys.argv[1],'r') as fin, open (sys.argv[2],'w') as fout:
    for line in fin:
        line =line.strip().split(" ")
#        fout.write(">{}\n{}".format(line[-2],line[-1]))
        print(">{}\n{}".format(line[-2],line[-1]), file=fout)
