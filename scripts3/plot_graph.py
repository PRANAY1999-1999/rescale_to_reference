import sys
import pandas as pd
import matplotlib.pyplot as plt


df=pd.read_csv(sys.argv[1], sep='\t',names=['chr','seq1','seq2','frg','dot','sign'])
df_reference=pd.read_csv('/home/deserteagle/project/resample_data1/data/reference.hist', sep='\t', names=['fragment','normalized'])
df['seq1'] = pd.to_numeric(df['seq1'], errors='coerce')
df['seq2'] = pd.to_numeric(df['seq2'], errors='coerce')
df.dropna(subset=['seq1'], inplace=True)
df.dropna(subset=['seq2'], inplace=True)
df['seq1'] = df['seq1'].astype(int)
df['seq2'] = df['seq2'].astype(int)

df['frag']=df['seq2']-df['seq1']

df_freq=df['frag'].value_counts().reset_index()

df_freq.columns = [ 'frag', 'freq']

df_freq.sort_values(by='frag', ascending=True, inplace=True)

freq_sum = df_freq['freq'].sum()

df_freq['normalized_freq']=df_freq['freq']/freq_sum

plt.figure(figsize=(10, 5))

plt.plot(df_reference['fragment'], df_reference['normalized'], label='reference', color='green', marker='x')

plt.plot(df_freq['frag'], df_freq['normalized_freq'], label='resampled', color='purple', marker='o')

plt.xlabel('fragment_length')
plt.ylabel('normalized_frequency')
plt.title('Line Plot of reference and resampled')
plt.legend()

plt.grid()

output_file = sys.argv[2]
plt.savefig(output_file)

plt.close
