import os
import requests
import datetime
import random
import urllib.parse

ACCESS_TOKEN = os.environ.get('IG_TOKEN')
IG_USER_ID = os.environ.get('IG_USER_ID')

# --- Генерация картинки с помощью Pollinations AI ---
def generate_image():
    print("🎨 Генерируем картинку с IZVEST_AI...")
    scenes = [
        "in a Parisian cafe reading a book, warm morning light",
        "walking on a rainy city street at night with neon lights",
        "in a modern art gallery, elegant outfit",
        "at a rooftop bar at sunset, stylish summer look"
    ]
    scene = random.choice(scenes)
    prompt = f"IZVEST_AI, beautiful black woman with short platinum blonde hair, heterochromia eyes, vitiligo on face and neck, {scene}, photorealistic, 8k, cinematic, highly detailed"
    
    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={random.randint(1, 999999)}"
    return image_url

# --- Генерация текста с помощью Pollinations AI ---
def generate_caption():
    print("✍️ Генерируем текст для поста...")
    prompt = "Write a short, engaging Instagram caption (in English) for a virtual influencer named IZVEST_AI. She is a beautiful black woman with vitiligo and short platinum blonde hair. Include 3-5 relevant hashtags and 1-2 emojis."
    encoded_prompt = urllib.parse.quote(prompt)
    text_url = f"https://text.pollinations.ai/{encoded_prompt}"
    
    try:
        response = requests.get(text_url, timeout=30)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Не удалось сгенерировать текст: {e}. Используем запасной вариант.")
        return "A quiet morning in Paris. ☕️ Sometimes the best luxury is a good book and a warm cup of coffee. What are you reading? #IZVEST_AI #AIInfluencer #Paris"

# --- Публикация в Instagram ---
def post_to_instagram(image_url, caption):
    print(f"--- Публикация в {datetime.datetime.now()} ---")
    
    # 1. Создаём контейнер
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {'image_url': image_url, 'caption': caption, 'access_token': ACCESS_TOKEN}
    
    try:
        response = requests.post(url, data=payload, timeout=30)
        result = response.json()
        print(f"Ответ API: {result}")
    except Exception as e:
        print(f"❌ Ошибка при создании контейнера: {e}")
        return

    if 'id' not in result:
        print("❌ Не удалось создать контейнер. Проверьте URL картинки или права токена.")
        return

    creation_id = result['id']
    print(f"✅ Контейнер создан (ID: {creation_id}). Публикуем...")

    # 2. Публикуем
    publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    publish_payload = {'creation_id': creation_id, 'access_token': ACCESS_TOKEN}
    
    try:
        publish_response = requests.post(publish_url, data=publish_payload, timeout=30)
        print(f"Результат публикации: {publish_response.json()}")
    except Exception as e:
        print(f"❌ Ошибка при публикации: {e}")

if __name__ == "__main__":
    print("🤖 Бот IZVEST_AI запущен.")
    img_url = generate_image()
    print(f"🔗 Сгенерированная картинка: {img_url}")
    
    caption_text = generate_caption()
    print(f"📝 Сгенерированный текст: {caption_text}")
    
    post_to_instagram(img_url, caption_text)
