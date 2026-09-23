"""Lossless bounded evidence spans. Character limits are not token limits."""
def split_block(text, limit=10000, overlap=500):
    if limit < 1 or overlap < 0 or overlap >= limit:
        raise ValueError('Require 0 <= overlap < limit')
    start = 0
    while start < len(text):
        end = min(start + limit, len(text))
        if end < len(text):
            boundary = text.rfind('\n', start + limit//2, end)
            if boundary == -1:
                boundary = text.rfind(' ', start + limit//2, end)
            if boundary > start + overlap:
                end = boundary + 1
        yield {'start':start, 'end':end, 'text':text[start:end]}
        if end == len(text):
            break
        start = end - overlap
