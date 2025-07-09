import openai
import torch
# from transformers import pipeline
import ollama
import google.generativeai as genai

# def generate_prompt_for_screen(screen):
#     return f"Generate Android XML layout and Java code for a screen called '{screen['name']}' with the following UI elements: {screen['elements']}"

def generate_prompt_for_screen(screen_name, elements):
    lines = [
        "You are an expert Android developer.",
        "Generate ONLY an Android layout XML for the screen below.",
        "Use ConstraintLayout as the root layout.",
        "Ensure all tags are properly closed and XML is valid.",
        "Add android:id to each element.",
        "Use placeholder image for any icons or images: android:src=\"@drawable/placeholder\".",
        "Include the XML declaration line: <?xml version=\"1.0\" encoding=\"utf-8\"?>",
        "Do NOT include Java or Kotlin code.",
        "",
        f"Screen name: {screen_name}",
        "UI Elements:"
    ]

    for el in elements:
        line = f"- {el['type']}: {el['name']}"
        if 'text' in el:
            line += f", text: '{el['text']}'"
        if 'hint' in el:
            line += f", hint: '{el['hint']}'"
        lines.append(line)

    lines.append("\nOnly output the full XML layout. No explanation.")

    return "\n".join(lines)


def generate_code_openai(prompt, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert Android developer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def generate_code_ollama(prompt, model_name="qwen2.5-coder"):
    print("🔄 Querying Ollama model locally...")
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an expert Android developer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content']

def generate_code_gemini(prompt):
    genai.configure(api_key="")
    models = genai.list_models()
    # for m in models:
    #     print(m.name)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text