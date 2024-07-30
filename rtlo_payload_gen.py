import shutil
import os
import argparse


parser = argparse.ArgumentParser(description="Copy a file and apply RTLO obfuscation to the filename.")
parser.add_argument('-i', '--input_file', help='The input file. File name must not contain any numbers!', required=True)
parser.add_argument('-s', '--spoofed_suffix',help='The file suffix that should be spoofed', required=True)

args = parser.parse_args()

original_filename_without_suffix = os.path.splitext(args.input_file)[0]
print("Original filename:\t " + original_filename_without_suffix)

original_suffix = args.input_file.split(".")[-1]
print("Original suffix:\t " + original_suffix)

new_filename = original_filename_without_suffix + "\u202E" + args.spoofed_suffix [::-1] + "\uFEFF" + "." + original_suffix
print("New filename:\t " + new_filename)

shutil.copy2(args.input_file, new_filename)
