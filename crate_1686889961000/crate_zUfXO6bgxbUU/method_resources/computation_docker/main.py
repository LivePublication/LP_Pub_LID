from langdetect import DetectorFactory, detect, detect_langs
import os
import codecs 
import sys

# Directory constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.environ.get("INPUT_DIR", os.path.join(BASE_DIR, "input"))  
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(BASE_DIR, "output"))

if __name__ == "__main__":
    
    with codecs.open(sys.argv[1], "r", encoding = "utf-8") as f:
        lines = f.readlines()

      # write predictions to file
    with open(f"{OUTPUT_DIR}/langdetect_predictions.txt", "w") as f:
        counter = 0
        for line in lines:
            line = line.strip()  # Remove leading/trailing white space including '\n'
            if line:  # Only process the line if it's not empty
                print(counter)
                try:
                    f.write(detect(line) + "\n")
                except:
                    # Only write error if line isn't empty
                    if line:
                        f.write(f"error: {line}" + "\n")

                counter += 1

  