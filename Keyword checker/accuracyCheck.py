import json
import os

def get_accuracy(expected_keywords, predicted_keywords):
    # initialize variables for accuracy calculation
    total_expected_keywords = len(expected_keywords)
    total_correct_predictions = 0

    # compare the predicted and expected keywords
    predicted_keywords = [tag for tag, confidence in predicted_keywords if confidence >= 0.01]
    for tag_list in expected_keywords:
        if any(tag in predicted_keywords for tag in tag_list):
            total_correct_predictions += 1

    # calculate accuracy
    accuracy = total_correct_predictions / total_expected_keywords
    return accuracy

# set up paths to directories
path_jsons_photo_devoir = '' # Set up the path
path_expected_keywords = 'expected_keywords'

# initialize variables for accuracy calculation
total_expected_keywords = 0
total_correct_predictions = 0

# iterate over all files in jsons_photo_devoir and check if they have a corresponding file in expected_keywords
for root, dirs, files in os.walk(path_jsons_photo_devoir):
    for filename in files:
        # check if the file has a corresponding file in expected_keywords
        expected_path = os.path.join(path_expected_keywords, filename)
        if os.path.exists(expected_path):
            # if so, load the contents of both files and get the accuracy
            json_path = os.path.join(root, filename)
            with open(json_path, 'r') as json_file:
                json_data = json.load(json_file)
            with open(expected_path, 'r') as expected_file:
                expected_data = json.load(expected_file)
            accuracy = get_accuracy(expected_data['keywords'], json_data['tags'])
            print(f"Accuracy for {filename}: {accuracy}")
            total_expected_keywords += len(expected_data['keywords'])
            total_correct_predictions += len(expected_data['keywords']) * accuracy

# calculate total accuracy
total_accuracy = total_correct_predictions / total_expected_keywords
print(f"Total Accuracy: {total_accuracy*100:.2f}%")


