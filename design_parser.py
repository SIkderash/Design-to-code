def extract_design_info(figma_json):
    document = figma_json['document']
    pages = document.get('children', [])
    screens = []
    image_nodes = []

    for page in pages:
        for frame in page.get('children', []):
            screen = {
                "name": frame['name'],
                "elements": []
            }
            for node in frame.get('children', []):
                el_type = node['type']
                element = {
                    "type": el_type,
                    "name": node.get('name', ''),
                    "text": node.get('characters', '')
                }
                screen["elements"].append(element)

                # Save image/vector node IDs
                if el_type in ['VECTOR', 'RECTANGLE', 'COMPONENT', 'INSTANCE']:
                    image_nodes.append(node['id'])

            screens.append(screen)

    return screens, image_nodes