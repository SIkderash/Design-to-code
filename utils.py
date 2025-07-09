import os
import re

import requests

import re

import os
import re

def extract_valid_xml(text):
    match = re.search(r"<\\?xml.*?</.*?Layout>", text, re.DOTALL)
    return match.group(0) if match else text.strip()

def save_layout_xml(xml, output_dir, name):
    os.makedirs(output_dir, exist_ok=True)
    fname = name.lower().replace(" ", "_") + ".xml"
    path = os.path.join(output_dir, fname)
    with open(path, "w") as f:
        f.write(xml)
    print(f"✅ Saved: {path}")


def extract_layout_xml(code):
    layout_patterns = [
        r"<\?xml.*?</ConstraintLayout\s*>",
        r"<\?xml.*?</LinearLayout\s*>",
        r"<\?xml.*?</RelativeLayout\s*>",
        r"<\?xml.*?</FrameLayout\s*>",
        r"<\?xml.*?</androidx.constraintlayout.widget.ConstraintLayout\s*>"
    ]

    for pattern in layout_patterns:
        match = re.search(pattern, code, re.DOTALL)
        if match:
            return match.group(0)

    # fallback: match any layout
    fallback_match = re.search(r"<([a-zA-Z0-9.]+Layout)[\s\S]*?</\1>", code)
    if fallback_match:
        content = fallback_match.group(0)
        if not content.strip().startswith("<?xml"):
            content = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" + content
        return content

    return None


def save_layout_xml(xml_code, output_dir, screen_name):
    layout_dir = os.path.join(output_dir, 'res', 'layout')
    os.makedirs(layout_dir, exist_ok=True)

    file_name = f"layout_{screen_name.lower().replace(' ', '_')}.xml"
    path = os.path.join(layout_dir, file_name)

    with open(path, 'w') as f:
        f.write(xml_code)

    print(f"✅ Saved layout: {path}")



def download_assets(image_urls, output_dir):
    drawable_dir = os.path.join(output_dir, 'res', 'drawable')
    os.makedirs(drawable_dir, exist_ok=True)
    
    for node_id, url in image_urls.items():
        resp = requests.get(url)
        filename = f"{node_id}.png"
        with open(os.path.join(drawable_dir, filename), 'wb') as f:
            f.write(resp.content)
        print(f"🖼️ Saved asset: {filename}")



