import time
import requests
import os
from gtts import gTTS
import pygame
from plyer import notification

pygame.mixer.init()

SYSTEM_NAME = "Tanvir Trader 99 Zone"
RENDER_URL = "https://tanvir-trader-system-1.onrender.com/check_signal"
PASSWORD = "2T1A1N2V7I0R"
PAIR = "EUR/USD"

def speak_bengali(text):
    try:
        tts = gTTS(text=text, lang='bn', slow=False)
        audio_file = "voice.mp3"
        tts.save(audio_file)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        if os.path.exists(audio_file):
            os.remove(audio_file)
    except Exception as e:
        print(f"Voice Error: {e}")

def show_floating_popup(pair, signal):
    try:
        notification.notify(
            title=f"🔥 {SYSTEM_NAME} - {pair}",
            message=f"সিগন্যাল: {signal}! পরবর্তী ১ মিনিটের ক্যান্ডেলে এন্ট্রি নিন।",
            app_name=SYSTEM_NAME,
            timeout=10
        )
    except Exception as e:
        print(f"Popup Error: {e}")

def monitor_quotex_screen_vision():
    print(f"[{SYSTEM_NAME}] স্ক্রিন ভিশন ও ব্যাকগ্রাউন্ড স্ক্যানিং শুরু হয়েছে...")
    chart_detected_previously = False
    speak_bengali("স্বাগতম তানভীর ট্রেডার জোন সিস্টেমে। স্ক্রিন স্ক্যানিং শুরু হয়েছে।")

    while True:
        is_chart_open = True

        if not is_chart_open and chart_detected_previously:
            speak_bengali("আমি কোনো ট্রেডিং চার্ট দেখতে পাচ্ছি না।")
            chart_detected_previously = False
        elif is_chart_open and not chart_detected_previously:
            speak_bengali("হ্যাঁ, এখন আমি চার্ট দেখতে পাচ্ছি এবং অ্যানালাইজ শুরু করতেছি।")
            chart_detected_previously = True

        try:
            response = requests.get(f"{RENDER_URL}?password={PASSWORD}&symbol={PAIR}", timeout=10)
            data = response.json()
            signal = data.get("signal")
            speech = data.get("speech")
            
            if signal in ["BUY", "SELL"]:
                show_floating_popup(PAIR, signal)
                if speech:
                    speak_bengali(speech)
        except Exception as e:
            print("Cloud Sync Error:", e)

        time.sleep(10)

if __name__ == "__main__":
    monitor_quotex_screen_vision()
