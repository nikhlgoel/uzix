import argparse
import json
import sys

from uzix.core import detect


def main() -> None:
    parser = argparse.ArgumentParser(prog="uzix", description="Uzix prompt injection detector")
    parser.add_argument("prompt", nargs="*", help="Prompt text to inspect")
    parser.add_argument("--no-ml", action="store_true", help="Run rule-based detection only")
    args = parser.parse_args()

    text = " ".join(args.prompt) if args.prompt else input("Enter prompt: ")
    result = detect(text, use_ml=not args.no_ml)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    exit_codes = {"SAFE": 0, "SUSPICIOUS": 1, "DANGEROUS": 2}
    sys.exit(exit_codes.get(result["risk"], 0))


if __name__ == "__main__":
    main()