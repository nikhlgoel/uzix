import sys
import json
from detector.hybrid import detect

def main():
    if len(sys.argv) < 2:
        text = input("Enter prompt: ")
    else:
        text = " ".join(sys.argv[1:])

    result = detect(text)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    # exit code signals risk for pipeline use
    codes = {"SAFE": 0, "SUSPICIOUS": 1, "DANGEROUS": 2}
    sys.exit(codes.get(result["risk"], 0))

if __name__ == "__main__":
    main()
