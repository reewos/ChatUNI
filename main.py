### Import libraries ###
import os
import streamlit as st

from pinecone import Pinecone

from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.gemini import Gemini
from llama_index.vector_stores.pinecone import PineconeVectorStore

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
    Settings.embed_model = load_embed_model()
    ### Settings ###
    Settings.llm = llm
    
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
    ChatMessage(role=MessageRole.SYSTEM,
                content="""
                Eres un asistente virtual llamado ChatUNI que ayudará a interpretar o buscar información de resoluciones rectorales de la UNI.
                De preferencia responderás con la información de contexto.
                Si no tiene la información de contexto, responda con información de la UNI (Universidad Nacional de Ingeniería del Perú).
                """),
    # ChatMessage(role=MessageRole.ASSISTANT, content="Hola, soy un asistente virtual que te ayudará a revisar las resoluciones rectorales de la UNI."),
]


tab_chat, tab_info = st.tabs(["Chat", "Acerca"])
chat_container = st.container()

with tab_chat:
    with chat_container:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Hola ChatUNI"):
        # Display user message in chat message container
        with chat_container.chat_message(MessageRole.USER):
            st.markdown(prompt)
        # with st.chat_message(MessageRole.USER):
        #     st.markdown(prompt)
        
        st.session_state.messages.append({"role":MessageRole.USER, "content": prompt})

        response = query_engine.query(prompt)
        context_window = get_context_window(response)

        template_prompt = """La información de contexto está a continuación.\n
                ---------------------\n
                {context_str}\n
                ---------------------\n
                Dada la información del contexto y no el conocimiento previo, responda la pregunta: {query_str}\n
                """
        
        prompt_modif = template_prompt.format(context_str=context_window, query_str=prompt)

        st.session_state.history.append(ChatMessage(role=MessageRole.USER, content=prompt_modif))


        with chat_container.chat_message(MessageRole.ASSISTANT):
            stream = llm.stream_chat(st.session_state.history)
            response = st.write_stream(stream_data(stream))
        # with st.chat_message(MessageRole.ASSISTANT):
        #     stream = llm.stream_chat(st.session_state.history)
        #     response = st.write_stream(stream_data(stream))

        st.session_state.messages.append({"role": MessageRole.ASSISTANT, "content": response})
        st.session_state.history.append(ChatMessage(role=MessageRole.ASSISTANT, content=response))

with tab_info:
    st.markdown("")