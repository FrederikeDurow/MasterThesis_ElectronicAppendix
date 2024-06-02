import os
import csv

def remove_failed_lines(csv_folder, txt_folder):
    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith('_config3.csv'):
            csv_path = os.path.join(csv_folder, csv_file)
            txt_file_name = csv_file.replace('_config3.csv', '.txt')
            txt_path = os.path.join(txt_folder, txt_file_name)
            if os.path.exists(txt_path):
                with open(csv_path, 'r', newline='') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    csv_data = list(csv_reader)
                    header = csv_data[0]
                    for row in csv_data[1:]:
                        if "FAILURE" in row[4]:
                            content_to_delete = row[0]
                            with open(txt_path, 'r') as txt_file:
                                lines = txt_file.readlines()
                            with open(txt_path, 'w') as txt_file:
                                for line in lines:
                                    if content_to_delete not in line:
                                        txt_file.write(line)



txt_folder ="/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/Test_samples/Successful_Level01_Tasks" 
csv_folder = "/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/Test_samples/config3_csvs"


remove_failed_lines(csv_folder, txt_folder)
