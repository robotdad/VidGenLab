# tools/**/*.py

[collect-files]

**Search:** ['tools/**/*.py']
**Exclude:** ['__pycache__', '*.pyc']
**Include:** []
**Date:** 8/18/2025, 9:53:16 AM
**Files:** 4

=== File: tools/build_ai_context_files.py ===
#!/usr/bin/env python3
"""
Build AI Context Files Script

This script imports the collect_files module and calls its functions directly
 to generate Markdown files containing code and recipe files for AI context.

This script should be placed at:
[repo_root]/tools/build_ai_context_files.py

And will be run from the repository root.
"""

import argparse
import datetime
import os
import platform
import re
import sys

OUTPUT_DIR = "ai_context/generated"

# We're running from repo root, so that's our current directory
global repo_root
repo_root = os.getcwd()

# Add the tools directory to the Python path
tools_dir = os.path.join(repo_root, "tools")
sys.path.append(tools_dir)

# Import the collect_files module
try:
    import collect_files  # type: ignore
except ImportError:
    print(f"Error: Could not import collect_files module from {tools_dir}")
    print("Make sure this script is run from the repository root.")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build AI Context Files script that collects project files into markdown."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Always overwrite files, even if content unchanged",
    )
    return parser.parse_args()


def ensure_directory_exists(file_path) -> None:
    """Create directory for file if it doesn't exist."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")


def strip_date_line(text: str) -> str:
    """Remove any '**Date:** …' line so we can compare content ignoring timestamps."""
    # Remove the entire line that begins with **Date:**
    return re.sub(r"^\*\*Date:\*\*.*\n?", "", text, flags=re.MULTILINE)


def build_context_files(force=False) -> None:
    # Define the tasks to run
    tasks = [
        {
            "patterns": ["src/**/*.py"],
            "output": f"{OUTPUT_DIR}/source_code.md",
            "exclude": ["__pycache__", "*.pyc", ".pytest_cache", "*.egg-info"],
            "include": [],
        },
        {
            "patterns": ["*.toml", "*.yml", "*.yaml", "Makefile", "ruff.toml"],
            "output": f"{OUTPUT_DIR}/config_files.md",
            "exclude": ["uv.lock"],
            "include": [],
        },
        {
            "patterns": ["*.md"],
            "output": f"{OUTPUT_DIR}/documentation.md",
            "exclude": ["ai_context/generated"],
            "include": [],
        },
        {
            "patterns": ["examples/**/*"],
            "output": f"{OUTPUT_DIR}/examples.md",
            "exclude": ["*.mp4", "*.jpg", "*.png", "*.jpeg"],
            "include": [],
        },
        {
            "patterns": ["tools/**/*.py"],
            "output": f"{OUTPUT_DIR}/tools.md",
            "exclude": ["__pycache__", "*.pyc"],
            "include": [],
        },
    ]

    # Execute each task
    for task in tasks:
        patterns = task["patterns"]
        output = task["output"]
        exclude = task["exclude"]
        include = task["include"]

        # Ensure the output directory exists
        ensure_directory_exists(output)

        print(f"Collecting files for patterns: {patterns}")
        print(f"Excluding patterns: {exclude}")
        print(f"Including patterns: {include}")

        # Collect the files
        files = collect_files.collect_files(patterns, exclude, include)
        print(f"Found {len(files)} files.")

        # Build header
        now = datetime.datetime.now()
        # Use appropriate format specifiers based on the platform
        if platform.system() == "Windows":
            date_str = now.strftime("%#m/%#d/%Y, %#I:%M:%S %p")  # Windows non-padding format
        else:
            date_str = now.strftime("%-m/%-d/%Y, %-I:%M:%S %p")  # Unix non-padding format
        header_lines = [
            f"# {' | '.join(patterns)}",
            "",
            "[collect-files]",
            "",
            f"**Search:** {patterns}",
            f"**Exclude:** {exclude}",
            f"**Include:** {include}",
            f"**Date:** {date_str}",
            f"**Files:** {len(files)}\n\n",
        ]
        header = "\n".join(header_lines)

        # Build content body
        content_body = ""
        for file in files:
            rel_path = os.path.relpath(file)
            content_body += f"=== File: {rel_path} ===\n"
            try:
                with open(file, encoding="utf-8") as f:
                    content_body += f.read()
            except Exception as e:
                content_body += f"[ERROR reading file: {e}]\n"
            content_body += "\n\n"

        new_content = header + content_body

        # If file exists and we're not forcing, compare (ignoring only the date)
        if os.path.exists(output) and not force:
            try:
                with open(output, encoding="utf-8") as f:
                    existing_content = f.read()
                # Strip out date lines from both
                existing_sanitized = strip_date_line(existing_content).strip()
                new_sanitized = strip_date_line(new_content).strip()
                if existing_sanitized == new_sanitized:
                    print(f"No substantive changes in {output}, skipping write.")
                    continue
            except Exception as e:
                print(f"Warning: unable to compare existing file {output}: {e}")

        # Write the file (new or forced update)
        with open(output, "w", encoding="utf-8") as outfile:
            outfile.write(new_content)
        print(f"Written to {output}")


def main():
    args = parse_args()

    # Verify we're in the repository root by checking for key directories/files
    required_paths = [os.path.join(repo_root, "tools", "collect_files.py")]

    missing_paths = [path for path in required_paths if not os.path.exists(path)]
    if missing_paths:
        print("Warning: This script should be run from the repository root.")
        print("The following expected paths were not found:")
        for path in missing_paths:
            print(f"  - {path}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != "y":
            sys.exit(1)

    build_context_files(force=args.force)


if __name__ == "__main__":
    main()


=== File: tools/build_git_collector_files.py ===
#!/usr/bin/env python3
"""
Runs git-collector → falls back to npx automatically (with --yes) →
shows guidance only if everything fails.
"""

import os
import subprocess
import sys
from shutil import which
from textwrap import dedent

OUTPUT_DIR = "ai_context/git_collector"


# Debug function - can be removed or commented out when fixed
def print_debug_info():
    print("===== DEBUG INFO =====")
    print(f"PATH: {os.environ.get('PATH', '')}")
    npx_location = which("npx")
    print(f"NPX location: {npx_location}")
    print("======================")


def guidance() -> str:
    return dedent(
        """\
        ❌  git-collector could not be run.

        Fixes:
          • Global install ……  npm i -g git-collector
          • Or rely on npx (no install).

        Then re-run:  make ai-context-files
        """
    )


def run(cmd: list[str], capture: bool = True) -> subprocess.CompletedProcess:
    """Run a command, optionally capturing its output."""
    print("→", " ".join(cmd))
    return subprocess.run(
        cmd,
        text=True,
        capture_output=capture,
    )


def main() -> None:
    root = sys.argv[1] if len(sys.argv) > 1 else OUTPUT_DIR

    # Uncomment to see debug info when needed
    # print_debug_info()

    # Preferred runners in order
    runners: list[list[str]] = []
    git_collecto_path = which("git-collector")
    if git_collecto_path:
        runners.append([git_collecto_path])
    pnpm_path = which("pnpm")
    if pnpm_path:
        try:
            # Check if git-collector is available via pnpm by running a simple list command
            # Redirect output to avoid cluttering the console
            result = subprocess.run(
                [pnpm_path, "list", "git-collector"],
                capture_output=True,
                text=True,
                check=False,
            )

            # If git-collector is in the output, it's installed via pnpm
            if "git-collector" in result.stdout and "ERR" not in result.stdout:
                runners.append([pnpm_path, "exec", "git-collector"])
        except Exception:
            # If any error occurs during check, move to next option
            pass

    # For npx, we need to try multiple approaches
    # First, check if npx is in the PATH
    npx_path = which("npx")
    if npx_path:
        # Use the full path to npx if we can find it
        runners.append([npx_path, "--yes", "git-collector"])
    else:
        # Fallback to just the command name as a last resort
        runners.append(["npx", "--yes", "git-collector"])

    if not runners:
        sys.exit(guidance())

    last_result = None
    for r in runners:
        # Capture output for git-collector / pnpm, but stream for npx (shows progress)
        is_npx = "npx" in r[0].lower() if isinstance(r[0], str) else False
        is_git_collector = "git-collector" in r[0].lower() if isinstance(r[0], str) else False
        capture = not (is_npx or is_git_collector)

        print(f"Executing command: {' '.join(r + [root, '--update'])}")
        try:
            last_result = run(r + [root, "--update"], capture=capture)
        except Exception as e:
            print(f"Error executing command: {e}")
            continue
        if last_result.returncode == 0:
            return  # success 🎉
        if r[:2] == ["pnpm", "exec"]:
            print("pnpm run not supported — falling back to npx …")

    # All attempts failed → print stderr (if any) and guidance
    if last_result and last_result.stderr:
        print(last_result.stderr.strip(), file=sys.stderr)
    sys.exit(guidance())


if __name__ == "__main__":
    main()


=== File: tools/collect_files.py ===
#!/usr/bin/env python3
"""
Collect Files Utility

