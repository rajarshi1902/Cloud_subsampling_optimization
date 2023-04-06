#!/usr/bin/python3

import os
import csv
import numpy as np
import subprocess
import multiprocessing
import analyzer as analyze_point_cloud #make sure the analyzer is in the same directory as all the other files

# Set up the input and output directories
input_dir = "sample-test"
output_dir = "output"

# Generate a list of random levels within the range
random_levels = np.random(0.1, 0.9)

# Set up the subsampling levels for space and voxel-based techniques
space_levels = [0.125, 0.225, 0.325, 0.425, 0.525, 0.625, 0.725, 0.825, 0.925]
voxel_levels = [0.125, 0.225, 0.325, 0.425, 0.525, 0.625, 0.725, 0.825, 0.925]

# Define a function to run a subsampling script for a given level
def run_subsampling_script(script_name, input_file, output_file, level):
    subprocess.run([
        "python",
        f"sampling-scripts/{script_name}",
        input_file,
        output_file,
        str(level)
    ])

# Define a function to run a task for a given input file and subsampling levels
def run_task(input_file):
    # Create the output directory for this file if it doesn't exist
    if not os.path.exists(f"{output_dir}/{input_file}"):
        os.makedirs(f"{output_dir}/{input_file}")

    # Run the subsampling scripts for each level
    for random_level in random_levels:
        random_output_file = f"{output_dir}/{input_file}/random_{random_level}.csv"
        run_subsampling_script("random_based.py", f"{input_dir}/{input_file}", random_output_file, random_level)

        for space_level in space_levels:
            space_output_file = f"{output_dir}/{input_file}/space_{random_level}_{space_level}.csv"
            run_subsampling_script("space_based.py", random_output_file, space_output_file, space_level)

            for voxel_level in voxel_levels:
                voxel_output_file = f"{output_dir}/{input_file}/voxel_{random_level}_{space_level}_{voxel_level}.csv"
                run_subsampling_script("voxel_based.py", space_output_file, voxel_output_file, voxel_level)

                # Analyze the output point cloud and compute m
                m = analyze_point_cloud.analyze_point_cloud(input_file, voxel_output_file)

                # Save the results to a CSV file
                with open("results.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([random_level, space_level, voxel_level, m])

# Create a pool of processes to run the tasks in parallel
with multiprocessing.Pool(processes=64) as pool:
    # Run the tasks for each input file
    input_files = os.listdir(input_dir)
    for input_file in input_files:
        pool.apply_async(run_task, args=(input_file,))

    # Wait for all the tasks to complete
    pool.close()
    pool.join()
