#!/usr/bin/env python
"""
Author: Ryuku - https://ryukudz.com
"""
import httpx
import random
import string
import asyncio
import webbrowser
import tkinter as tk

channel_id_entry = None
num_viewers_entry = None
status_label = None
send_button = None
stop_button = None
are_we_botting = False

def create_gui():
    global channel_id_entry, num_viewers_entry, status_label, send_button, stop_button
    app = tk.Tk()
    app.title("Rumbot - Rumble Viewbot tool")
    app.configure(bg="#161618")
    app.resizable(False, False)

    channel_id_label = tk.Label(app, text="Video ID:", fg="white", bg="#161618")
    channel_id_label.grid(row=0, column=0, padx=10, pady=5)
    channel_id_entry = tk.Entry(app, width=20)
    channel_id_entry.grid(row=0, column=1, padx=10, pady=5)

    num_viewers_label = tk.Label(app, text="Number of Viewers:", fg="white", bg="#161618")
    num_viewers_label.grid(row=1, column=0, padx=10, pady=5)
    num_viewers_entry = tk.Entry(app, width=20)
    num_viewers_entry.grid(row=1, column=1, padx=10, pady=5)

    question_label = tk.Label(app, text="?", fg="white", bg="#0078d4", cursor="hand2")
    question_label.grid(row=0, column=0, padx=0, pady=0, sticky="e")
    question_label.bind("<Button-1>", lambda e: on_help_click())

    status_label = tk.Label(app, text="", fg="green", bg="#161618")
    status_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    send_button = tk.Button(app, text="Send", width=12, command=on_send_clicked, bg="#0078d4", fg="white", borderwidth=0)
    send_button.grid(row=4, column=0, padx=10, pady=5)

    stop_button = tk.Button(app, text="Stop", width=12, command=on_stop_clicked, bg="#e81123", fg="white", borderwidth=0)
    stop_button.grid(row=4, column=1, padx=10, pady=5)

    button_font = ("Arial", 12, "bold")
    send_button.config(font=button_font)
    stop_button.config(font=button_font)
    footer_label = tk.Label(app, text="© - Ryuku", fg="white", bg="#161618", cursor="hand2")
    footer_label.grid(row=5, column=1, pady=5, padx=10, sticky="e")
    footer_label.bind("<Button-1>", lambda e: on_footer_click())

    app.mainloop()

def on_help_click():
    webbrowser.open("https://raw.githubusercontent.com/Ryukudz/Rumble-Viewer-Bot/main/tab.png")

def on_footer_click():
    webbrowser.open("https://ryukudz.com")

def generate_viewer_id():
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(8))


async def start_viewbotting(session, channel_id, num_viewers):
    url = f"https://wn0.rumble.com/service.php?video_id={channel_id}&name=video.watching-now"
    response = await session.get(url)
    if "data" not in response.json():
        status_label.config(text="Channel doesn't exist.", fg="red")
        return False


    url = "https://wn0.rumble.com/service.php?name=video.watching-now"
    tasks = []
    for _ in range(num_viewers):
        viewer_id = generate_viewer_id()
        data = {"video_id": channel_id, "viewer_id": viewer_id}
        task = session.post(url, data=data)
        tasks.append(task)

    await asyncio.gather(*tasks)
    channel_id_entry.config(state=tk.DISABLED)
    num_viewers_entry.config(state=tk.DISABLED)
    send_button.config(state=tk.DISABLED)

    return True


async def keep_viewbotting(session, channel_id, num_viewers, interval_seconds=80):
    while True:
        if await start_viewbotting(session, channel_id, num_viewers):
            await asyncio.sleep(interval_seconds)
        else:
            break
        await session.aclose()


def on_send_clicked():
    global are_we_botting
    channel_id = channel_id_entry.get()
    num_viewers = num_viewers_entry.get()

    if not channel_id or not num_viewers:
        status_label.config(text="Please enter both fields.", fg="red")
        return

    num_viewers = int(num_viewers)
    status_label.config(text="Viewers sent...", fg="green")
    session = httpx.AsyncClient()
    asyncio.run(start_viewbotting(session, channel_id, num_viewers))
    are_we_botting = True


def on_stop_clicked():
    global are_we_botting
    if are_we_botting:
      status_label.config(text="Stopping...", fg="red")
      send_button.config(state=tk.NORMAL)
      channel_id_entry.config(state=tk.NORMAL)
      num_viewers_entry.config(state=tk.NORMAL)
      are_we_botting = False
    else:
      status_label.config(text="Nothing to stop...", fg="red")


if __name__ == "__main__":
    create_gui()
