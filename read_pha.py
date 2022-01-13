import pandas as pd
import numpy as np

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)

phadata = pd.read_table('lampung.pha', header=None, engine='python', sep='[\s,]{1,15}')
relocdd = pd.read_table('arivaltimee.txt', header=None, delim_whitespace=True)

relocdd[13] = relocdd[13].astype(str)
relocdd[14] = relocdd[14].astype(str)
relocdd[15] = relocdd[15].astype(str)
relocdd[1] = relocdd[1].map(lambda x: '{0:.6f}'.format(x))
relocdd[2] = relocdd[2].map(lambda x: '{0:.6f}'.format(x))
relocdd[3] = relocdd[3].map(lambda x: '{0:.3f}'.format(x)) 

#replace value origin pha with reloc dd
phadata[4] = phadata[14].map(relocdd.set_index(0)[13]) #t0 hour
phadata[5] = phadata[14].map(relocdd.set_index(0)[14]) #t0 min
phadata[6] = phadata[14].map(relocdd.set_index(0)[15]) #t0 sec
phadata[7] = phadata[14].map(relocdd.set_index(0)[1]) #lat
phadata[8] = phadata[14].map(relocdd.set_index(0)[2]) #lon
phadata[9] = phadata[14].map(relocdd.set_index(0)[3]) #depth

#remove unreloc event and arrival
id_reloc = relocdd[0]
phadata[15] = phadata[14].copy()
phadata[15].fillna(method='ffill', inplace=True)
new_phadata = phadata[phadata[15].isin(id_reloc)]
new_phadata = new_phadata.replace(np.nan, '', regex=True)
new_phadata.loc[(new_phadata[0] == '#'),1] = new_phadata[(new_phadata[0] == '#')][1].astype(np.int64).astype(str)
new_phadata.loc[(new_phadata[0] == '#'),11] = new_phadata[(new_phadata[0] == '#')][11].astype(np.int64).astype(str)
new_phadata.loc[(new_phadata[0] == '#'),12] = new_phadata[(new_phadata[0] == '#')][12].astype(np.int64).astype(str)
new_phadata.loc[(new_phadata[0] == '#'),13] = new_phadata[(new_phadata[0] == '#')][13].astype(np.int64).astype(str)
new_phadata[2] = new_phadata[2].astype(np.int64).astype(str)
del new_phadata[15]
new_phadata.to_csv('lampung.pha', index=False, sep='\t', header=False, float_format='%.3f')
print(new_phadata)

























