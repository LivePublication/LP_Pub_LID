from iso639 import Lang
import matplotlib.pyplot as plt
import numpy as np
import pickle
import json
import pandas as pd
import sys

class langauge_stats:
    name = "",
    overall_accuracy = 0,
    accuracy_by_language = {}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def convert_fastText(line):
    if line == "zhs":
      line = "zho"
    if line == "cti":
      line = "ctu"
    if line == "pob":
      line = "poh"
    if line == "cbm":
      line = "cak"
    if line == "eml":
      line = "egl"
    if line == "hva":
      line = "hus"
    if line == "mvj":
      line = "mam"
    if line == "cke":
      line = "cak"
    if line == "acc":
      line = "acr"
    if line == "tzc":
      line = "tzo"
    if line == "tzu":
      line = "tzo"
    if line == "zht":
      line = "zho"
    return line

def create_validation():
  with open(sys.argv[1], "r") as fastText:
      with open(sys.argv[2], "r") as langdetect:
          with open("output/fastText_validation.txt", "w") as fastText_validation:
            for line in fastText:
                line = line.strip()
                line = convert_fastText(line)
                fastText_validation.write(Lang(line).pt3 + "\n")
          with open("output/langdetect_validation.txt", "w") as langdetect_validation:
            count = 0
            for line in langdetect:
              count += 1
              lang_code = line[:line.index('-')] if '-' in line else line.strip()
              if "error" in lang_code:
                langdetect_validation.write(str(count) + "\n")
                print("error")
              else:
                langdetect_validation.write(Lang(lang_code).pt3 + "\n")

          with open(sys.argv[3], "r") as validation:
              with open("output/primary_validation.txt", "w") as primary_validation:
                  for line in validation:
                      primary_validation.write(Lang(line.strip()).pt3 + "\n")

def calculate_correct(primary, test):
    correct_count = 0
    incorrect_indices = []

    for i, (p, t) in enumerate(zip(primary, test)):
        if p == t:
            correct_count += 1
        else:
            incorrect_indices.append(i)

    return correct_count, incorrect_indices

def read_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.read().split('\n')
    # Removing empty strings if present
    lines = list(filter(None, lines))
    return lines, set(lines)

def calculate_accuracy_per_id(primary, test, unique_ids):
    # initialize the count and correct dictionaries with all IDs
    count_per_id = {id: 0 for id in unique_ids}
    correct_per_id = {id: 0 for id in unique_ids}

    for p, t in zip(primary, test):
        if p: # This will exclude empty strings
            # increment the total count for this ID
            count_per_id[p] += 1

            # increment the correct count for this ID
            if p == t:
                correct_per_id[p] += 1

    accuracy_per_id = {}
    for id in count_per_id.keys():
        accuracy_per_id[id] = round(correct_per_id[id] / count_per_id[id] * 100, 1) if count_per_id[id] > 0 else 0.0

    return accuracy_per_id

def create_bar_chart(fastText_accuracy_per_id, langdetect_accuracy_per_id):
    # Sort language IDs for consistent display
    language_ids = sorted(set(fastText_accuracy_per_id.keys()) | set(langdetect_accuracy_per_id.keys()))

    # Get the corresponding accuracies, defaulting to 0 if a language ID is not present in one of the dictionaries
    fastText_accuracies = [fastText_accuracy_per_id.get(lang_id, 0) for lang_id in language_ids]
    langdetect_accuracies = [langdetect_accuracy_per_id.get(lang_id, 0) for lang_id in language_ids]

    # Set the width of the bars
    bar_width = 0.35

    # Set the position of the FastText bars
    fastText_positions = [i for i, _ in enumerate(language_ids)]

    # Set the position of the Langdetect bars
    langdetect_positions = [i + bar_width for i, _ in enumerate(language_ids)]

    # Set the figure size
    plt.figure(figsize=(11.7, 8.3))  # A4 size in inches

    # Create the bars
    plt.barh(fastText_positions, fastText_accuracies, height=bar_width, color='#2f4b7c', edgecolor='gray')  # pastel blue bars
    plt.barh(langdetect_positions, langdetect_accuracies, height=bar_width, color='#ff6361', edgecolor='gray')  # pastel orange bars

    # Set the labels for the bars
    language_names = [Lang(lang_id).name.split("(")[0] for lang_id in language_ids]
    plt.yticks([pos + bar_width / 2 for pos in fastText_positions], language_names)

    # Set the chart title and labels
    plt.title('Model Accuracy by Language')
    plt.xlabel('Accuracy (%)')
    plt.ylabel('Language ID')

    # Show the legend
    plt.legend(['FastText', 'Langdetect'])

    # Show the chart
    plt.savefig('output/accuracy_by_language.png')

def main():
    # Read the files and get unique IDs
    primary_data, primary_unique_ids = read_file('output/primary_validation.txt')
    fastText_data, _ = read_file('output/fastText_validation.txt')
    langdetect_data, _ = read_file('output/langdetect_validation.txt')

    # Calculate correctness
    fastText_correct, fastText_incorrect_indices = calculate_correct(primary_data, fastText_data)
    langdetect_correct, langdetect_incorrect_indices = calculate_correct(primary_data, langdetect_data)

    # Calculate accuracy per ID
    fastText_accuracy_per_id = calculate_accuracy_per_id(primary_data, fastText_data, primary_unique_ids)
    langdetect_accuracy_per_id = calculate_accuracy_per_id(primary_data, langdetect_data, primary_unique_ids)

    # print(f'FastText got {fastText_correct} correct out of {len(primary_data)}.')
    # print(f'Langdetect got {langdetect_correct} correct out of {len(primary_data)}.')
    # print(f'Unique language IDs in primary data: {primary_unique_ids}')
    # print(f'FastText accuracy per ID: {fastText_accuracy_per_id}')
    # print(f'Langdetect accuracy per ID: {langdetect_accuracy_per_id}')

    fastText = langauge_stats()
    fastText.name = "FastText"
    fastText.accuracy_by_language = fastText_accuracy_per_id
    fastText.overall_accuracy = (fastText_correct / len(primary_data)) * 100

    langdetect = langauge_stats()
    langdetect.name = "Langdetect"
    langdetect.accuracy_by_language = langdetect_accuracy_per_id
    langdetect.overall_accuracy = (langdetect_correct / len(primary_data)) * 100

    with open("output/fastText_stats.json", "w") as fastText_stats:
        fastText_stats.write(langdetect.toJSON())
    with open("output/langdetect_stats.json", "w") as langdetect_stats:
        langdetect_stats.write(langdetect.toJSON())

    # In your main function, after calculating accuracies:
    fastText_df = pd.DataFrame.from_dict(fastText.accuracy_by_language, orient='index', columns=['FastText'])
    langdetect_df = pd.DataFrame.from_dict(langdetect.accuracy_by_language, orient='index', columns=['Langdetect'])

    # Merge the dataframes
    accuracy_df = pd.merge(fastText_df, langdetect_df, left_index=True, right_index=True, how='outer')

    # Fill NaN values with 0
    accuracy_df = accuracy_df.fillna(0)
    accuracy_df.index.name = 'Language_ID'
    
    # Save to CSV
    accuracy_df.to_csv('output/accuracy_by_language.csv')

    print(f"FastText overall accuracy: {fastText.overall_accuracy}")
    print(f"Langdetect overall accuracy: {langdetect.overall_accuracy}")
    create_bar_chart(fastText_accuracy_per_id, langdetect_accuracy_per_id)

if __name__ == '__main__':
    create_validation()
    main()




