import argparse
import json
import os

full_path_to_file = None

def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('tex_file')
    args = parser.parse_args()

    if args.tex_file:
        return args.tex_file

def get_all_lines_from_file():
    all_lines = list()
    with open(full_path_to_file, 'r') as tex_file:
        line_counter = 0
        for line in tex_file:
            all_lines.append(line)
    return all_lines

def get_label_lines(label):
    label = '\label{{{}}}'.format(label)
    found_label = False
    label_lines = dict()

    with open(full_path_to_file, 'r') as tex_file:
        line_counter = 0
        for line in tex_file:
            if '\label' in line:
                if line.split()[0] == label:
                    found_label = True
                else:
                    found_label = False
            if found_label:
                label_lines[line_counter] = line
            line_counter += 1

    return label_lines

def get_proper_values(label_title):
    full_path_to_proper_values_file = '{}\{}'.format(dir_path, 'proper_values.json')
    with open(full_path_to_proper_values_file, 'r') as proper_values_file:
        full_proper_values = json.load(proper_values_file)
    proper_values = full_proper_values[label_title]

    proper_value_dictionary = dict()
    for feature_name, feature_value in proper_values.items():
        proper_value_dictionary[feature_name] = feature_value

    return proper_value_dictionary

def search_and_replace_improper_values(label_lines, proper_values):
    for line_number, line_content in label_lines.items():
        for phony_value, real_value in proper_values.items():
            if phony_value in line_content:
                line_content = line_content.replace(phony_value, real_value)
                label_lines[line_number] = line_content

def log_back_proper_values(all_lines, label_lines):
    for line_number in range(len(all_lines)):
        if label_lines.get(line_number):
            all_lines[line_number] = label_lines[line_number]

def write_proper_values_to_file(corrected_lines):
    with open(full_path_to_file, 'w') as tex_file:
        for i in range(len(corrected_lines)):
            line = corrected_lines[i]
            tex_file.write(line)

if __name__ == "__main__":
    file_name = parse_cli_args()

    if file_name:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        full_path_to_file = '{}\{}'.format(dir_path, file_name)

        all_lines = get_all_lines_from_file()

        # Get line number of header values.
        label_title = 'Heading'
        heading_label = '\label{{{}}}'.format(label_title)
        heading_lines = get_label_lines(heading_label)

        # Get a dictionary of 'improper values' mapped to their proper values, as defined by the user.
        proper_values = get_proper_values(label_title)

        # We have a dictionary of lines mapping the label to values to be replaced. Complete the replacements.
        search_and_replace_improper_values(heading_lines, proper_values)

        # Log back the real values to the list representation of the .tex document.
        log_back_proper_values(all_lines, heading_lines)

        # Write the proper values back to the tex file.
        if all_lines:
            write_proper_values_to_file(all_lines)
