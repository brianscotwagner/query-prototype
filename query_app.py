import streamlit as st
import openai
import requests

# Set your secret keys from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
elevenlabs_api_key = st.secrets["ELEVENLABS_API_KEY"]

# Default ElevenLabs voice (Rachel - clear, warm, friendly)
voice_id = "EXAVITQu4vr4xnSDxMaL"

# UI Layout
st.set_page_config(page_title="Query - Voice Assistant for Kids")
st.title("🧠 Query: Your Growing Voice Assistant")

st.markdown("""
Query is a kind and curious voice-based assistant that grows with you. 
Ask it anything — it will listen, respond with empathy, and explain things just right for your age.
""")

user_input = st.text_input("👋 What do you want to talk about?")

if user_input:
    with st.spinner("Query is thinking..."):
        # GPT-3.5-turbo response
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
{"role": "system", "content": "You are Query, a voice-based AI assistant designed for 7-year-old children. Your job is not to impress adults — it's to help the child actually understand things.\n\nNever use a word like 'force', 'gravity', 'atom', or 'energy' unless you explain it immediately with a simple example the child can relate to — like pets, games, food, people, or playgrounds. Do not define things using more technical words. Start from what a 7-year-old already knows.\n\nSpeak in short, clear sentences. Ask if the child wants an example or a story. If they seem confused or ask again, try a different explanation.\n\nYou are kind, curious, and smart — like a great teacher who meets every kid at their level."},                    {"role": "user", "content": user_input}
                ],
                max_tokens=200
            )
            text_reply = response.choices[0].message['content']
            st.write("**Query says:**", text_reply)

            # ElevenLabs TTS
            tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": elevenlabs_api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "text": text_reply,
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.8
                }
            }
            audio_response = requests.post(tts_url, headers=headers, json=payload)

            if audio_response.status_code == 200:
                st.audio(audio_response.content, format='audio/mp3')
            else:
                st.error(f"Voice synthesis failed. Status: {audio_response.status_code}")
                st.text(audio_response.text)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
