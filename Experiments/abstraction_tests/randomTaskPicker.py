import os
import re
import random

def choose_random_task(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip()

def combine_tasks(folder_path, num_lines):
    files = os.listdir(folder_path)
    random_files = random.sample(files, num_lines)  # Choose 'num_lines' random files

    combined_tasks = ""
    objectives_matched = []
    for idx, file_name in enumerate(random_files):
        task = choose_random_task(os.path.join(folder_path, file_name))
        
        # Add conjunction randomly except for the first task
        if idx != 0:
            conjunction = random.choice(["", "And", "Also", "Then", "Afterwards"])
            combined_tasks += f" {conjunction} "
            
        combined_tasks += f"{task}"

        for obj in objectives:
            file_name_parts = file_name.split('_')
            if re.search(obj, file_name_parts[-1]):
                objectives_matched.append(obj)  # Store the filename

    combined_tasks = combined_tasks + "\n"  

    return combined_tasks, objectives_matched

objectives = ["banana", "apple", "cup", "laptop", "dog",  "bottle", "teddy-bear", "person", "bowl", "refrigerator", "home","garage","garden","office","bedroom","kitchen","workshop","dining-room","living-room", "cat"]

sample_folder = "/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/Test_samples/Level_02/samples"
solution_folder = "/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/Test_samples/Level_02/solutions"

os.makedirs(sample_folder, exist_ok=True)

nr_of_tasks = 10
nr_of_examples = 200
sample_file_path = os.path.join(sample_folder, "ordered_"+str(nr_of_tasks)+".txt")
solutions_file_path = os.path.join(solution_folder, "solution_"+str(nr_of_tasks)+".txt")

with open(sample_file_path, 'w') as output_file:
    with open(solutions_file_path, 'w') as objects_file:
        for i in range(nr_of_examples):
            combined_line, objectives_matched = combine_tasks("/home/frederike/Documents/Speciale/MasterThesisGit/final_tests/abstraction_tests/Test_samples/Successful_Level01_Tasks/", nr_of_tasks)
            output_file.write(combined_line)
            # Write filenames as strings to solutions file
            objects_file.write(','.join(objectives_matched) + '\n')
