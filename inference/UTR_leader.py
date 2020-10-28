#!/Users/apple/anaconda3/bin/python3
#!/usr/bin/env python
'''
Title: barcode_remove
Author:Yixun Huang
Description:
    This script was used as one step in filter.sh. 
    It will merge column 'UTR' and 'leader' into a new column 'UTR_leader'
Usage:
    python UTR_leader.py 2_filtered_V_error_0.tab 3_merged.tab
'''

import pandas as pd
import sys
df = pd.read_csv(sys.argv[1], sep = '\t')
df['UTR_leader']= df['UTR'].str.cat(df['leader'],sep='')
df.to_csv(sys.argv[2], sep='\t')
