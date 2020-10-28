# 5'UTR-leaderseq inference pipeline
## Introduction
This is a tool can be used to infer the germline reference set of 5’UTR-leader sequence of immunoglobulin heavy chain (IGHV) genes based on the public dataset of antibody repertoires from naïve B-cells.

The pipeline is consist of three sections: 
* Data pre-process
* Inference of 5'UTR-leader sequences
* Quality control

## Table of contents
Purpose | tools
------------ | ------------- 
5'-barcode clipping | [barcode_remove.py](pre-process/barcode_remove.py)
Paired-end reads synchronizing | [PairSeq.py from pRESTO](https://presto.readthedocs.io/en/stable/tools/PairSeq.html#pairseq)
antibody repertoires analysis| [IgDiscover](http://docs.igdiscover.se/en/stable/index.html)
alignement filtering | [filtered.sh](https://github.com/yixun-h/5-UTR-leader_Infer/blob/main/filter.sh)
5'UTR-leader seqs extracting | [extract_UL.py](extract_UL.py)
summarizing seqs from subjects | [allele.sh](allele.sh)
summarizing seqs from alleles | [aligned.py](aligned.py) & [count.py](count.py)
Haplotype Inference  | [haplotyping.py](haplotyping.py)
CDR3-length distribution analysis | [CDR3_length.py](CDR3_length.py)

## Usage of code in project
![flow (1)](https://user-images.githubusercontent.com/61463722/97312948-5ebb5c00-1866-11eb-8c5e-ab5fa97846b8.png)

## Technologies
Project is created with:
* Python/3.6.6
* snakemake/5.2.4-Python-3.6.6
* Biopython/1.73-Python-3.6.6
* Anaconda3/2020.02

