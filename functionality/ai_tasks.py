import googletrans
from groq import Groq
from functionality.file_handlling import read_attr_from_settings


def translate_task(text, destination_lang):
    translator = googletrans.Translator()
    result = translator.translate(text, dest=destination_lang).text
    return result


def get_ai_results(prompt: str):
    groq_api_key = read_attr_from_settings('groq_api_key')

    client = Groq(api_key=groq_api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt + ' and return text ONLY without any other text or Double quotes.'
            },

        ],
        model="llama3-70b-8192"
    )
    return chat_completion.choices[0].message.content


def summarize_task(text, max_words):
    return get_ai_results(prompt=f'''
    Input Text:
    "{text}"
    
    Maximum Number Of Words:
    {max_words}
    
    Task:
    Please provide a summary of the input text in the same input text language with 
    Maximum of words as specified.
''')


def expand_task(text, max_words):
    return get_ai_results(prompt=f'''
    Input Text:
    "{text}"

    Maximum Number Of Expanded Approximate Line:
    {max_words}

    Task:
    Please expand the given input text by adding more details, explanations, and relevant information with same tone.
    Ensure that the expanded text are (Maximum Number Of Expanded Approximate Lines = {max_words}) 
    comprehensive and provides a deeper understanding of the topic
    and make it in the same input text language ONLY and dont insert any language to the results.
''')


def rephrase_task(text, tone):
    return get_ai_results(prompt=f'''
    User Input Text:
    {text}
    
    Desired Tone of Voice:
    {tone}
    
    AI Task:
    Rephrase the user's input text in the same Language to match the specified tone of voice 
    ''')


def check_grammar_spelling_task(text):
    return get_ai_results(prompt=f'''
    User Input Text:
    {text}
    Return Template:
    [Corrected Text]

    AI Task:
    Check And Correct The Grammar and Spelling in the same Language and Return the the correct one 
    ''')


def arrange_in_blots_task(text, max_no_blots):
    return get_ai_results(prompt=f'''
    User Input Text:
    {text}

    Max Number of Dot Blots:
    {max_no_blots}
    
    Return Template:
    • Summarized arranged text.
    • Summarized another one.
    • and so on.

    AI Task:
    Summarize and Arrange the user input text in dot blots in the same language 
    with respect of max number of Dot Blots as specified and you can make them in lower than this number as you can
    and Give me the dot blots only
    ''')


def arrange_in_steps_task(text, max_steps):
    return get_ai_results(prompt=f'''
    User Input Text:
    {text}

    Max Number of Steps:
    {max_steps}

    Return Template:
    1- arranged text.
    2- another one.
    3- and so on.

    AI Task:
    Arrange the user input text in steps in the same language 
    with respect of max number of Steps as specified and you can make them in lower than this number as you can
    and Give me the steps only
    ''')


def suitable_title_task(text, tone):
    return get_ai_results(prompt=f'''
    User Input Text:
    {text}

    Desired Tone of Voice:
    {tone}
    
    Return Template:
    [suitable title]

    AI Task:
    Extract The Suitable Title for the User Input Text 
    with respect the Desired Tone of Voice as provided
    ''')


all_tasks_functions = {
    "Translate": translate_task,
    "Summarize": summarize_task,
    "Expand": expand_task,
    "Rephrase": rephrase_task,
    "Check Grammar/Spelling": check_grammar_spelling_task,
    "Arrange In Blots": arrange_in_blots_task,
    "Arrange In Steps": arrange_in_steps_task,
    "Suitable Title": suitable_title_task,
}
