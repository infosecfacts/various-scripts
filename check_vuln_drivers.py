import os
import pefile
import argparse

# List of functions to highlight
highlight_functions = [
    "MmMapIoSpace",
    "MmMapIoSpaceEx",
    "MmMapLockedPages",
    "MmMapLockedPagesSpecifyCache",
    "MmMapLockedPagesWithReservedMapping"
]

# ANSI escape codes for colored output
YELLOW_BOLD = '\033[1;33m'
RESET = '\033[0m'

def get_sys_files(directory):
    """Get all .sys files in the given directory."""
    sys_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.sys'):
                sys_files.append(os.path.join(root, file))
    return sys_files

def read_iat(file_path):
    """Read and print the Import Address Table (IAT) of the given PE file."""
    try:
        pe = pefile.PE(file_path)
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            print(f"Imports for {file_path}:")
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    func_name = imp.name.decode() if imp.name else None
                    if func_name:
                        if func_name in highlight_functions:
                            print(f"{YELLOW_BOLD}  -> {func_name}{RESET}")
                        else:
                            print(f"  - {func_name}")
        else:
            print(f"No imports found for {file_path}.")
    except pefile.PEFormatError:
        print(f"{file_path} is not a valid PE file.")

def main(path):
    if os.path.isdir(path):
        sys_files = get_sys_files(path)
    elif os.path.isfile(path) and path.endswith('.sys'):
        sys_files = [path]
    else:
        print(f"Invalid path: {path}")
        return

    for sys_file in sys_files:
        read_iat(sys_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan .sys files and read their IAT.")
    parser.add_argument("path", help="Directory or single .sys file to scan")
    args = parser.parse_args()
    main(args.path)
