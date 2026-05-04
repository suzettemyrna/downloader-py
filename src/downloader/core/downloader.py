# Download one file

from downloader.models.download_task import DownloadStatus


async def download_file_manager(task, session, sem, reporter):
    async with sem:
        await download_file(task, session)


async def download_file(task, session):
    task.status = DownloadStatus.IN_PROGRESS

    try:
        async with session.get(task.link) as response:
            if response.status != 200:
                raise Exception("Bad status")

            content = await response.read()


        with open(task.filepath, "wb") as f:
            f.write(content)

        task.status = DownloadStatus.SUCCESS

    except Exception as e:
        task.status = DownloadStatus.FAILURE
