# Async File Downloader

Asynchronous file downloader built with `asyncio` and `aiohttp`.

The project demonstrates:

* concurrent I/O with `asyncio`
* task orchestration
* separation of concerns (core / utils / models)
* CLI + interactive input handling

---

## Features

* Concurrent downloads (configurable limit)
* Real-time status updates in console
* Two input modes (CLI / interactive)
* Basic error handling and logging
* Task-based architecture (`DownloadTask`)

---

## Project Structure

```
project/
│
├── src/
│   └── downloader/
│       ├── main.py
│       ├── config.py
│       ├── downloader.log
│       ├── links.txt
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

## Installation

### 1. Create virtual environment

```bash
sudo apt install python3.12-venv python3-pip

cd src/
python3 -m venv venv
source venv/bin/activate
```

---

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

## Current Limitations

* Files are fully loaded into memory (no streaming yet)
* No retry mechanism
* No per-file timeout handling
* No progress tracking
* Limited validation of URLs/content

---

## Planned Improvements

* Chunked downloading (streaming)
* Retry logic
* Progress indicators (size / percentage)
* File size limits
* Better error classification
* Improved CLI UX

---

## Notes

* Some URLs (e.g. certain CDNs) may reject requests from Python clients
* In such cases, downloads may fail despite working in a browser

---

## Purpose

Educational project to explore:

* async programming in Python
* concurrency control
* clean architecture

---