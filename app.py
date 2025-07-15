import streamlit as st
from openai import OpenAI

def rag_qa(client,deployment):
    system_prompt = "You are An AI assistant that helps people find information."
    messages = [{"role": "system", "content": system_prompt},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]]
    
    try:
        response = client.chat.completions.create(
            messages=messages,
            temperature=0,
            model=deployment)
        return response
    except:
        return None
    
def chatbot(client,deployment):

    if st.button("Reset Chat"):
        st.session_state.messages = []

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask here ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Generating Answer ..."):       
                response = rag_qa(client,deployment)
            try:
                answer = response.choices[0].message.content
                st.markdown(answer)
            except:
                answer = "I cant answer your question"
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

modelBase = "OpenAI"

deployment = "gpt-4.1-mini"
if deployment == "gpt-4.1-mini":
    secrets_helpers = "gpt_41_mini"

if modelBase == "OpenAI":
    endpoint = st.secrets["MODEL_SUMOPOD_ENDPOINT"]
    subscription_key =st.secrets["MODEL_SUMOPOD_KEY"]
    client = OpenAI(
        api_key=subscription_key,
        base_url=endpoint
    )

# Set page configuration
st.set_page_config(
    layout="centered",
    initial_sidebar_state="auto"
)

# Hide Streamlit menu
hide_menu = """ 
<style> 
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;};
</style> 
"""
st.markdown(hide_menu, unsafe_allow_html=True)

def main():
    chatbot(client,deployment)

if __name__ == "__main__":
    main()