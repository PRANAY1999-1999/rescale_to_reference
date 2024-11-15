import sys
import pandas as pd

run_df =  pd.read_csv("data/run_metadata.tsv", sep="\t", header="infer")
sample_df = pd.read_csv("data/sample.tsv" , sep = "\t" , header = "infer")

run_df.index = run_df["run"]
sample_df.index = sample_df["sample"]
print (run_df)
print (sample_df)

def get_all_runs_for_a_sample (wildcards):
    all_runs = sample_df.loc[wildcards.sample, "runs"].split(",")
    run_path_list = []
    for r in all_runs:
        p = run_df.loc[r, "file_path"]
        run_path_list.append(p)
    return run_path_list

rule cal_freq_norfreq:
    input:
         all_runs = lambda wildcards: get_all_runs_for_a_sample(wildcards)
    output:
          freq_norfreq = "freq_norfreq/for_{sample}.bed"
    shell:
         "cat {input.all_runs} | python3 scripts/cal_freq_norfreq.py {output.freq_norfreq}"


rule resample_bed_file:
    input:
        freq_norfreq = "freq_norfreq/for_{sample}.bed",
        all_runs = lambda wildcards: get_all_runs_for_a_sample(wildcards)
    output:
        resample_bed_file = "resample_bed/re_{sample}.bed"
    shell:
        "cat {input.all_runs} | python3 scripts2/resample_bed.py {input.freq_norfreq} {output.resample_bed_file}"

rule map_plot_graph:
    input:
        resample_bed_file = "resample_bed/re_{sample}.bed"
    output:
        map_plot_graph= "graph_plot/graph_{sample}.png"
    shell:
        "python3 scripts3/plot_graph.py {input.resample_bed_file} {output.map_plot_graph}"

