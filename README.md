# File Merger

A command-line tool to merge multiple text files from a directory (and its subdirectories) into a single output file.

## Features

- Recursively merges all text files from a directory
- Multiple sorting options (by name, creation time, modification time, or size)
- Exclude files/directories using patterns
- Clear file separation in output with file paths
- UTF-8 encoding support
- Error handling for binary or incorrectly encoded files

## Installation

Clone the repository and ensure you have Python 3.x installed.

```bash
git clone https://github.com/alexhooketh/merger.git
cd merger
```

## Usage

```bash
python merger.py <input_directory> <output_file> [options]
```

### Options

- `--sort`: Sort files by different criteria
  - `name` (default): Sort by filename
  - `creation_time`: Sort by file creation time
  - `modification_time`: Sort by last modified time
  - `size`: Sort by file size
- `--reverse`: Reverse the sort order
- `--exclude`: Patterns to exclude (can specify multiple)

### Examples

```bash
# Basic usage - merge all files sorted by name
python merger.py ./input_folder output.txt

# Sort by modification time in reverse order
python merger.py ./input_folder output.txt --sort modification_time --reverse

# Exclude specific patterns
python merger.py ./input_folder output.txt --exclude "*.pyc" ".git" "__pycache__"
```

## Output Format

The merged file will contain each input file separated by clear markers:

```
================================================================================
// File: path/to/file.txt
================================================================================

[Content of file.txt]

================================================================================
```

## Error Handling

- Binary files or files with incorrect encoding are skipped with error messages
- Directory creation for output file if needed
- Informative error messages for common issues

# Disclaimer

Everything you just read above, including the script itself, was written by an AI. I, Alex Hook, have no idea if any of it is correct, but the script works good. I made it to merge the docs and such multi-file stuff into a single large file to feed into LLMs with restrictions on the number of input files. Maybe such script even already exists, idk.