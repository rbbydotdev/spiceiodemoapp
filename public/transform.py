import re
import xml.etree.ElementTree as ET
import numpy as np
import argparse

def strip_namespace(tag):
    """Remove namespace from tag."""
    if '}' in tag:
        return tag.split('}', 1)[1]
    return tag

def parse_transform(transform):
    matrix = np.identity(3)
    transform_regex = re.compile(r'(\w+)\(([^)]+)\)')
    for func, values in transform_regex.findall(transform):
        values = list(map(float, values.split(',')))

        if func == 'translate':
            tx = values[0]
            ty = values[1] if len(values) > 1 else 0.0
            transform_matrix = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])

        elif func == 'scale':
            sx = values[0]
            sy = values[1] if len(values) > 1 else sx
            transform_matrix = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

        elif func == 'rotate':
            angle = values[0]
            rad = np.radians(angle)
            cos = np.cos(rad)
            sin = np.sin(rad)
            cx, cy = 0, 0
            if len(values) > 2:
                cx, cy = values[1], values[2]
            transform_matrix = np.array([[cos, -sin, cx*(1-cos) + cy*sin],
                                         [sin, cos, cy*(1-cos) - cx*sin],
                                         [0, 0, 1]])

        matrix = matrix @ transform_matrix

    return matrix

def apply_transform(coords, transform_matrix):
    transformed_coords = []
    for x, y in coords:
        vec = np.array([x, y, 1])
        transformed_vec = transform_matrix @ vec
        transformed_coords.append((transformed_vec[0], transformed_vec[1]))
    return transformed_coords

def transform_svg(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    for elem in root.iter():
        elem.tag = strip_namespace(elem.tag)  # Strip namespace from tag
        transform_attr = elem.get('transform')
        if transform_attr:
            transform_matrix = parse_transform(transform_attr)
            if elem.tag == 'rect':
                x = float(elem.get('x', '0'))
                y = float(elem.get('y', '0'))
                width = float(elem.get('width', '0'))
                height = float(elem.get('height', '0'))
                coords = [(x, y), (x + width, y), (x, y + height), (x + width, y + height)]
                transformed_coords = apply_transform(coords, transform_matrix)
                min_x = min(c[0] for c in transformed_coords)
                min_y = min(c[1] for c in transformed_coords)
                max_x = max(c[0] for c in transformed_coords)
                max_y = max(c[1] for c in transformed_coords)
                elem.set('x', str(min_x))
                elem.set('y', str(min_y))
                elem.set('width', str(max_x - min_x))
                elem.set('height', str(max_y - min_y))
            # Remove the transform attribute after applying
            del elem.attrib['transform']

    tree.write(output_file)

def main():
    parser = argparse.ArgumentParser(description='Transform SVG coordinates based on transforms')
    parser.add_argument('input_file', help='Input SVG file')
    parser.add_argument('output_file', help='Output SVG file with transformed coordinates')
    args = parser.parse_args()

    transform_svg(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
