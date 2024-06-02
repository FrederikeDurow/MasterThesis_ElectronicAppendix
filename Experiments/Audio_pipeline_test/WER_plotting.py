import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_rel

# Function to read WER results from a CSV file
def read_wer_results(csv_path):
    wers = []
    with open(csv_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header
        for row in csvreader:
            wers.append(float(row[2]))  # WER is in the third column
    return wers

# Function to calculate average WER
def calculate_average_wer(wers):
    return np.mean(wers)

# Paths to the outer folders and their corresponding configurations in order
outer_folders = {
    '/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/Audio_pipeline_test/Microphone Configurations': [
        'Config 1',
        'Config 2',
        'Config 3',
        'Config 4'
    ],
    '/home/rasmus/Desktop/Master/MasterThesisGit/final_tests/Audio_pipeline_test/VAD Configurations': [
        'Config 1',
        'Config 2',
        'Config 3',
        'Config 4',
        'Config 5'
    ]
}


# Function to perform paired t-test
def perform_paired_ttest(wers1, wers2):
    t_stat, p_value = ttest_rel(wers1, wers2)
    return t_stat, p_value

# Configure matplotlib for a nicer appearance
plt.rcParams.update({
    'font.size': 14,
    'font.weight': 'bold',
    'axes.labelweight': 'bold',
    'axes.titlesize': 18,
    'axes.titleweight': 'bold',
    'legend.fontsize': 12,
    'legend.title_fontsize': 14
})

# Process each outer folder
for outer_folder, config_order in outer_folders.items():
    all_wers = []
    avg_wers = []
    configurations = []

    for configuration_folder in config_order:
        configuration_folder_path = os.path.join(outer_folder, configuration_folder)
        if os.path.isdir(configuration_folder_path):
            csv_path = os.path.join(configuration_folder_path, 'results.csv')
            if os.path.exists(csv_path):
                # Read WER results
                wers = read_wer_results(csv_path)
                all_wers.append(wers)
                configurations.append(configuration_folder)
                
                # Calculate and print average WER
                avg_wer = calculate_average_wer(wers)
                avg_wers.append(avg_wer)
                print(f'Average WER for {configuration_folder}: {avg_wer:.2f}')
            else:
                print(f'Warning: results.csv not found for {configuration_folder_path}')
        else:
            print(f'Warning: Directory not found for {configuration_folder_path}')
    
    # Ensure configurations and average WERs are in the correct order
    configurations_sorted = [config for config in config_order if config in configurations]
    avg_wers_sorted = [avg_wers[configurations.index(config)] for config in configurations_sorted]

    print(f'Configurations: {configurations_sorted}')
    print(f'Average WERs: {avg_wers_sorted}')

    # Generate the line plot for WER
    plt.figure(figsize=(12, 8))
    for wers, config in zip(all_wers, configurations_sorted):
        plt.plot(wers, marker='o', linestyle='-', label=config)
    plt.xlabel('Sentence Index')
    plt.ylabel('Word Error Rate (WER)')
    plt.title(f'WER for Configurations in {os.path.basename(outer_folder)}')
    plt.legend()
    plt.grid(True)
    
    # Save the line plot as EPS
    plot_path = os.path.join(outer_folder, f'{os.path.basename(outer_folder)}_wer_plot.eps')
    plt.savefig(plot_path, format='eps')
    plt.close()

    # Generate the bar plot for average WER
    plt.figure(figsize=(12, 8))
    plt.bar(configurations_sorted, avg_wers_sorted, color='skyblue')
    plt.xlabel('Configuration')
    plt.ylabel('Average Word Error Rate (WER)')
    plt.title(f'Average WER for Configurations in {os.path.basename(outer_folder)}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the bar plot as EPS
    bar_plot_path = os.path.join(outer_folder, f'{os.path.basename(outer_folder)}_avg_wer_bar_plot.eps')
    plt.savefig(bar_plot_path, format='eps')
    plt.close()

    # Perform statistical tests and print results
    for i in range(len(all_wers)):
        for j in range(i + 1, len(all_wers)):
            t_stat, p_value = perform_paired_ttest(all_wers[i], all_wers[j])
            print(f'T-test between {configurations_sorted[i]} and {configurations_sorted[j]}: t-statistic={t_stat:.2f}, p-value={p_value:.4f}')
            if p_value < 0.05:
                print(f'Significant difference found between {configurations_sorted[i]} and {configurations_sorted[j]} (p < 0.05)')

print("Plots saved as EPS files, average WER printed for each configuration, and statistical tests performed.")






