'''
Title: barcode_remove
Author:Yixun Huang
Description:
    This program will summarize all the sequences from alleles into one final file/
Usage:
    ./sum.sh
'''

for f in * #loop over alleles
do
  echo $(pwd)/$f >>~/igdiscover/5_alignment/all_new.fasta;
  cat $f  >> ~/igdiscover/5_alignment/all_new.fasta
done
