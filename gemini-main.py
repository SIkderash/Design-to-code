import os
import argparse
import requests
from figma_api import fetch_figma_file, fetch_export_urls
from layoutgenerator import generate_layout_from_image
from utils import save_layout_xml, extract_valid_xml

def download_image(url, output_path):
    img = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(img.content)

def main():
    parser = argparse.ArgumentParser()
    token = ""
    file_id = ""
    parser.add_argument("--output_dir", default="./output")
    args = parser.parse_args()

    print("📥 Fetching Figma file...")
    figma_json = fetch_figma_file(file_id, token)

    frames = []
    for page in figma_json['document']['children']:
        for node in page['children']:
            if node['type'] == 'FRAME':
                frames.append({"name": node['name'], "id": node['id']})

    print(f"🖼 Found {len(frames)} screens...")
    node_ids = [f['id'] for f in frames]
    image_urls = fetch_export_urls(file_id, token, node_ids)

    for screen in frames:
        print(f"📸 Downloading: {screen['name']}")
        url = image_urls[screen['id']]
        img_path = os.path.join(args.output_dir, screen['name'] + ".png")
        download_image(url, img_path)

        print(f"🤖 Generating layout for {screen['name']}...")
        raw_xml = generate_layout_from_image(img_path, screen['name'])
        xml = extract_valid_xml(raw_xml)
        save_layout_xml(xml, args.output_dir, screen['name'])

if __name__ == "__main__":
    main()
