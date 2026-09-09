# Async File Downloader

Asynchronous file downloader built with Python,`asyncio` and `aiohttp`.

The project implements concurrent file downloads with a configurable concurrency limit, task-based orchestration, real-time terminal status updates, and two input modes: command-line arguments and interactive input.

---

## Features

* Concurrent file downloads with a configurable limit
* Asynchronous I/O with asyncio and aiohttp
* Task-based download management
* Real-time download status updates
* CLI and interactive input modes
* Configurable request timeout and concurrency limit
* Download retry configuration
* File size limit configuration
* Basic error handling and logging
* Automatic output filename handling

---

## How It Works

The downloader separates the download workflow into several components:

1. Input handlers collect the download directory and source URLs.
2. Each URL is represented as a DownloadTask.
3. The download manager creates and coordinates asynchronous tasks.
4. A concurrency limit controls how many files can be downloaded simultaneously.
5. The downloader performs HTTP requests using aiohttp.
6. The display component periodically updates the status of active and completed downloads.
7. The reporter produces the final download results.

This structure keeps input handling, download logic, task management, and presentation separate.

## Project Structure

```
project/
│
├── src/
│   ├── downloader.log
│   ├── links.txt
│   └── downloader/
│       ├── main.py
│       ├── config.py
│       ├── core/
│       │    ├── downloader.py
│       │    └── manager.py
│       ├── models/
│       │    └── download_task.py
│       └── utils/
│            ├── display.py
│            ├── filename.py
│            ├── input_handler.py
│            └── reporter.py
│
├── downloads/
├── requirements.txt
└── README.md
```

---

## Technologies

* Python 3.12+
* `asyncio`
* `aiohttp`
* `argparse`
* `logging`

---

## Installation

### 1. Create virtual environment

On Ubuntu/Debian:

```bash
sudo apt install python3.12-venv python3-pip
```
Then:

```bash
cd src/
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If you experience timeouts:

```bash
pip install -r requirements.txt -i https://pypi.org/simple
```

---

## Running the Program

Run from the `src/` directory:

```bash
python3 -m downloader [OPTIONS]
```

---

## Input Modes

### 1. CLI Mode (default)

Provide input via command-line arguments:

```bash
python3 -m downloader -d ../downloads -f links.txt
```

#### Arguments:

* `-d, --dir` — directory to save files
* `-f, --file` — file containing links

#### Behavior:

* If an argument is omitted → default from `config.py` is used
* If arguments are invalid → program terminates with error

---

### 2. Interactive Mode

```bash
python3 -m downloader -k
```

Flow:

1. Program asks for download directory
2. Then asks for links one by one
3. Empty input → stops input

Example:

```
Please enter path where downloaded files will be saved:
> ../downloads

Enter link (empty to finish):
> https://example.com/image.jpg
> https://example.com/file.png
>
```

---

## Example Input File

`links.txt`:

```
# comment
https://example.com/image1.jpg
https://example.com/image2.png
```

---

## Example Output (during execution)

```
+--------------------------------------+--------------+
| Link                                 | Status       |
+--------------------------------------+--------------+
| image1.jpg                           | In progress  |
| image2.png                           | Waiting      |
+--------------------------------------+--------------+
```

(Updated every second)

---

## Final Output

```
+--------------------------------------+---------+
| Link                                 | Status  |
+--------------------------------------+---------+
| image1.jpg                           | Success |
| image2.png                           | Failure |
+--------------------------------------+---------+
```

---

## Configuration

`config.py`:

* `PATH_ENTER_RETRIES` — attempts to enter download path
* `TIMEOUT` — total request timeout
* `MAX_CONCURRENT_DOWNLOADS` — concurrency limit
* `MAX_FILE_SIZE` — maximum file size
* `DOWNLOAD_RETRIES` — attempts to download a file
* default paths (download dir, links file, log file)

---

## Possible Improvements

* Stream files in chunks instead of loading the entire response into memory
* Add detailed progress indicators with downloaded size and percentage
* Improve error classification and reporting
* Add more comprehensive URL and response validation
* Improve CLI interaction and output formatting
* Add automated tests for core download and task-management logic

---

## Notes

* Some URLs (e.g. certain CDNs) may reject requests from Python clients
* In such cases, downloads may fail despite working in a browser

---

## Project Scope

This project focuses on asynchronous I/O, concurrency control, task orchestration, and separation of responsibilities within a command-line Python application.

---
