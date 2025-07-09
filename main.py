import argparse, os
from code_gen import generate_code_gemini, generate_code_ollama, generate_prompt_for_screen
from figma_api import fetch_figma_file
from design_parser import extract_design_info
from utils import extract_layout_xml, save_layout_xml

def main():
    parser = argparse.ArgumentParser(description="Convert Figma file to Android code using AI")
    # parser.add_argument('--file_id', required=True, help='Figma file ID')
    # parser.add_argument('--token', required=True, help='Figma API token')
    token = ""
    file_id = ""
    parser.add_argument('--method', choices=['ollama'], required=True)
    parser.add_argument('--output-dir', default='./output')
    args = parser.parse_args()

    print("📥 Fetching design from Figma...")
    figma_json = fetch_figma_file(file_id, token)

    print("🧾 Parsing design...")
    screens, _ = extract_design_info(figma_json)

    for screen in screens:
        print(f"\n🧠 Generating layout for screen: {screen['name']}")
        prompt = generate_prompt_for_screen(screen['name'], screen['elements'])

        # code = generate_code_ollama(prompt)
        code = generate_code_gemini(prompt)

        layout_xml = extract_layout_xml(code)
        if layout_xml:
            save_layout_xml(layout_xml, args.output_dir, screen['name'])
        else:
            print(f"❌ Could not extract layout from generated code for {screen['name']}")

if __name__ == "__main__":
    main()