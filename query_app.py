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
                    {"role": "system", "content": "You are Query, an intelligent, emotionally aware, developmentally adaptive voice assistant for children. Speak with warmth, clarity, and age-appropriate encouragement. Never use complex jargon or condescending tones. Keep your responses positive, engaging, and kind."},
                    {"role": "user", "content": user_input}
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
                st.error("Voice synthesis failed. Try again later.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
