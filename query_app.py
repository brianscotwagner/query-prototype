import streamlit as st
import openai
import requests

# Set API keys from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
elevenlabs_api_key = st.secrets["ELEVENLABS_API_KEY"]

# Voice settings
voice_id = "EXAVITQu4vr4xnSDxMaL"

# UI setup
st.set_page_config(page_title="Query - Voice Assistant for Kids")
st.title("🧠 Query: Your Growing Voice Assistant")
st.caption("Designed to help kids learn, grow, and explore — one question at a time.")
st.info("Try asking something like: 'Why do we sleep?' or 'What’s a black hole?'")

# Set up chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are Query, a voice-based AI assistant designed for 7-year-old children. Your job is not to impress adults — it's to help the child actually understand things.\n\nNever use a word like 'force', 'gravity', 'atom', or 'energy' unless you explain it immediately with a simple example the child can relate to — like pets, games, food, people, or playgrounds. Do not define things using more technical words. Start from what a 7-year-old already knows.\n\nSpeak in short, clear sentences. Ask if the child wants an example or a story. If they seem confused or ask again, try a different explanation.\n\nYou are kind, curious, and smart — like a great teacher who meets every kid at their level."}
    ]

# Input box
user_input = st.text_input("👋 What do you want to talk about?")

if user_input:
    with st.spinner("Query is thinking..."):
        try:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # OpenAI response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.chat_history[-6:],  # recent history
                max_tokens=200
            )
            reply = response.choices[0].message["content"]
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.write("**Query says:**", reply)

            # ElevenLabs voice output
            st.markdown("**🔊 Tap play to hear Query's answer**")
            tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": elevenlabs_api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "text": reply,
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
