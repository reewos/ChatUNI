import streamlit as st
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

@st.cache(allow_output_mutation=True)
def load_embed_model():
    return HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def stream_data(stream):
    for r in stream:
        yield r.raw['content']['parts'][0]['text'] + ""

def get_context_window(response):
    context_window = []
    for node in response.source_nodes:
        metadata = node.metadata
        text = node.text
        context_node = {'metadata': metadata, 'text': text}
        context_window.append(context_node)

    window_with_default_response = str(context_window) + "\n" + str(response.response)
    return window_with_default_response