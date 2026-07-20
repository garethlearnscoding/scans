#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(prog="pipeline")

subparsers = parser.add_subparsers(
    dest="mode",
    required=True,
)

# ------------------------
# OCR mode
# ------------------------
ocr = subparsers.add_parser("ocr", help="Run OCR pipeline")
ocr.add_argument("--input", required=True)
ocr.add_argument("--output", required=True)
ocr.add_argument("--model", required=True)
ocr.add_argument("--workers", type=int, default=4)

# ------------------------
# Rename mode
# ------------------------
rename = subparsers.add_parser("rename", help="Rename files")
rename.add_argument("--csv", required=True)
rename.add_argument("--directory", required=True)

# ------------------------
# Clean mode
# ------------------------
clean = subparsers.add_parser("clean", help="Clean temporary files")
clean.add_argument("--directory", required=True)

args = parser.parse_args()

print(args)