Recursively scans the specified file/directory patterns and outputs a single Markdown
document containing each file's relative path and its content.

This tool helps aggregate source code files for analysis or documentation purposes.

Usage examples:
  # Collect all Python files in the current directory:
  python collect_files.py *.py > my_python_files.md

  # Collect all files in the 'output' directory:
  python collect_files.py output > my_output_dir_files.md

  # Collect specific files, excluding 'utils' and 'logs', but including Markdown files from 'utils':
  python collect_files.py *.py --exclude "utils,logs,__pycache__,*.pyc" --include "utils/*.md" > my_output.md
"""

import argparse
import datetime
import fnmatch
import glob
import os
import pathlib

# Default exclude patterns: common directories and binary files to ignore.
DEFAULT_EXCLUDE = [
    ".venv",
    "node_modules",
    "*.lock",
    ".git",
    "__pycache__",
    "*.pyc",
    "*.ruff_cache",
    "logs",
    "output",
]


def parse_patterns(pattern_str: str) -> list[str]:
    """Splits a comma-separated string into a list of stripped patterns."""
    return [p.strip() for p in pattern_str.split(",") if p.strip()]


def resolve_pattern(pattern: str) -> str:
    """
    Resolves a pattern that might contain relative path navigation.
    Returns the absolute path of the pattern.
    """
    # Convert the pattern to a Path object
    pattern_path = pathlib.Path(pattern)

    # Check if the pattern is absolute or contains relative navigation
    if os.path.isabs(pattern) or ".." in pattern:
        # Resolve to absolute path
        return str(pattern_path.resolve())

    # For simple patterns without navigation, return as is
    return pattern


def match_pattern(path: str, pattern: str, component_matching=False) -> bool:
    """
    Centralized pattern matching logic.

    Args:
        path: File path to match against
        pattern: Pattern to match
        component_matching: If True, matches individual path components
                           (used primarily for exclude patterns)

    Returns:
        True if path matches the pattern
    """
    # For simple exclude-style component matching
    if component_matching:
        parts = os.path.normpath(path).split(os.sep)
        return any(fnmatch.fnmatch(part, pattern) for part in parts)

    # Convert paths to absolute for consistent comparison
    abs_path = os.path.abspath(path)

    # Handle relative path navigation in the pattern
    if ".." in pattern or "/" in pattern or "\\" in pattern:
        # If pattern contains path navigation, resolve it to an absolute path
        resolved_pattern = resolve_pattern(pattern)

        # Check if this is a directory pattern with a wildcard
        if "*" in resolved_pattern:
            # Get the directory part of the pattern
            pattern_dir = os.path.dirname(resolved_pattern)
            # Get the filename pattern
            pattern_file = os.path.basename(resolved_pattern)

            # Check if the file is in or under the pattern directory
            file_dir = os.path.dirname(abs_path)
            if file_dir.startswith(pattern_dir):
                # Match the filename against the pattern
                return fnmatch.fnmatch(os.path.basename(abs_path), pattern_file)
            return False  # Not under the pattern directory
        # Direct file match
        return abs_path == resolved_pattern or fnmatch.fnmatch(abs_path, resolved_pattern)
    # Regular pattern without navigation, use relative path matching
    return fnmatch.fnmatch(path, pattern)


def should_exclude(path: str, exclude_patterns: list[str]) -> bool:
    """
    Returns True if any component of the path matches an exclude pattern.
    """
    for pattern in exclude_patterns:
        if match_pattern(path, pattern, component_matching=True):
            return True
    return False


def should_include(path: str, include_patterns: list[str]) -> bool:
    """
    Returns True if the path matches any of the include patterns.
    Handles relative path navigation in include patterns.
    """
    return any(match_pattern(path, pattern) for pattern in include_patterns)


def collect_files(
    patterns: list[str], exclude_patterns: list[str], include_patterns: list[str]
) -> list[str]:
    """
    Collects file paths matching the given patterns, applying exclusion first.
    Files that match an include pattern are added back in.

    Returns a sorted list of absolute file paths.
    """
    collected = set()

    # Process included files with simple filenames or relative paths
    for pattern in include_patterns:
        # Check for files in the current directory first
        direct_matches = glob.glob(pattern, recursive=True)
        for match in direct_matches:
            if os.path.isfile(match):
                collected.add(os.path.abspath(match))

        # Then check for relative paths
        if ".." in pattern or os.path.isabs(pattern):
            resolved_pattern = resolve_pattern(pattern)

            # Direct file inclusion
            if "*" not in resolved_pattern and os.path.isfile(resolved_pattern):
                collected.add(resolved_pattern)
            else:
                # Pattern with wildcards
                directory = os.path.dirname(resolved_pattern)
                if os.path.exists(directory):
                    filename_pattern = os.path.basename(resolved_pattern)
                    for root, _, files in os.walk(directory):
                        for file in files:
                            if fnmatch.fnmatch(file, filename_pattern):
                                full_path = os.path.join(root, file)
                                collected.add(os.path.abspath(full_path))

    # Process the main patterns
    for pattern in patterns:
        matches = glob.glob(pattern, recursive=True)
        for path in matches:
            if os.path.isfile(path):
                process_file(path, collected, exclude_patterns, include_patterns)
            elif os.path.isdir(path):
                process_directory(path, collected, exclude_patterns, include_patterns)

    return sorted(collected)


def process_file(
    file_path: str, collected: set[str], exclude_patterns: list[str], include_patterns: list[str]
) -> None:
    """Process a single file"""
    abs_path = os.path.abspath(file_path)
    rel_path = os.path.relpath(file_path)

    # Skip if excluded and not specifically included
    if should_exclude(rel_path, exclude_patterns) and not should_include(
        rel_path, include_patterns
    ):
        return

    collected.add(abs_path)


def process_directory(
    dir_path: str, collected: set[str], exclude_patterns: list[str], include_patterns: list[str]
) -> None:
    """Process a directory recursively"""
    for root, dirs, files in os.walk(dir_path):
        # Filter directories based on exclude patterns, but respect include patterns
        dirs[:] = [
            d
            for d in dirs
            if not should_exclude(os.path.join(root, d), exclude_patterns)
            or should_include(os.path.join(root, d), include_patterns)
        ]

        # Process each file in the directory
        for file in files:
            full_path = os.path.join(root, file)
            process_file(full_path, collected, exclude_patterns, include_patterns)


def read_file(file_path: str) -> tuple[str, str | None]:
    """
    Read a file and return its content.

    Returns:
        Tuple of (content, error_message)
    """
    # Check if file is likely binary
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            if b"\0" in chunk:  # Simple binary check
                return "[Binary file not displayed]", None

        # If not binary, read as text
        with open(file_path, encoding="utf-8") as f:
            return f.read(), None
    except UnicodeDecodeError:
        # Handle encoding issues
        return "[File contains non-UTF-8 characters]", None
    except Exception as e:
        return "", f"[ERROR reading file: {e}]"


def format_output(
    file_paths: list[str],
    format_type: str,
    exclude_patterns: list[str],
    include_patterns: list[str],
    patterns: list[str],
) -> str:
    """
    Format the collected files according to the output format.

    Args:
        file_paths: List of absolute file paths to format
        format_type: Output format type ("markdown" or "plain")
        exclude_patterns: List of exclusion patterns (for info)
        include_patterns: List of inclusion patterns (for info)
        patterns: Original input patterns (for info)

    Returns:
        Formatted output string
    """
    output_lines = []

    # Add metadata header
    now = datetime.datetime.now()
    date_str = now.strftime("%-m/%-d/%Y, %-I:%M:%S %p")
    output_lines.append(f"# {patterns}")
    output_lines.append("")
    output_lines.append("[collect-files]")
    output_lines.append("")
    output_lines.append(f"**Search:** {patterns}")
    output_lines.append(f"**Exclude:** {exclude_patterns}")
    output_lines.append(f"**Include:** {include_patterns}")
    output_lines.append(f"**Date:** {date_str}")
    output_lines.append(f"**Files:** {len(file_paths)}\n\n")

    # Process each file
    for file_path in file_paths:
        rel_path = os.path.relpath(file_path)

        # Add file header based on format
        if format_type == "markdown":
            output_lines.append(f"### File: {rel_path}")
            output_lines.append("```")
        else:
            output_lines.append(f"=== File: {rel_path} ===")

        # Read and add file content
        content, error = read_file(file_path)
        if error:
            output_lines.append(error)
        else:
            output_lines.append(content)

        # Add file footer based on format
        if format_type == "markdown":
            output_lines.append("```")

        # Add separator between files
        output_lines.append("\n")

    return "\n".join(output_lines)


def main() -> None:
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Recursively collect files matching the given patterns and output a document with file names and content."
    )
    parser.add_argument(
        "patterns",
        nargs="+",
        help="File and/or directory patterns to collect (e.g. *.py or output)",
    )
    parser.add_argument(
        "--exclude",
        type=str,
        default="",
        help="Comma-separated patterns to exclude (will be combined with default excludes: "
        + ",".join(DEFAULT_EXCLUDE)
        + ")",
    )
    parser.add_argument(
        "--include",
        type=str,
        default="",
        help="Comma-separated patterns to include (overrides excludes if matched)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["markdown", "plain"],
        default="plain",
        help="Output format (default: plain)",
    )
    args = parser.parse_args()

    # Parse pattern arguments and combine with default excludes
    user_exclude_patterns = parse_patterns(args.exclude)
    exclude_patterns = DEFAULT_EXCLUDE + user_exclude_patterns

    include_patterns = parse_patterns(args.include) if args.include else []

    # Collect files
    patterns = args.patterns
    files = collect_files(patterns, exclude_patterns, include_patterns)

    # Format and print output
    output = format_output(files, args.format, exclude_patterns, include_patterns, patterns)
    print(output)


if __name__ == "__main__":
    main()


=== File: tools/list_by_filesize.py ===
#!/usr/bin/env python3
import os
import sys


def get_file_sizes(directory):
    """
    Recursively get all files in the directory tree and their sizes.
    Returns a list of tuples (file_path, size_in_bytes).
    """
    file_sizes = []

    # Walk through the directory tree
    for dirpath, _dirnames, filenames in os.walk(directory):
        for filename in filenames:
            # Get the full path of the file
            file_path = os.path.join(dirpath, filename)

            # Get the file size if it's a file (not a symbolic link)
            if os.path.isfile(file_path) and not os.path.islink(file_path):
                try:
                    size = os.path.getsize(file_path)
                    file_sizes.append((file_path, size))
                except (OSError, FileNotFoundError):
                    # Skip files that can't be accessed
                    pass

    return file_sizes


def format_size(size_bytes):
    """Format file size in a human-readable format"""
    # Define size units
    units = ["B", "KB", "MB", "GB", "TB", "PB"]

    # Convert to appropriate unit
    unit_index = 0
    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024
        unit_index += 1

    # Format with 2 decimal places if not bytes
    if unit_index == 0:
        return f"{size_bytes} {units[unit_index]}"
    return f"{size_bytes:.2f} {units[unit_index]}"


def main():
    # Use the provided directory or default to current directory
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."

    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)

    # Get all files and their sizes
    file_sizes = get_file_sizes(directory)

    # Sort by size in descending order
    file_sizes.sort(key=lambda x: x[1], reverse=True)

    # Print the results
    print(f"Files in '{directory}' (sorted by size, largest first):")
    print("-" * 80)
    print(f"{'Size':<10} {'Path':<70}")
    print("-" * 80)

    for file_path, size in file_sizes:
        # Convert the size to a human-readable format
        size_str = format_size(size)
        print(f"{size_str:<10} {file_path}")


if __name__ == "__main__":
    main()


