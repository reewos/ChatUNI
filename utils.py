def stream_data(stream):
    for r in stream:
        yield r.raw['content']['parts'][0]['text'] + ""