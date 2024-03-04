### Import libraries ###
import os
import streamlit as st

from pinecone import Pinecone

from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.gemini import Gemini
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.core import Settings
from llama_index.core import VectorStoreIndex

from utils import *

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
    """,
    unsafe_allow_html=True
)
st.title("🤖 ChatUNI")

### Keys ###
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
    # os.environ["PINECONE_ENVIRONMENT"] = st.secrets["PINECONE_ENVIRONMENT"]
except:
    st.error("Error: Secrets")

try:
    ### LLM ###
    llm = Gemini()
    ### Embeddings ###
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    ### Settings ###
    Settings.llm = llm
    Settings.embed_model = embed_model
except:
    st.error("Error: LLM or Embedding Model")

try:
    ### Pinecone setup ###
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    pinecone_index = pc.Index("pdfsnew")
    ### Pinecone vector store ###
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query_engine = index.as_query_engine()
except:
    st.error("Error: Pinecone")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = [
    ChatMessage(role=MessageRole.SYSTEM, content="Eres un asistente virtual que ayudará a interpretar o buscar información de resoluciones rectorales de la UNI."),
    # ChatMessage(role=MessageRole.ASSISTANT, content="Hola, soy un asistente virtual que te ayudará a revisar las resoluciones rectorales de la UNI."),
]


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


tab_chat, tab_info = st.tabs(["Chat", "Acerca"])
chat_container = st.empty()
with tab_chat:
    with chat_container:
        # React to user input
        if prompt := st.chat_input("Hola ChatUNI"):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            st.session_state.messages.append({"role":MessageRole.USER, "content": prompt})

            response = query_engine.query(prompt)
            context_window = []
            for node in response.source_nodes:
                metadata = node.metadata
                text = node.text
                context_node = {'metadata': metadata, 'text': text}
                context_window.append(context_node)

            window = str(context_window) + "\n" + str(response.response)

            template_prompt = """Context information is below.\n
                    ---------------------\n
                    {context_str}\n
                    ---------------------\n
                    Given the context information and not prior knowledge, answer the question: {query_str}\n
                    """
            
            prompt_modif = template_prompt.format(context_str=window, query_str=prompt)

            st.session_state.history.append(ChatMessage(role=MessageRole.USER, content=prompt_modif))

            with st.chat_message("assistant"):
                stream = llm.stream_chat(st.session_state.history)
                response = st.write_stream(stream_data(stream))

            st.session_state.messages.append({"role": MessageRole.ASSISTANT, "content": response})
            st.session_state.history.append(ChatMessage(role=MessageRole.ASSISTANT, content=response))

with tab_info:
    st.markdown("")