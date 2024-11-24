import os
from pathlib import Path
from typing import Callable, List
import argparse
import sys

class FileMerger:
    """A class to merge text files with customizable sorting options."""
    
    def __init__(self, directory: str):
        """Initialize with the directory containing text files to merge."""
        self.directory = directory
        
    def _get_creation_time(self, filepath: str) -> float:
        """Get file creation time."""
        return os.path.getctime(filepath)
    
    def _get_modification_time(self, filepath: str) -> float:
        """Get file modification time."""
        return os.path.getmtime(filepath)
    
    def _get_file_size(self, filepath: str) -> int:
        """Get file size in bytes."""
        return os.path.getsize(filepath)
    
    def get_sorting_function(self, sort_by: str) -> Callable:
        """Return the appropriate sorting function based on user choice."""
        sort_functions = {
            'name': lambda x: x.lower(),
            'creation_time': self._get_creation_time,
            'modification_time': self._get_modification_time,
            'size': self._get_file_size
        }
        return sort_functions.get(sort_by, lambda x: x.lower())
    
    def merge_files(self, output_file: str, sort_by: str = 'name', 
                   exclude_patterns: List[str] = None, reverse: bool = False) -> None:
        """
        Merge text files from the directory into a single output file.
        
        Args:
            output_file (str): Path to the output file
            sort_by (str): Sorting method ('name', 'creation_time', 'modification_time', 'size')
            exclude_patterns (List[str]): List of patterns to exclude (e.g., ['.git', '*.pyc'])
            reverse (bool): Whether to sort in reverse order
        """
        # Get all files in directory and subdirectories
        files = []
        for root, dirs, filenames in os.walk(self.directory):
            # Skip excluded directories
            if exclude_patterns:
                dirs[:] = [d for d in dirs if not any(
                    pattern in d for pattern in exclude_patterns)]
            
            for filename in filenames:
                # Skip excluded files
                if exclude_patterns and any(
                    pattern in filename for pattern in exclude_patterns):
                    continue
                    
                filepath = os.path.join(root, filename)
                # Skip the output file itself if it exists
                if os.path.abspath(filepath) == os.path.abspath(output_file):
                    continue
                files.append(filepath)
        
        if not files:
            raise ValueError(f"No files found in {self.directory}")
        
        # Sort files according to the chosen method
        sort_func = self.get_sorting_function(sort_by)
        files.sort(key=sort_func, reverse=reverse)
        
        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Merge files
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for file_path in files:
                # Get relative path from input directory
                rel_path = os.path.relpath(file_path, self.directory)
                
                # Write file separator
                outfile.write(f"{'=' * 80}\n")
                outfile.write(f"// File: {rel_path}\n")
                outfile.write(f"{'=' * 80}\n\n")
                
                # Write file content
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        # Add newlines if the file doesn't end with them
                        if content and not content.endswith('\n'):
                            outfile.write('\n')
                        outfile.write('\n')
                except UnicodeDecodeError:
                    outfile.write(f"[Error: Could not read {rel_path} - file may be binary or encoded incorrectly]\n\n")
                except Exception as e:
                    outfile.write(f"[Error reading {rel_path}: {str(e)}]\n\n")
                
                # Write file end separator
                outfile.write(f"{'=' * 80}\n\n")

def main():
    """CLI entry point for the file merger."""
    parser = argparse.ArgumentParser(
        description='Merge text files from a directory into a single file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input_dir output.txt
  %(prog)s input_dir output.txt --sort creation_time --reverse
  %(prog)s input_dir output.txt --exclude "*.pyc" ".git" "__pycache__"
        """
    )
    
    parser.add_argument('input_directory', 
                       help='Directory containing files to merge')
    parser.add_argument('output_file', 
                       help='Path for the merged output file')
    parser.add_argument('--sort', choices=['name', 'creation_time', 
                       'modification_time', 'size'], default='name',
                       help='How to sort the files (default: name)')
    parser.add_argument('--reverse', action='store_true',
                       help='Reverse the sort order')
    parser.add_argument('--exclude', nargs='+', 
                       help='Patterns to exclude (e.g., ".git" "*.pyc")')
    
    args = parser.parse_args()
    
    try:
        merger = FileMerger(args.input_directory)
        merger.merge_files(
            output_file=args.output_file,
            sort_by=args.sort,
            exclude_patterns=args.exclude,
            reverse=args.reverse
        )
        print(f"Successfully merged files into {args.output_file}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()