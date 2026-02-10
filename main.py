from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import ThreeLineListItem, MDList
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from datetime import datetime, timedelta
import webbrowser
import urllib.parse
import sqlite3
import os

class SakkakMobile(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        # إنشاء قاعدة البيانات عند التشغيل
        self.init_db()

        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        # العنوان
        layout.add_widget(MDLabel(
            text="⚜️ السكك PREMIUM ⚜️", 
            halign="center", font_style="H5", size_hint_y=None, height=dp(60),
            text_color=self.theme_cls.primary_color
        ))

        # المدخلات
        self.name_ent = MDTextField(hint_text="اسم المشترك", icon_right="account", mode="fill")
        self.phone_ent = MDTextField(hint_text="رقم الهاتف", icon_right="phone", input_filter="int", mode="fill")
        layout.add_widget(self.name_ent)
        layout.add_widget(self.phone_ent)

        # زر الإضافة
        add_btn = MDFillRoundFlatButton(
            text="🚀 تـفعيل وحفظ",
            size_hint_x=1,
            on_release=self.add_subscriber
        )
        layout.add_widget(add_btn)

        # القائمة
        self.scroll = ScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        layout.add_widget(self.scroll)

        screen.add_widget(layout)
        
        # تحميل البيانات المحفوظة سابقاً
        self.load_data_from_db()
        
        return screen

    def init_db(self):
        # إنشاء ملف قاعدة البيانات في مسار التطبيق
        self.db_path = os.path.join(os.path.dirname(__file__), "sakkak.db")
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS subscribers 
                     (name TEXT, phone TEXT, expiry TEXT)''')
        conn.commit()
        conn.close()

    def add_subscriber(self, *args):
        name = self.name_ent.text.strip()
        phone = self.phone_ent.text.strip()
        
        if name and phone:
            expiry = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            
            # حفظ في قاعدة البيانات
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT INTO subscribers VALUES (?, ?, ?)", (name, phone, expiry))
            conn.commit()
            conn.close()

            # إضافة للقائمة في الواجهة
            self.add_item_to_list(name, phone, expiry)
            
            self.name_ent.text = ""
            self.phone_ent.text = ""

    def add_item_to_list(self, name, phone, expiry):
        item = ThreeLineListItem(
            text=f"👤 {name}",
            secondary_text=f"📞 {phone}",
            tertiary_text=f"📅 ينتهي في: {expiry}",
            on_release=self.send_whatsapp_reminder
        )
        self.list_view.add_widget(item, index=0)

    def load_data_from_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM subscribers")
        rows = c.fetchall()
        for row in rows:
            self.add_item_to_list(row[0], row[1], row[2])
        conn.close()

    def send_whatsapp_reminder(self, instance):
        phone = instance.secondary_text.replace("📞 ", "").strip()
        name = instance.text.replace("👤 ", "").strip()
        message = f"مرحباً سيد {name} 🌹\nنحيطكم علماً بأن اشتراك الإنترنت قارب على الانتهاء.\nمكتب السكك ✨"
        webbrowser.open(f"https://wa.me/964{phone}?text={urllib.parse.quote(message)}")

if __name__ == "__main__":
    SakkakMobile().run()

