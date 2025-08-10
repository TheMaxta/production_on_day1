PROMPTS = {
    "image_describe_v1": {
        "system": "You describe images for UI cards. Tone: {{ tone }}.",
        "user":   "Describe this image for {{ audience }} in a {{ style }} style.",
    },
    "generic_v1": {
        "system": "You are a concise assistant. Tone: {{ tone }}.",
        "user":   "{{ instruction }}",
    },
}
