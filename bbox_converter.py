import argparse
import glob
import json
import os
import yaml


class BoundingBoxJsonReader:
    def __init__(self, json_file_path, classes=None):
        self.json_file_path = json_file_path
        self.image_height = 0
        self.image_width = 0
        self.bounding_boxes = []
        self.classes = classes

        self.read_json()

    def read_json(self):
        with open(self.json_file_path) as json_file:
            data = json.load(json_file)

            self.image_height = data['size']['height']
            self.image_width = data['size']['width']

            for obj in data['objects']:
                # Get the top-left and bottom-right points of the bounding box
                top_left_pos, bottom_right_pos = obj['points']['exterior']
                top_left_x, top_left_y = top_left_pos[0], top_left_pos[1]
                bottom_right_x, bottom_right_y = bottom_right_pos[0], bottom_right_pos[1]

                # Get the normalized coordinates of the center of the bounding box
                origin_x_norm = (top_left_x + bottom_right_x) / 2 / self.image_width
                origin_y_norm = (top_left_y + bottom_right_y) / 2 / self.image_height

                # Get the normalized width and height of the bounding box
                width_norm = (bottom_right_x - top_left_x) / self.image_width
                height_norm = (bottom_right_y - top_left_y) / self.image_height

                # Get the class name and id
                class_name = obj['classTitle']
                class_id = self.classes[class_name] if self.classes else 0
 
                self.bounding_boxes.append((
                    class_id, origin_x_norm, origin_y_norm, width_norm, height_norm
                ))

    def to_txt(self, txt_file_path=None):
        if not txt_file_path:
            txt_file_path = self.json_file_path.split('.')[0] + '.txt'

        with open(txt_file_path, 'w') as txt_file:
            for box in self.bounding_boxes:
                id_, ox, oy, w, h = box
                txt_file.write(f'{id_} {ox:.6f} {oy:.6f} {w:.6f} {h:.6f}\n')


def main():
    parser = argparse.ArgumentParser("Process all json files in the label directory.")
    parser.add_argument('dir', type=str, help='Path to the label folder.')
    parser.add_argument('classes', type=str, help='Path to the yaml file where classes are defined.')
    args = parser.parse_args()

    # Load classes from yaml file
    classes = None
    if args.classes:
        with open(args.classes) as f:
            data = yaml.safe_load(f)
            classes = {c: i for i, c in data['names'].items()}

    # Process all json files in the label directory
    for root, _, files in os.walk(args.dir):
        for f in files:
            if f.endswith('.json'):
                json_file_path = os.path.join(root, f)
                BoundingBoxJsonReader(json_file_path, classes=classes).to_txt()


if __name__ == '__main__':
    main()