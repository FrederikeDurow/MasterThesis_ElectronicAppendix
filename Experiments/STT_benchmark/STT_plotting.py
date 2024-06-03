import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress Axes3D warnings if 3D plotting is not needed
try:
    from mpl_toolkits.mplot3d import Axes3D
except ImportError:
    pass

# Define the base directory where the files are located
baseDir = '/home/rasmus/Desktop/Master/MasterThesisGit/standalone_tests/STT_bencemark/results_dir/'

# Define file names and algorithm names
files = ['Google_results.csv', 'Silero_results.csv', 'Whisper-Ori_results.csv', 'Whisper-CT2-tiny_results.csv',
         'Whisper-CT2-base_results.csv', 'Whisper-CT2-small_results.csv', 'Whisper-CT2-distil-small_results.csv',
         'Whisper-CT2-large_results.csv', 'Whisper-CT2-distil-large_results.csv', 'Whisper-JAX_results.csv']
names = ['GoogleTTS', 'SileroTTS', 'Whisper-Original', 'Whisper-CT2-tiny', 'Whisper-CT2-base', 'Whisper-CT2-small',
         'Whisper-CT2-distil-small', 'Whisper-CT2-large', 'Whisper-CT2-distil-large', 'Whisper-JAX']

# Append the base directory to each filename
files = [os.path.join(baseDir, f) for f in files]

# Metrics to be plotted
metrics = ['ExecutionTime', 'RealTimeFactor', 'CPUUsage', 'MemoryUsage', 'WER']
metric_titles = ['Execution Time (ms)', 'Realtime Factor', 'CPU Usage (%)', 'Memory Usage (MB)', 'Word-error-rate']

# Colors for plots
colors = plt.get_cmap('tab10').colors

# Read and process all data once
all_data = []
for file in files:
    if os.path.isfile(file):
        try:
            data = pd.read_csv(file, encoding='ISO-8859-1')
            if 'Sentence_Index' not in data.columns:
                data['Sentence_Index'] = range(len(data))
            all_data.append(data)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            all_data.append(pd.DataFrame())
    else:
        all_data.append(pd.DataFrame())

# Set up seaborn style
sns.set(style="whitegrid")

# Loop through each metric and plot data
for i, metric in enumerate(metrics):
    plt.figure()
    valid_plot = False
    
    for j, data in enumerate(all_data):
        if not data.empty and metric in data.columns and 'Sentence_Index' in data.columns:
            plt.plot(data['Sentence_Index'], pd.to_numeric(data[metric], errors='coerce'), '-o', label=names[j], color=colors[j])
            valid_plot = True
    
    if valid_plot:
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.title(metric_titles[i], fontsize=18, fontweight='bold')
        plt.xlabel('Sentence Index', fontsize=14, fontweight='bold')
        plt.ylabel(metric_titles[i], fontsize=14, fontweight='bold')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'plot_{metric}.eps', format='eps')
    else:
        print(f"No valid data to plot for metric: {metric}")
    
    plt.close()

# Initialize data structure for metrics data and best performance tracking
metric_data = {metric: pd.DataFrame(index=names, columns=['Best', 'Worst', 'Average', 'StdDev'], dtype=float) for metric in metrics}

# Process each file and compute statistics
for j, data in enumerate(all_data):
    if not data.empty:
        for metric in metrics:
            if metric in data.columns:
                plot_data = pd.to_numeric(data[metric], errors='coerce').dropna()
                if not plot_data.empty:
                    metric_data[metric].loc[names[j]] = [plot_data.min(), plot_data.max(), plot_data.mean(), plot_data.std()]

# Identify and display the best performance
for metric in metrics:
    if not metric_data[metric]['Average'].isnull().all():
        best_algorithm = metric_data[metric]['Average'].idxmin()
        print(f'\n{metric_titles[metrics.index(metric)]} - Best Algorithm: {best_algorithm} (Average: {metric_data[metric]["Average"][best_algorithm]:.2f})')

# Display each metric's table
for metric in metrics:
    print(f'\nMetric: {metric_titles[metrics.index(metric)]}')
    print(metric_data[metric])

# Generate bar plots
for i, metric in enumerate(metrics):
    dataMatrix = [metric_data[metric]['Average'][name] if name in metric_data[metric].index else np.nan for name in names]
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(names, dataMatrix, color=[colors[j] for j in range(len(names))])
    plt.xticks(rotation=45, ha='right', fontsize=14, fontweight='bold')
    plt.yticks(fontsize=14, fontweight='bold')
    plt.ylabel(metric_titles[i], fontsize=16, fontweight='bold')
    plt.title(metric_titles[i].replace('_', ' '), fontsize=20, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Add value labels on the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(baseDir, f'{metric}_bar_plot.eps'))
    plt.close()
