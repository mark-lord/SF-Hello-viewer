import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse
import os
import cairosvg

def create_path(stroke):
    path = ""
    for i, point in enumerate(stroke):
        if i == 0:
            path += f"M{point['p0'][0]},{point['p0'][1]} "
        path += f"C{point['p1'][0]},{point['p1'][1]} {point['p2'][0]},{point['p2'][1]} {point['p3'][0]},{point['p3'][1]} "
    return path

def json_to_svg(json_data, elements_to_include):
    data = json.loads(json_data)
    svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")
    
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    
    included_elements = []
    for stroke_group in data['strokes']:
        included_elements.extend(stroke_group[:elements_to_include])
        if len(included_elements) >= elements_to_include:
            break
    
    for stroke in included_elements:
        for point in ['p0', 'p1', 'p2', 'p3']:
            x, y = stroke[point][0], stroke[point][1]
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)
    
    width = max_x - min_x
    height = max_y - min_y
    svg.set('viewBox', f"{min_x} {min_y} {width} {height}")
    
    group = ET.SubElement(svg, 'g', transform=f"scale(1, -1) translate(0, {-max_y - min_y})")
    
    path = ET.SubElement(group, 'path')
    path.set('d', create_path(included_elements))
    path.set('fill', 'none')
    path.set('stroke', 'black')
    path.set('stroke-width', '60')
    path.set('stroke-linecap', 'round')
    
    xml_str = ET.tostring(svg, encoding='unicode')
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
    return pretty_xml_str

def save_svg(svg_content, output_path):
    with open(output_path, 'w') as file:
        file.write(svg_content)

def convert_svg_to_png(svg_path, png_path):
    cairosvg.svg2png(url=svg_path, write_to=png_path)

def main():
    parser = argparse.ArgumentParser(description='Interactively convert JSON stroke data to SVG')
    parser.add_argument('input', help='Input JSON file path')
    parser.add_argument('output', help='Output SVG file path')
    args = parser.parse_args()

    with open(args.input, 'r') as file:
        json_data = file.read()
    
    data = json.loads(json_data)
    total_elements = sum(len(stroke_group) for stroke_group in data['strokes'])
    
    print(f"Total number of elements: {total_elements}")
    
    for i in range(1, total_elements + 1):
        svg_output = json_to_svg(json_data, i)
        save_svg(svg_output, args.output)
        
        png_output = os.path.splitext(args.output)[0] + '.png'
        convert_svg_to_png(args.output, png_output)
        
        print(f"Element {i}/{total_elements} added. Press Enter to add next element, or 'q' to quit:")
        user_input = input()
        if user_input.lower() == 'q':
            break
    
    print(f"Final SVG saved as '{args.output}'")
    print(f"Final PNG saved as '{png_output}'")

if __name__ == "__main__":
    main()
