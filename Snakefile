#This snakefile achieved the pre-process of raw data
samples=['ERR2567178','ERR2567179','ERR2567180','ERR2567181','ERR2567182','ERR2567183','ERR2567184','ERR2567185','ERR2567186','ERR2567187','ERR2567188','ERR2567189', \
'ERR2567190','ERR2567191','ERR2567192','ERR2567193','ERR2567194','ERR2567195','ERR2567196','ERR2567197','ERR2567198','ERR2567199', \
'ERR2567200','ERR2567201','ERR2567202','ERR2567203','ERR2567204','ERR2567205','ERR2567206','ERR2567207','ERR2567208','ERR2567209', \
'ERR2567210','ERR2567211','ERR2567212','ERR2567213','ERR2567214','ERR2567215','ERR2567216','ERR2567217','ERR2567218','ERR2567219', \
'ERR2567220','ERR2567221','ERR2567222','ERR2567223','ERR2567224','ERR2567225','ERR2567226','ERR2567227','ERR2567228','ERR2567229', \
'ERR2567230','ERR2567231','ERR2567232','ERR2567233','ERR2567234','ERR2567235','ERR2567236','ERR2567237','ERR2567238','ERR2567239', \
'ERR2567240','ERR2567241','ERR2567242','ERR2567243','ERR2567244','ERR2567245','ERR2567246','ERR2567247','ERR2567248','ERR2567249', \
'ERR2567250','ERR2567251','ERR2567252','ERR2567253','ERR2567254','ERR2567255','ERR2567256','ERR2567257','ERR2567258','ERR2567259', \
'ERR2567260','ERR2567261','ERR2567262','ERR2567263','ERR2567264','ERR2567265','ERR2567266','ERR2567267','ERR2567268','ERR2567269', \
'ERR2567270','ERR2567271','ERR2567272','ERR2567274','ERR2567276','ERR2567277']

rule all:
  input:
    expand(['1_igdiscover/{sample}/{sample}_1.fastq.gz','1_igdiscover/{sample}/{sample}_2.fastq.gz'], sample=samples),
    #expand('1_igdiscover/{sample}/database', sample=samples)
    expand('1_igdiscover/{sample}/standard', sample=samples)
#ruleorder: igdiscover > name_change 
rule barcode_remove:
    input:
        '2_remove_barcode/raw_data/{sample}_2.fastq'
    output:
        '2_remove_barcode/raw_data/filter_{sample}_2.fastq'
    shell:
        'python3 ~/2_remove_barcode/barcode_remove.py {input} {output}'

rule PairSeq:
    input:
        forward='2_remove_barcode/raw_data/filter_{sample}_2.fastq',
        reverse='2_remove_barcode/raw_data/{sample}_1.fastq'
    output:
        '2_remove_barcode/raw_data/{sample}_1_pair-pass.fastq',
        '2_remove_barcode/raw_data/filter_{sample}_2_pair-pass.fastq'
    shell:
        'PairSeq.py -1 {input.forward} -2 {input.reverse}'

rule zip:
    input:
        seq1='2_remove_barcode/raw_data/{sample}_1_pair-pass.fastq',
        seq2='2_remove_barcode/raw_data/filter_{sample}_2_pair-pass.fastq'
    output:
        seq1='2_remove_barcode/raw_data/{sample}_1_pair-pass.fastq.gz',
        seq2='2_remove_barcode/raw_data/filter_{sample}_2_pair-pass.fastq.gz'
    shell:
        'gzip {input.seq1};'
        'gzip {input.seq2}'

rule name_change:
    input:
        seq1='2_remove_barcode/raw_data/{sample}_1_pair-pass.fastq.gz',
        seq2='2_remove_barcode/raw_data/filter_{sample}_2_pair-pass.fastq.gz'
    output:
        seq1='1_igdiscover/{sample}/{sample}_1.fastq.gz',
        seq2='1_igdiscover/{sample}/{sample}_2.fastq.gz'
    shell:
        'mv {input.seq1} {output.seq1};'
        'mv {input.seq2} {output.seq2}'
        
rule igdiscover:
    params:
        pp="1_igdiscover/{sample}",
        seq="{sample}_1.fastq.gz"
    output:
        directory("1_igdiscover/{sample}/standard")
    shell:
        'cd {params.pp} && igdiscover init --db ~/database --reads1 {params.seq} standard;'
        'cd standard && nohup igdiscover run &'

