import sys
import asyncio

from downloader.config import DEFAULT_LOG_FILE
from downloader.utils.input_handler import get_input
from downloader.utils.reporter import Reporter
from downloader.core.manager import main_async


def main():
    reporter = Reporter(DEFAULT_LOG_FILE)

    download_dir, links = get_input(reporter)

    if reporter.exit_required: sys.exit(1)

    asyncio.run(main_async(download_dir, links, reporter))