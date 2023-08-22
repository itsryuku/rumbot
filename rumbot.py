#!/usr/bin/env python
"""
Author: Ryuku - https://ryukudz.com
"""
import httpx
import random
import string
import asyncio
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from stylesheet import Stylesheets

are_we_botting = False
class RumbotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Rumbot")
        self.setFixedSize(300, 150)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        app_icon = QIcon("./img/sigma.jpg")
        self.setWindowIcon(app_icon)

        container_frame = QFrame(self)
        container_frame.setStyleSheet("background-color: #1A1A1A; border-radius: 10px; padding: 3px;")
        self.setCentralWidget(container_frame)

        layout = QVBoxLayout(container_frame)

        form_layout = QFormLayout()
        input_style = Stylesheets.input_style()
        label_style = Stylesheets.label_style()
        noti_style = Stylesheets.noti_style()

        self.channel_id_label = QLabel("Video ID:")
        self.channel_id_label.setStyleSheet(label_style)
        self.channel_id_entry = QLineEdit()
        self.channel_id_entry.setStyleSheet(input_style)
        form_layout.addRow(self.channel_id_label, self.channel_id_entry)

        self.num_viewers_label = QLabel("Number of Bots:")
        self.num_viewers_label.setStyleSheet(label_style)
        self.num_viewers_entry = QLineEdit()
        self.num_viewers_entry.setStyleSheet(input_style)
        form_layout.addRow(self.num_viewers_label, self.num_viewers_entry)

        layout.addLayout(form_layout)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(noti_style)
        layout.addWidget(self.status_label)

        button_layout = QHBoxLayout()
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet(Stylesheets.button_style())
        self.send_button.clicked.connect(self.on_send_clicked)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.on_stop_clicked)
        self.stop_button.setStyleSheet(Stylesheets.button_style())
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

    def on_send_clicked(self):
        global are_we_botting
        channel_id = self.channel_id_entry.text()
        num_viewers = self.num_viewers_entry.text()

        if not channel_id or not num_viewers:
            self.show_status_message("Please enter both fields.", "red")
            return

        num_viewers = int(num_viewers)
        self.show_status_message("Viewers sent...", "green")
        session = httpx.AsyncClient()
        asyncio.run(self.start_viewbotting(session, channel_id, num_viewers))
        are_we_botting = True

    def on_stop_clicked(self):
        global are_we_botting
        if are_we_botting:
            self.show_status_message("Stopped...", "red")
            self.enable_ui_elements(True)
            are_we_botting = False
        else:
            self.show_status_message("Nothing to stop...", "red")

    async def start_viewbotting(self, session, channel_id, num_viewers):
        url = f"https://wn0.rumble.com/service.php?video_id={channel_id}&name=video.watching-now"
        response = await session.get(url)
        if "data" not in response.json():
            self.show_status_message("Channel doesn't exist.", "red")
            return False

        url = "https://wn0.rumble.com/service.php?name=video.watching-now"
        tasks = []
        for _ in range(num_viewers):
            viewer_id = self.generate_viewer_id()
            data = {"video_id": channel_id, "viewer_id": viewer_id}
            task = session.post(url, data=data)
            tasks.append(task)

        await asyncio.gather(*tasks)
        self.enable_ui_elements(False)

        return True

    def generate_viewer_id(self):
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(8))

    def show_status_message(self, message, color):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-family: Lato; font-size: 13px; font-style: italic;")

    def enable_ui_elements(self, enable):
        self.channel_id_entry.setDisabled(not enable)
        self.num_viewers_entry.setDisabled(not enable)
        self.send_button.setDisabled(not enable)

if __name__ == "__main__":
    app = QApplication([])
    mainWin = RumbotApp()
    mainWin.show()
    app.exec()
