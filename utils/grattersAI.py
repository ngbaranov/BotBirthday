from openai import AsyncOpenAI
from settings import settings

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
)

async def generate_birthday_text():
    """
    Генерирует текст для поздравления с днем рождения через OpenAI.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {
                    "role": "system",
                    "content": "Ты помощник, который создает красивые и оригинальные поздравления с днем рождения на русском языке. Создавай теплые, искренние и позитивные поздравления",
                },
                {
                    "role": "user",
                    "content": "Создай поздровление с днем рождения. Поздравление должно быть теплым и позитивным."
                }
            ],
            max_tokens=500,
            temperature=0.8
        )
        generated_text = response.choices[0].message.content.strip()
        birthday_texts = [text.strip() for text in generated_text.split('|||')]
        return birthday_texts
    except Exception as e:
        # В случае ошибки возвращаем базовые поздравления
        print(f"Ошибка при генерации поздравлений: {e}")
        return [
            "🎉 Поздравляю с днем рождения! Желаю здоровья, счастья и исполнения всех желаний!",
            ]