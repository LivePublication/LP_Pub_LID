from langdetect import DetectorFactory, detect, detect_langs
import os
import codecs 
import sys

# Directory constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.environ.get("INPUT_DIR", os.path.join(BASE_DIR, "input"))  
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(BASE_DIR, "output"))

if __name__ == "__main__":
    
    # Read input lines
    with codecs.open(sys.argv[1], "r", encoding = "utf-8") as f:
        lines = f.readlines()

    # Write predictions to file
    with open(f"{OUTPUT_DIR}/langdetect_predictions.txt", "w") as f:
        for line in lines:
            line = line.strip()  # Remove leading/trailing white space including '\\n'
            if line:  # Only process the line if it's not empty
                try:
                    detected_language = detect(line)
                    f.write(detected_language + "\n")
                except:
                    # In case of an exception, write an error line with the line content
                    f.write(f"error: {line} \n")
  