#create output file for CDR3 lengths plots and haplotyping analysis
cd ~/3_filter2/
for d in */; do #loop over directories
  cd ~/3_filter2/${d%/}/splitting/output
  for f in * #loop over alleles
  do
    cat $f >> ~/5_allele/2_reads/$f #write sequences into a new file named by allele
  done
done

#calculate frenquency
cd ~/5_allele/2_reads
for f in I*; do cat $f | sort | uniq -c | sort -n  >> ~/5_allele/2_frequency/"$f" ; done
cd ~/5_allele/2_frequency
for f in I*; do python ~/5_allele/align.py "$f" "../2_fasta/$f.fasta" ; done
