import os
from lxml import etree

async def compress_kml(original_file_name: str):
    print('KML PARSER: Parsing file')
    
    file_dir = './content/' + original_file_name
    try:
        tree = etree.parse(file_dir)
    except Exception as e:
        print('KML PARSER [ERROR]:', e)
        exit()
    
    root = tree.getroot()
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    document = root.find('.//kml:Document', namespaces=namespace)
    
    if document is None:
        print('KML PARSER [ERROR]: No Document tag found')
        exit()
    
    for style in document.findall('.//kml:Style', namespaces=namespace):
        style.getparent().remove(style)
    
    for style_map in document.findall('.//kml:StyleMap', namespaces=namespace):
        style_map.getparent().remove(style_map)
    
    for open_tag in document.findall('.//kml:open', namespaces=namespace):
        open_tag.getparent().remove(open_tag)
    
    for snippet in document.findall('.//kml:snippet', namespaces=namespace):
        snippet.getparent().remove(snippet)

    for style_url in document.findall('.//kml:styleUrl', namespaces=namespace):
        style_url.getparent().remove(style_url)
    

    for folder in document.findall('.//kml:Folder', namespaces=namespace):
        for feature in folder.findall('.//kml:Placemark', namespaces=namespace):
            document.append(feature)
        
        folder.getparent().remove(folder)
    
    for lookat in document.findall('.//kml:LookAt', namespaces=namespace):
        lookat.getparent().remove(lookat)
    
    if not os.path.exists('./tmp'):
        print('KML PARSER: Creating tmp directory')
        os.makedirs('./tmp')
    
    output_file_name = 'campus_compressed.kml'
    
    print('KML PARSER: Writing to file')
    tree.write(
        './tmp/' + output_file_name,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True
    )
    
    print('KML PARSER: Finished!')
    return output_file_name