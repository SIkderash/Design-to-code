import requests

def fetch_figma_file(file_id, token):
    headers = {"X-Figma-Token": token}
    url = f"https://api.figma.com/v1/files/{file_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_export_urls(file_id, token, node_ids):
    headers = {"X-Figma-Token": token}
    ids = ",".join(node_ids)
    url = f"https://api.figma.com/v1/images/{file_id}?ids={ids}&format=png"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['images']
