#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# أداة Guessing passwords - المطور: Ahmed -Jazzy 111

import sys
import time
from datetime import datetime

class PasswordGuesser:
    def __init__(self):
        self.banner = """
        ██████╗ ██╗   ██╗███████╗███████╗███████╗██╗███╗   ██╗ ██████╗ 
        ██╔══██╗██║   ██║██╔════╝██╔════╝██╔════╝██║████╗  ██║██╔════╝ 
        ██████╔╝██║   ██║███████╗███████╗███████╗██║██╔██╗ ██║██║  ███╗
        ██╔═══╝ ██║   ██║╚════██║╚════██║╚════██║██║██║╚██╗██║██║   ██║
        ██║     ╚██████╔╝███████║███████║███████║██║██║ ╚████║╚██████╔╝
        ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                            by Ahmed -Jazzy 111
        """
        self.target_info = {
            'name': '',
            'birthdate': '',
            'partner_name': '',
            'partner_birthdate': '',
            'child_name': '',
            'child_birthdate': '',
            'pet_name': '',
            'favorite_team': '',
            'hobbies': '',
            'phone_number': '',
            'id_number': '',
            'important_years': '',
            'other_keywords': ''
        }
        self.generated_passwords = set()
        self.attempts = 0
        self.start_time = None

    def display_banner(self):
        print(self.banner)
        print("="*60)
        print("🔐 أداة توليد كلمات المرور بناءً على المعلومات الشخصية")
        print("="*60)
        print()

    def collect_target_info(self):
        print("[*] جمع المعلومات (اترك الحقل فارغاً إذا غير معروف)")
        print("-" * 50)
        
        for key in self.target_info:
            prompt = f"[?] أدخل {key.replace('_', ' ')}"
            if 'date' in key:
                prompt += " (YYYY-MM-DD): "
            else:
                prompt += ": "
            self.target_info[key] = input(prompt)
        
        print("\n✅ تم جمع المعلومات بنجاح!")
        print("-" * 50)

    def expand_variants(self, value):
        variants = [value.lower(), value.upper(), value.capitalize()]
        if len(value) > 3:
            variants.append(value[:3].lower())
            variants.append(value[-3:].lower())
        return variants

    def extract_key_elements(self):
        """استخراج العناصر المهمة لتوليد كلمات مرور"""
        elements = []
        
        for key, value in self.target_info.items():
            if not value:
                continue
            if 'name' in key or 'keyword' in key:
                for val in value.split(','):
                    elements.extend(self.expand_variants(val.strip()))

            elif 'date' in key:
                parts = value.split('-')
                if len(parts) == 3:
                    y, m, d = parts
                    elements.extend([y, y[2:], m, d, m + d, d + m])

            elif key in ['phone_number', 'id_number']:
                clean = value.replace(' ', '').replace('-', '')
                elements.extend([clean, clean[-4:]])

            elif key == 'important_years':
                for year in value.split(','):
                    y = year.strip()
                    if y:
                        elements.append(y)
                        elements.append(y[2:])

        return elements

    def generate_passwords(self, elements):
        print("\n[*] جاري توليد كلمات المرور...")

        for elem in elements:
            if 4 <= len(elem) <= 12:
                self.generated_passwords.add(elem)

        for e1 in elements:
            for e2 in elements:
                combo = e1 + e2
                if 4 <= len(combo) <= 12:
                    self.generated_passwords.add(combo)

        print(f"🔢 تم توليد [ {len(self.generated_passwords)} ] كلمة مرور")

        self.save_passwords_to_file()

    def save_passwords_to_file(self):
        """حفظ النتائج في ملف نصي"""
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"passwords_{now}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for pwd in sorted(self.generated_passwords, key=lambda x: len(x)):
                    f.write(pwd + "\n")
            print(f"📁 تم حفظ كلمات المرور في: {filename}")
        except Exception as e:
            print(f"[!] خطأ أثناء حفظ الملف: {e}")

    def simulate_attack(self):
        """محاكاة محاولة تخمين لكلمات المرور"""
        self.start_time = datetime.now()
        print(f"\n[*] بدء التجربة في {self.start_time.strftime('%H:%M:%S')}")

        for pwd in self.generated_passwords:
            self.attempts += 1
            sys.stdout.write(f"\r🔍 المحاولة {self.attempts} - تجربة: {pwd}")
            sys.stdout.flush()
            time.sleep(0.003)

        duration = (datetime.now() - self.start_time).total_seconds()
        print("\n\n✅ تم الانتهاء من المحاكاة.")
        print(f"📊 عدد المحاولات: {self.attempts}")
        print(f"⏱️ الوقت المستغرق: {duration:.2f} ثانية")

    def run(self):
        self.display_banner()
        self.collect_target_info()
        keywords = self.extract_key_elements()
        self.generate_passwords(keywords)
        self.simulate_attack()

if __name__ == "__main__":
    try:
        guesser = PasswordGuesser()
        guesser.run()
    except KeyboardInterrupt:
        print("\n❗️ تم إيقاف البرنامج يدويًا.")
        sys.exit(0)

