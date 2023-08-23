import os
import codecs
import pandas as pd
import json
import matplotlib.pyplot as plt
import sys

# Directory constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(BASE_DIR, "output"))
INPUT_DIR = os.environ.get("INPUT_DIR", os.path.join(BASE_DIR, "input"))

# ISO 639-1 (two-letter) to ISO 639-3 (three-letter) mapping
iso_639_1_to_639_3 = {
    'nl': 'nld', 'en': 'eng', 'fr': 'fra', 'de': 'deu', 'it': 'ita',
    'es': 'spa', 'zh': 'zho', 'ar': 'ara', 'bg': 'bul', 'el': 'ell',
    'hi': 'hin', 'ja': 'jpn', 'pl': 'pol', 'pt': 'por', 'ru': 'rus',
    'sw': 'swa', 'th': 'tha', 'tr': 'tur', 'ur': 'urd', 'vi': 'vie'
}

fasttext_conversion = {
    'zhs': 'zho',
    'cti': 'ctu',
    'pob': 'poh',
    'cbm': 'cak',
    'eml': 'egl',
    'hva': 'hus',
    'mvj': 'mam',
    'cke': 'cak',
    'acc': 'acr',
    'tzc': 'tzo',
    'tzu': 'tzo',
    'zht': 'zho'
}


class LanguageStats:
    def __init__(self, name):
        self.name = name
        self.overall_accuracy = 0
        self.accuracy_by_language = {}
        
    def toJSON(self):
        return json.dumps(self.__dict__)
    
def calculate_correct(primary, predictions):
    correct = sum([1 for p, pred in zip(primary, predictions) if p == pred])
    incorrect_indices = [i for i, (p, pred) in enumerate(zip(primary, predictions)) if p != pred]
    return correct, incorrect_indices
    
def calculate_accuracy_per_id(primary, predictions):
    correct_count = {}
    total_count = {}
    
    for p, pred in zip(primary, predictions):
        lang_id = p.strip()
        total_count[lang_id] = total_count.get(lang_id, 0) + 1
        if p == pred:
            correct_count[lang_id] = correct_count.get(lang_id, 0) + 1
            
    accuracy_per_id = {lang_id: round((correct_count.get(lang_id, 0) / total) * 100, 1) for lang_id, total in total_count.items()}
    return accuracy_per_id

def generate_statistics(primary, fastText_data, langdetect_data):
    fastText_correct, _ = calculate_correct(primary, fastText_data)
    langdetect_correct, _ = calculate_correct(primary, langdetect_data)
    
    fastText_accuracy_per_id = calculate_accuracy_per_id(primary, fastText_data)
    langdetect_accuracy_per_id = calculate_accuracy_per_id(primary, langdetect_data)
    
    fastText = LanguageStats("FastText")
    fastText.accuracy_by_language = fastText_accuracy_per_id
    fastText.overall_accuracy = (fastText_correct / len(primary)) * 100

    langdetect = LanguageStats("Langdetect")
    langdetect.accuracy_by_language = langdetect_accuracy_per_id
    langdetect.overall_accuracy = (langdetect_correct / len(primary)) * 100
    
    return fastText, langdetect

def create_validation(filename, model_type):
    with codecs.open(filename, "r", encoding = "utf-8") as f:
        lines = f.readlines()

    with open(f"{OUTPUT_DIR}/{model_type}_validation.txt", "w") as f:
        for line in lines:
            
            line = line.strip()
            # if model_type == "fastText":
            #   line = fasttext_conversion.get(line, line)
            line = iso_639_1_to_639_3.get(line, line)
            f.write(line + "\n")

def create_bar_chart(fastText_accuracy_per_id, langdetect_accuracy_per_id):
    df = pd.DataFrame(list(fastText_accuracy_per_id.items()), columns=["Language_ID", "FastText"])
    df["Langdetect"] = df["Language_ID"].map(langdetect_accuracy_per_id)
    df.set_index("Language_ID", inplace=True)
    
    df.plot(kind='bar', figsize=(15,7))
    plt.ylabel('Accuracy (%)')
    plt.title('Accuracy comparison by Language ID')
    plt.savefig(f"{OUTPUT_DIR}/accuracy_by_language.png")
    plt.show()

def save_accuracy_data_to_csv(fastText_accuracy_per_id, langdetect_accuracy_per_id):
    df = pd.DataFrame(list(fastText_accuracy_per_id.items()), columns=["Language_ID", "FastText"])
    df["Langdetect"] = df["Language_ID"].map(langdetect_accuracy_per_id)
    df.set_index("Language_ID", inplace=True)
    df.to_csv(f"{OUTPUT_DIR}/accuracy_by_language.csv")

if __name__ == "__main__":
    # Generate validation files
    create_validation(sys.argv[1], "fastText")
    create_validation(sys.argv[2], "langdetect")
    create_validation(sys.argv[3], "primary")
    
    # Load validation data
    with codecs.open(f"{OUTPUT_DIR}/primary_validation.txt", "r", encoding = "utf-8") as f:
        primary_validation = f.readlines()
    with codecs.open(f"{OUTPUT_DIR}/fastText_validation.txt", "r", encoding = "utf-8") as f:
        fastText_validation = f.readlines()
    with codecs.open(f"{OUTPUT_DIR}/langdetect_validation.txt", "r", encoding = "utf-8") as f:
        langdetect_validation = f.readlines()
    
    # Generate and print statistics
    fastText_stats, langdetect_stats = generate_statistics(primary_validation, fastText_validation, langdetect_validation)
    print(f"FastText overall accuracy: {fastText_stats.overall_accuracy:.1f}%")
    print(f"Langdetect overall accuracy: {langdetect_stats.overall_accuracy:.1f}%")
    
    # Generate the bar chart
    create_bar_chart(fastText_stats.accuracy_by_language, langdetect_stats.accuracy_by_language)
    # Save the accuracy data to CSV
    save_accuracy_data_to_csv(fastText_stats.accuracy_by_language, langdetect_stats.accuracy_by_language)
    with open(f"{OUTPUT_DIR}/fastText_stats.json", "w") as fastText_file:
        fastText_file.write(fastText_stats.toJSON())
    with open(f"{OUTPUT_DIR}/langdetect_stats.json", "w") as langdetect_file:
        langdetect_file.write(langdetect_stats.toJSON())

