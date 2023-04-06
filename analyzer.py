import csv

def analyze_point_cloud(original_file, processed_file):
    # Load original point cloud and count desired points
    with open(original_file) as f:
        reader = csv.reader(f)
        original_points = 0
        desired_points = 0
        for row in reader:
            original_points += 1
            label = int(row[4])
            if label in [5, 6, 7, 8]:
                desired_points += 1

    # Load processed point cloud and count desired points
    with open(processed_file) as f:
        reader = csv.reader(f)
        processed_points = 0
        desired_processed_points = 0
        for row in reader:
            processed_points += 1
            label = int(row[4])
            if label in [5, 6, 7, 8]:
                desired_processed_points += 1

    # Calculate ratio of desired points in processed file to original file
    m = desired_processed_points / original_points

    return m


#To call this function (uncomment)
# original_file_path = '/path/to/original/file.csv'
# processed_file_path = '/path/to/processed/file.csv'
# m = analyze_point_cloud(original_file_path, processed_file_path)
# print('m:', m)
