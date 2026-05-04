import os
from enum import Enum

from downloader.utils.filename import get_filename


class DownloadTask:
    def __init__(self, link, dir_path):
        self.link = link
        self.status = DownloadStatus.READY_TO_START
        self.error = None
        self.http_status = None
        
        self.filename = get_filename(link)
        self.filepath = os.path.join(dir_path, self.filename)

        self.size = 0

        self.start_time = None
        self.end_time = None

        self.retries = 0


    @property
    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


class DownloadStatus(Enum):
    READY_TO_START = 0
    IN_PROGRESS = 1
    SUCCESS = 2
    FAILURE = 3

    def __str__(self):
        if self == DownloadStatus.READY_TO_START:
            return "Waiting for the start"
        elif self == DownloadStatus.IN_PROGRESS:
            return "In progress"
        elif self == DownloadStatus.SUCCESS:
            return "Success"
        elif self == DownloadStatus.FAILURE:
            return "Failure"