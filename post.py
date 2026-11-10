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
        print(f"Ответ от API (создание): {result}")
    except Exception as e:
        print(f"Критическая ошибка при создании контейнера: {e}")
        return
        
    if 'id' not in result:
        print(f"❌ ОШИБКА: Не удалось создать контейнер. Полный ответ: {result}")
        return
        
    creation_id = result['id']
    print(f"✅ Контейнер создан (ID: {creation_id}). Публикуем...")
    
    publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    publish_payload = {'creation_id': creation_id, 'access_token': ACCESS_TOKEN}
    
    try:
        publish_response = requests.post(publish_url, data=publish_payload, timeout=30)
        print(f"Статус-код публикации: {publish_response.status_code}")
        print(f"Результат публикации: {publish_response.json()}")
    except Exception as e:
        print(f"Критическая ошибка при публикации: {e}")

if __name__ == "__main__":
    TEST_IMAGE_URL = "https://images.unsplash.com/photo-1554118811-1e0d58224f24?q=80&w=1000&auto=format&fit=crop"
    TEST_CAPTION = "Доброе утро! ☕️ Начинаю свой день с чашки идеального кофе. #IZVEST_AI #утро"
    post_to_instagram(TEST_IMAGE_URL, TEST_CAPTION)
