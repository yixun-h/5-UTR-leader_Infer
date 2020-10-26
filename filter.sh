#!/usr/bin/env bash
gunzip filtered.tab
cat filtered.tab | awk -F "\t" -v OFS="\t" 'NR==1; {if ($28 == 0) {print $0}}' > 2_filtered_V_error_0.tab
python ~/3_filter/UTR_leader.py 2_filtered_V_error_0.tab 3_merged.tab
cat 3_merged.tab | cut -f 3,53 | grep .> 4_UL.txt
echo "$(tail -n +2 4_UL.txt)" > 4_UL.txt #remove header
cat 4_UL.txt | awk '$2!=""' | sort -k2 -n > 5_UL_empty_remove.txt #remove lines whoes sequences is empty and sort numerically by 1th column
cat expressed_V.tab | awk -F "\t" -v OFS="\t" 'NR==1; {if ($3 < 75) {print $0}}' | cut -f 1 > low_CDR.txt
echo "$(tail -n +2 low_CDR.txt)" > low_CDR.txt
#filter by CDR<75
python ../low_CDR.py low_CDR.txt 5_UL_empty_remove.txt 6_lowCDR_remove.txt
cat 6_lowCDR_remove.txt | tr \* _ > 7_lowCDR_remove.txt
mkdir splitting
cat 7_lowCDR_remove.txt | awk -F '\t' '{ fname = "splitting/" $1".txt"; print >>fname; close(fname) }'
bash ../rmlc.sh -less 20 *.txt   #filter by number of reads < 20
mkdir splitting/output
cd splitting
bash ~/3_filter2/rmlc.sh -less 20 *.txt   #filter by number of reads < 20
for f in *.txt; do python ~/3_filter2/extractUL.py "$f" "output/${f%.txt}" "${f%.txt}" "${f%.txt}_seqlogo"; done
