import os
from lxml import etree

def purge_kml(compressed_file_name: str):
    print('KML PURGER: Starting advanced purge process')
    
    file_dir = './tmp/' + compressed_file_name
    try:
        tree = etree.parse(file_dir)
    except Exception as e:
        print('KML PURGER [ERROR]:', e)
        exit()
    
    root = tree.getroot()
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    

    document = root.find('.//kml:Document', namespaces=namespace)
    
    if document is None:
        print('KML PURGER [ERROR]: No Document tag found')
        exit()
    
    for name_tag in document.findall('.//kml:name', namespaces=namespace):
        name_tag.getparent().remove(name_tag)
    
    invisible_features = document.findall('.//*[kml:visibility="0"]', namespaces=namespace)
    for feature in invisible_features:
        feature.getparent().remove(feature)
    
    point_features = document.findall('.//kml:Point', namespaces=namespace)
    for point in point_features:
        point.getparent().remove(point)
    
    if not os.path.exists('./tmp'):
        print('KML PURGER: Creating tmp directory')
        os.makedirs('./tmp')
    
    output_file_name = 'purged.kml'
    
    print('KML PURGER: Writing purged file')
    tree.write(
        './tmp/' + output_file_name,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True
    )
    
    print('KML PURGER: Advanced purge process completed!')