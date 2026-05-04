# orchestrator

import asyncio
import aiohttp

from downloader.config import TIMEOUT, MAX_CONCURRENT_DOWNLOADS
from downloader.utils.input_handler import get_link_by_keyboard
from downloader.utils.display import print_in_process_message, print_final_table
from downloader.models.download_task import DownloadTask
from downloader.core.downloader import download_file_manager


async def main_async(path, links, reporter):
    task_objs = []
    async_tasks = []

    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    sem = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        if links:
            create_tasks_list(links, path, task_objs, async_tasks, session, sem, reporter)

        else:
            print("Enter link (empty to finish):")
            create_tasks_list_keyboard_mode(path, task_objs, async_tasks, session, sem, reporter)

        if task_objs:
            display_task = asyncio.create_task(display_loop(task_objs))

            await asyncio.gather(*async_tasks, return_exceptions=True)

            display_task.cancel()
            try:
                await display_task
            except asyncio.CancelledError:
                pass

            print_final_table(task_objs)


def create_tasks_list(links, path, task_objs, async_tasks, session, sem, reporter):
    for link in links:
        task_obj = DownloadTask(link, path)
        task_objs.append(task_obj)

        t = asyncio.create_task(download_file_manager(task_obj, session, sem, reporter))
        async_tasks.append(t)


async def create_tasks_list_keyboard_mode(path, task_objs, async_tasks, session, sem, reporter):
    while True:
        link = await get_link_by_keyboard()
        if link == "":
            break

        task_obj = DownloadTask(link, path)
        task_objs.append(task_obj)

        t = asyncio.create_task(download_file_manager(task_obj, session, sem, reporter))
        async_tasks.append(t)


async def display_loop(task_objs):
    while True:
        print_in_process_message(task_objs)
        await asyncio.sleep(1)