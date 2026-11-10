import os
import requests
import datetime
import random
import urllib.parse
import time

ACCESS_TOKEN = os.environ.get('IG_TOKEN')
IG_USER_ID = os.environ.get('IG_USER_ID')

# --- НАШ ЗОЛОТОЙ ЗАПАС КАРТИНОК ---
IMAGE_URLS = [
    "https://raw.githubusercontent.com/andreyizmestez12-design/izvest-bot/main/01a1c70c-67d4-7140-8486-3252fb0d5e29.png",
    "https://raw.githubusercontent.com/andreyizmestez12-design/izvest-bot/main/01a1c70c-f0d2-7e22-9d5f-9e73f245137e.png",
    "https://raw.githubusercontent.com/andreyizmestez12-design/izvest-bot/main/01a1c70d-9c11-7b21-a2ea-62ba8c789c6a.png",
    "https://raw.githubusercontent.com/andreyizmestez12-design/izvest-bot/main/01a1c70e-1735-7d82-b391-814a3e30ff71.png",
    "https://raw.githubusercontent.com/andreyizmestez12-design/izvest-bot/main/01a1c70e-9fb0-7402-aec2-b90030fe56b1.png",
    "https://raw.githubusercontent.com/andreyizmestez12-design/izvest-bot/main/01a1c70f-1b42-7eb2-95fd-d93bad67edcf.png",
    "https://raw.githubusercontent.com/andreyizmestez12-design/izvest-bot/main/01a1c70f-9925-7980-b1f3-ec71c7766c37.png",
    "https://raw.githubusercontent.com/andreyizmestez12-design/izvest-bot/main/01a1c710-2064-7cb2-b8e9-146e0ef67d38.png"
]

# --- Генерация текста ---
def generate_caption():
    print("✍️ Генерируем текст для поста...")
    prompt = "Write a short, engaging Instagram caption (in English) for a virtual influencer named IZVEST_AI. She is a beautiful black woman with vitiligo and short platinum blonde hair. The post is about lifestyle and fashion. Include 3-5 relevant hashtags and 1-2 emojis."
    encoded_prompt = urllib.parse.quote(prompt)
    text_url = f"https://text.pollinations.ai/{encoded_prompt}"
    
    try:
        response = requests.get(text_url, timeout=30)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Не удалось сгенерировать текст: {e}. Используем запасной.")
        return "Living my best life. ✨ #IZVEST_AI #AIInfluencer #Lifestyle"

# --- Ожидание готовности медиа-контейнера ---
def wait_for_media_ready(creation_id):
    print("⏳ Ожидаем, пока Instagram обработает картинку...")
    status_url = f"https://graph.facebook.com/v19.0/{creation_id}"
    params = {'fields': 'status_code', 'access_token': ACCESS_TOKEN}
    
    for attempt in range(1, 6):  # Максимум 5 попыток
        try:
            response = requests.get(status_url, params=params, timeout=30)
            status_data = response.json()
            
            status = status_data.get('status_code')
            print(f"   Попытка {attempt}/5, статус: {status}")
            
            if status in ('FINISHED', 'PUBLISHED'):
                print("✅ Картинка готова к публикации!")
                return True
            elif status in ('ERROR', 'EXPIRED'):
                print(f"❌ Ошибка обработки медиа. Статус: {status}")
                return False
                
        except Exception as e:
            print(f"⚠️ Ошибка при проверке статуса: {e}")
            
        time.sleep(10)  # Пауза 10 секунд между проверками
        
    print("❌ Превышено время ожидания готовности картинки.")
    return False

# --- Публикация в Instagram с повторными попытками ---
def post_to_instagram(image_url, caption):
    print(f"--- Публикация в {datetime.datetime.now()} ---")
    
    # 1. Создаём контейнер
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {'image_url': image_url, 'caption': caption, 'access_token': ACCESS_TOKEN}
    
    try:
        response = requests.post(url, data=payload, timeout=30)
        result = response.json()
        print(f"Ответ API (создание): {result}")
    except Exception as e:
        print(f"❌ Ошибка при создании контейнера: {e}")
        return

    if 'id' not in result:
        print("❌ Не удалось создать контейнер.")
        return

    creation_id = result['id']
    print(f"✅ Контейнер создан (ID: {creation_id}).")

    # 2. Ждём, пока картинка будет готова
    if not wait_for_media_ready(creation_id):
        return

    # 3. Публикуем с повторными попытками
    publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    publish_payload = {'creation_id': creation_id, 'access_token': ACCESS_TOKEN}

    for attempt in range(1, 4):  # Максимум 3 попытки
        try:
            print(f"🚀 Попытка публикации {attempt}/3...")
            publish_response = requests.post(publish_url, data=publish_payload, timeout=30)
            publish_result = publish_response.json()
            
            if 'id' in publish_result:
                print(f"🎉 УСПЕХ! Пост опубликован. Ответ: {publish_result}")
                return
            else:
                print(f"⚠️ Попытка {attempt} не удалась: {publish_result.get('error', {}).get('message', 'Неизвестная ошибка')}")
                
        except Exception as e:
            print(f"⚠️ Ошибка при публикации: {e}")
            
        if attempt < 3:
            print("   Ждём 30 секунд перед следующей попыткой...")
            time.sleep(30)
            
    print("❌ Не удалось опубликовать пост после 3 попыток.")

if __name__ == "__main__":
    print("🤖 Бот IZVEST_AI запущен.")
    random_img = random.choice(IMAGE_URLS)
    print(f"🎲 Случайно выбрана картинка: {random_img}")
    caption_text = generate_caption()
    print(f"📝 Текст: {caption_text}")
    post_to_instagram(random_img, caption_text)
