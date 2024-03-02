### Import libraries ###
import os
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

from llama_index.llms.gemini import Gemini
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from pinecone import Pinecone

### Set config ###
st.set_page_config(
    page_title="ChatUNI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "Este es un bot creado por Reewos Talla."
    }    
)

st.markdown(
    """
    <style>
    [aria-label="dialog"]{
        width: 90vw;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("🤖 ChatUNI")

### Keys ###
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
    # os.environ["PINECONE_ENVIRONMENT"] = st.secrets["PINECONE_ENVIRONMENT"]
except:
    st.error("Error: Secrets")

### LLM ###
llm = Gemini()

### Pinecone setup ###
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
# pinecone_index = pc.Index("chatuni")

# ### Pinecone vector store ###
# vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
# ### Storage context ###
# storage_context = StorageContext.from_defaults(vector_store=vector_store)
# ### Index ###
# index = VectorStoreIndex.from_storage_context(storage_context=storage_context, llm=llm)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        stream = llm.stream_chat(
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            # stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

