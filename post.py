import os
import requests
import datetime

ACCESS_TOKEN = os.environ.get('IG_TOKEN')
IG_USER_ID = os.environ.get('IG_USER_ID')

def post_to_instagram(image_url, caption):
    print(f"--- Попытка публикации в {datetime.datetime.now()} ---")
    
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {'image_url': image_url, 'caption': caption, 'access_token': ACCESS_TOKEN}
    
    try:
        response = requests.post(url, data=payload, timeout=30)
        print(f"Статус-код создания контейнера: {response.status_code}")
        result = response.json()
        print(f"Ответ от API: {result}")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        return
        
    if 'id' not in result:
        print(f"❌ ОШИБКА: Не удалось создать контейнер. Проверь ссылку на картинку.")
        return
        
    creation_id = result['id']
    print(f"✅ Контейнер создан (ID: {creation_id}). Публикуем...")
    
    publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    publish_payload = {'creation_id': creation_id, 'access_token': ACCESS_TOKEN}
    
    try:
        publish_response = requests.post(publish_url, data=publish_payload, timeout=30)
        print(f"Результат публикации: {publish_response.json()}")
    except Exception as e:
        print(f"Критическая ошибка при публикации: {e}")

if __name__ == "__main__":
    # Ссылка на картинку с твоей IZVEST_AI
    IMAGE_URL = "https://raw.githubusercontent.com/andreyizmestez12-design/izvest-bot/main/01a1c6bd-8494-7cf0-a9fb-7769a45cf43d.png"
    
    # Текст поста
    CAPTION = "Тихое парижское утро. ☕️📖 Иногда лучшая роскошь — это хорошая книга и чашка кофе. Что читаете вы? #IZVEST_AI #AIInfluencer #Paris"
    
    post_to_instagram(IMAGE_URL, CAPTION)
