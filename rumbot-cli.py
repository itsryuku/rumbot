#!/usr/bin/env python
## As the name suggests this is the command-line version of tool
## To run the script, provide the channel ID and the desired number of viewers as command-line arguments
## e.g python3 rumbot-cli.py 12345678 200 
## Author: Ryuku

import argparse
import httpx
import random
import string
import asyncio

def generate_viewer_id():
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

async def start_viewbotting(session, channel_id, num_viewers):
    url = f"https://wn0.rumble.com/service.php?video_id={channel_id}&name=video.watching-now"
    response = await session.get(url)
    if "data" not in response.json():
        print("Channel doesn't exist, please refer to https://github.com/Ryukudz/rumbot to learn how to get the video id.")
        return False

    url = "https://wn0.rumble.com/service.php?name=video.watching-now"
    tasks = []
    for _ in range(num_viewers):
        viewer_id = generate_viewer_id()
        data = {"video_id": channel_id, "viewer_id": viewer_id}
        task = session.post(url, data=data)
        tasks.append(task)

    await asyncio.gather(*tasks)
    print("Viewers sent...\nWhen you are done press ^C to exit.")
    return True

async def keep_viewbotting(session, channel_id, num_viewers, interval_seconds=80):
    try:
        while True:
            if await start_viewbotting(session, channel_id, num_viewers):
                await asyncio.sleep(interval_seconds)
            else:
                break
    except KeyboardInterrupt:
        print("Ctrl + C Pressed. Stopping the viewbotting...")

async def main():
    parser = argparse.ArgumentParser(description="Rumble video Viewbot CLI Tool")
    parser.add_argument("video_id", type=str, help="Video ID to viewbot")
    parser.add_argument("num_viewers", type=int, help="Number of viewers to send")
    args = parser.parse_args()

    async with httpx.AsyncClient() as session:
        await keep_viewbotting(session, args.video_id, args.num_viewers)

if __name__ == "__main__":
    asyncio.run(main())
