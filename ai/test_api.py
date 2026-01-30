import openai
import time

from data.json_manager import jsonManager


YANDEX_CLOUD_FOLDER = jsonManager.get_value("data/data.json", "api_yandex")["YANDEX_CLOUD_FOLDER"]
YANDEX_CLOUD_API_KEY = jsonManager.get_value("data/data.json", "api_yandex")["YANDEX_CLOUD_API_KEY"]



start = time.time()

client = openai.OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER
)

response = client.responses.create(
    prompt={
        "id": "fvttaahbt6cg539kq4k4",
    },
    input="",
)


print(response.output_text)
end = time.time()
print(f"Время выполнения: {end - start:.6f} сек.")