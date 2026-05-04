# Read path and links

import os
import argparse
import asyncio

from downloader.config import DEFAULT_DOWNLOAD_DIR, DEFAULT_LINKS_FILE, PATH_ENTER_RETRIES

# ==SYNC PART==

def parse_args():
    parser = argparse.ArgumentParser(description="Async downloader")

    parser.add_argument('-k', '--keyboard', action='store_true', help='Switch to keyboard mode. If true, other arguments are ignored and keyboard input is expected.')
    parser.add_argument('-d', '--dir', type=str, default=DEFAULT_DOWNLOAD_DIR, help="Directory for downloaded file(s). Default: DEFAULT_DOWNLOAD_DIR from 'config.py'")
    parser.add_argument('-f', '--file', type=str, default=DEFAULT_LINKS_FILE, help="File with links to file(s). Default: DEFAULT_LINKS_FILE from 'config.py'")

    return parser.parse_args()


# validate_* funcs return error

def validate_download_dir(path):
    if path == "":
        return "'Download_dir' field is empty."

    if not os.path.isdir(path):
        return f"The path '{path}' does not exist."

    if not os.access(path, os.R_OK | os.W_OK):
        return f"There is no access to the folder '{path}'."
        
    return None


def validate_links_file(file):
    if file == "":
        return "'Links_file' field is empty."
    
    if not os.path.isfile(file):
        return f"'{file}' does not exist or is not a file."
    
    if os.path.getsize(file) == 0:
        return f"File '{file}' is empty."
    
    return None

# get_* funcs return value and error(s)

def get_path_by_keyboard(reporter):
    print(f"Please enter path where downloaded files will be saved (you have {PATH_ENTER_RETRIES} attempts):")

    for i in range(PATH_ENTER_RETRIES):
        path = input().strip()

        error = validate_download_dir(path)
        if error:
            reporter.error(error)
            print(f"Attempts left: {PATH_ENTER_RETRIES - i - 1}")
            continue

        return path, None
    
    return "", "All attempts to enter the path have been used."


def get_links_from_file(file):
    links = []
    errors = []

    with open(file, "r") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("http"):
                links.append(line)
            else:
                errors.append(f"Invalid line {i}: '{line}'")

    return links, errors
    

# input orchestrator: collects data (dir, links, errors) and decides if exit required
def get_input(reporter):
    args = parse_args()

    # --GET DOWNLOAD DIR--
    # case of keyboard mode: no default data
    if args.keyboard:
        reporter.info("Keyboard input mode has been selected.")
        download_dir, critical_error = get_path_by_keyboard(reporter)
        if critical_error: reporter.fatal(critical_error)
        return download_dir, []

    # case of default or args mode:
    download_dir = args.dir

    critical_error = validate_download_dir(download_dir)
    if critical_error:
        reporter.fatal(critical_error)
        return None, None

    # --GET LINKS (SYNC)--
    # cases of default or args mode only
    links_file = args.file

    critical_error = validate_links_file(links_file)
    if critical_error:
        reporter.fatal(critical_error)
        links = []
        return None, None

    else:
        links, errors = get_links_from_file(links_file)
        if errors:
            for e in errors: reporter.error(e)
            reporter.info("Line must contain link or comment starting with '#' or be empty.")
        if not links:
            reporter.fatal(f"Invalid file: {links_file}")
            return None, None

    return download_dir, links


# ==ASYNC PART==

async def get_link_by_keyboard():
    user_input = await asyncio.to_thread(input)
    return user_input