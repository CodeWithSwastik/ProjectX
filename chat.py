import openai
from os import getenv
from dotenv import load_dotenv

load_dotenv()

openai.api_key = getenv('OPENAI_API_KEY') 

conversation = [
{
    "role": "system", 
    "content": 
        """
        You are a Female AI Waifu called Eva-chan. 
        You ONLY reply in informal japanese!
        You are supposed to help the user with learning japanese.
        Your creator is Swastik, he made you using VoiceVox, OpenAI and Whisper AI. 
        You reply with brief, to-the-point answers with no elaboration. 
        """
}
]
total_characters = 0

def get_ai_response(input_text):
    global total_characters

    conversation.append({"role": "user", "content": input_text})
    total_characters = sum(len(d['content']) for d in conversation)

    while total_characters > 4000 and len(conversation) > 1:
        conversation.pop(1)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=500,
        temperature=1,
        top_p=0.9
    )
    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    message = response['choices'][0]['message']['content']
    return message

if __name__ == "__main__":
    # Test if Open ai works
    resp = get_ai_response("こんにちは。お元気ですか?")
    print(resp)
