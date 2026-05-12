import csv
import json
import os
import time

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

results = []

with open("reviews.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        review = row["review"]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Определи:
                    1. Тональность отзыва (positive / negative / neutral)
                    2. Основную тему

                    Верни ответ строго в JSON формате:

                    {{
                    "sentiment": "...",
                    "topic": "..."
                    }}

                    Отзыв:
                    {review}
                    """,
                }
            ],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        try:
            parsed = json.loads(content)

            results.append(
                {
                    "id": row["id"],
                    "review": review,
                    "sentiment": parsed["sentiment"],
                    "topic": parsed["topic"],
                }
            )

            print(f"Обработан: {review}")

        except Exception as e:
            print(f"Ошибка: {review}")
            print(content)

with open("results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=2)

print("Готово!")
