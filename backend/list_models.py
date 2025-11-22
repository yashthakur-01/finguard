import google.generativeai as genai

genai.configure(api_key='AIzaSyClWhVqPqS79DCU4NiPT9H-hf-WTFEsfAY')

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
