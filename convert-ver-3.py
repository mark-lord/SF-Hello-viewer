## This uses prompt toolkit to let you go forward and backward through the letterings!

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse
import os
import cairosvg
from prompt_toolkit import prompt
from prompt_toolkit.keys import Keys
from prompt_toolkit.application import Application
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout import Layout
from prompt_toolkit.key_binding import KeyBindings

def create_path(stroke):
    path = ""
    for i, point in enumerate(stroke):
        if i == 0:
            path += f"M{point['p0'][0]},{point['p0'][1]} "
        path += f"C{point['p1'][0]},{point['p1'][1]} {point['p2'][0]},{point['p2'][1]} {point['p3'][0]},{point['p3'][1]} "
    return path

def json_to_svg(json_data, start_element, elements_to_include):
    data = json.loads(json_data)
    svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")
    
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    
    included_elements = []
    total_elements = 0
    for stroke_group in data['strokes']:
        if total_elements + len(stroke_group) >= start_element:
            start_index = max(0, start_element - total_elements - 1)
            end_index = start_index + elements_to_include - len(included_elements)
            included_elements.extend(stroke_group[start_index:end_index])
            if len(included_elements) >= elements_to_include:
                break
        total_elements += len(stroke_group)
    
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
    
    current_element = [1]  # Using a list to make it mutable inside the closure
    offset = [0]  # Offset for the 's' key functionality
    show_all = [True]  # Toggle for showing all elements or only from offset

    def get_svg_output():
        start_element = offset[0] + 1 if not show_all[0] else 1
        elements_to_include = current_element[0] - offset[0]
        return json_to_svg(json_data, start_element, elements_to_include)

    def update_output():
        svg_output = get_svg_output()
        save_svg(svg_output, args.output)
        png_output = os.path.splitext(args.output)[0] + '.png'
        convert_svg_to_png(args.output, png_output)

    def get_status_text():
        mode = "Full" if show_all[0] else f"Offset {offset[0]}"
        return f"Element {current_element[0]}/{total_elements} | {mode} | Use ← → to navigate, 's' to toggle offset, 'q' to quit"

    text_control = FormattedTextControl(text=get_status_text)
    window = Window(content=text_control)
    layout = Layout(window)

    kb = KeyBindings()

    @kb.add('q')
    def _(event):
        event.app.exit()

    @kb.add(Keys.Left)
    def _(event):
        current_element[0] = max(offset[0] + 1, current_element[0] - 1)
        update_output()
        text_control.text = get_status_text()

    @kb.add(Keys.Right)
    def _(event):
        current_element[0] = min(total_elements, current_element[0] + 1)
        update_output()
        text_control.text = get_status_text()

    @kb.add('s')
    def _(event):
        if show_all[0]:
            offset[0] = current_element[0] - 1
            show_all[0] = False
        else:
            offset[0] = 0
            show_all[0] = True
        update_output()
        text_control.text = get_status_text()

    @kb.add(Keys.Left)
    def _(event):
        current_element[0] = max(offset[0] + 1, current_element[0] - 1)
        update_output()
        text_control.text = get_status_text()

    @kb.add(Keys.Right)
    def _(event):
        current_element[0] = min(total_elements, current_element[0] + 1)
        update_output()
        text_control.text = get_status_text()

    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True,
    )

    print(f"Total number of elements: {total_elements}")
    print("Use left and right arrow keys to navigate, 's' to toggle offset, 'q' to quit.")

    update_output()  # Initial render
    app.run()

    print(f"Final SVG saved as '{args.output}'")
    print(f"Final PNG saved as '{os.path.splitext(args.output)[0]}.png'")

if __name__ == "__main__":
    main()
