import sys
import pandas as pd
from collections import defaultdict

freq_df = pd.read_csv(sys.argv[1], sep='\t', usecols=['frag','adjusted_freq'])

fragment_freq_dict = {row['frag']: row['adjusted_freq'] for _, row in freq_df.iterrows()}


bed_df = pd.read_csv(sys.stdin, sep='\t', header=None, names=['chr', 'seq1', 'seq2', 'frg', 'dot','sign'])

bed_df.dropna(subset=['seq1'], inplace=True)
bed_df.dropna(subset=['seq2'], inplace=True)
bed_df['seq1'] = bed_df['seq1'].astype(int)
bed_df['seq2'] = bed_df['seq2'].astype(int)


sampled_lines = []


for index, row in freq_df.iterrows():
    fragment = int(row['frag'])
    frequency = int(row['adjusted_freq'])

    resampled_bed_df = bed_df[(bed_df['seq2']-bed_df['seq1']).astype(int) == int(fragment)]
    print(f"Fragment: {fragment}, Matches Found: {len(resampled_bed_df)}")
    if not resampled_bed_df.empty:
        sampled = resampled_bed_df.sample(n=min(frequency, len(resampled_bed_df)), replace=True)
        sampled_lines.append(sampled)
    else:
        print("no matching lines for fragment")
        continue


if sampled_lines:

    final_sampled_df = pd.concat(sampled_lines)
    final_sampled_df.to_csv(sys.argv[2], sep='\t', header=False, index=False)
else:
    print("No lines were sampled")
