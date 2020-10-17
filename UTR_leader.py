#!/Users/apple/anaconda3/bin/python3
#!/usr/bin/env python
#merge column UTR and leafer into a new column 'UTR_leader'
# ./UTR_leader.py 2_filtered_V_error_0.tab 3_merged.tab

import pandas as pd
import sys
df = pd.read_csv(sys.argv[1], sep = '\t')
df['UTR_leader']= df['UTR'].str.cat(df['leader'],sep='')
df.to_csv(sys.argv[2], sep='\t')
