

def translate_task(text: str, destination_lang: str):
    from deep_translator import GoogleTranslator

    result = GoogleTranslator(
        source='auto',
        target=destination_lang).translate(text)
    return result


def get_ai_results(prompt: str):
    from functionality.file_handlling import read_attr_from_settings
    from groq import Groq

    groq_api_key = read_attr_from_settings('groq_api_key')

    client = Groq(api_key=groq_api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt + '\n and return text ONLY without any other text or Double quotes.'
            },

        ],
        model="llama3-70b-8192"
    )
    return chat_completion.choices[0].message.content

