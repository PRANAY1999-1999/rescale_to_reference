import sys
import pandas as pd

df=pd.read_csv(sys.stdin, sep='\t',names=['chr','seq1','seq2','frg','dot','sign'])
df_reference=pd.read_csv('/home/deserteagle/project/resample_data1/data/reference.hist', sep='\t', names=['fragment','normalized'])
df['seq1'] = pd.to_numeric(df['seq1'], errors='coerce')
df['seq2'] = pd.to_numeric(df['seq2'], errors='coerce')

df.dropna(subset=['seq1'], inplace=True)
df.dropna(subset=['seq2'], inplace=True)
df['seq1'] = df['seq1'].astype(int)
df['seq2'] = df['seq2'].astype(int)

df['frag']=df['seq2']-df['seq1']
print("df['frag'] column created successfully:", 'frag' in df.columns)

df_freq=df['frag'].value_counts().reset_index()

df_freq.columns = [ 'frag', 'freq']

df_freq.sort_values(by='frag', ascending=True, inplace=True)

freq_sum = df_freq['freq'].sum()

df_freq['normalized_freq']=df_freq['freq']/freq_sum


df_freq = df_freq.merge(df_reference[['fragment', 'normalized']],left_on='frag', right_on='fragment', how='left')
df_freq.rename(columns={'normalized': 'ref_norm'}, inplace=True)

df_freq['diff_normalized']=df_freq['ref_norm'] - df_freq['normalized_freq']

max_index = df_freq['diff_normalized'].abs().idxmax()

max_new_normalized = df_freq.loc[max_index, 'ref_norm']
max_freq = df_freq.loc[max_index, 'freq']

df_freq['adjusted_freq'] =((df_freq['ref_norm']) / (max_new_normalized)) * max_freq
df_freq['adjusted_freq'] = df_freq['adjusted_freq'].round().fillna(0).astype(int)

output_file=sys.argv[1]
df_freq[['frag','adjusted_freq']].to_csv(output_file,sep='\t', index=False)

