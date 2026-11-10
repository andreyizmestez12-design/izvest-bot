import os
import requests
import datetime
import random
import urllib.parse

ACCESS_TOKEN = os.environ.get('IG_TOKEN')
IG_USER_ID = os.environ.get('IG_USER_ID')

# --- НАШ ЗОЛОТОЙ ЗАПАС КАРТИНОК (прямые raw-ссылки) ---
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

# --- Генерация текста (нейросеть придумает уникальную подпись) ---
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

# --- Публикация в Instagram ---
def post_to_instagram(image_url, caption):
    print(f"--- Публикация в {datetime.datetime.now()} ---")
    
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {'image_url': image_url, 'caption': caption, 'access_token': ACCESS_TOKEN}
    
    try:
        response = requests.post(url, data=payload, timeout=30)
        result = response.json()
        print(f"Ответ API: {result}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return

    if 'id' not in result:
        print("❌ Не удалось создать контейнер. Проверь ссылку на картинку или токен.")
        return

    creation_id = result['id']
    print(f"✅ Контейнер создан (ID: {creation_id}). Публикуем...")

    publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    publish_payload = {'creation_id': creation_id, 'access_token': ACCESS_TOKEN}
    
    try:
        publish_response = requests.post(publish_url, data=publish_payload, timeout=30)
        print(f"Результат публикации: {publish_response.json()}")
    except Exception as e:
        print(f"❌ Ошибка при публикации: {e}")

if __name__ == "__main__":
    print("🤖 Бот IZVEST_AI запущен.")
    
    # Выбираем случайную картинку из золотого запаса
    random_img = random.choice(IMAGE_URLS)
    print(f"🎲 Случайно выбрана картинка: {random_img}")
    
    # Генерируем текст
    caption_text = generate_caption()
    print(f"📝 Текст: {caption_text}")
    
    # Постим
    post_to_instagram(random_img, caption_text)
