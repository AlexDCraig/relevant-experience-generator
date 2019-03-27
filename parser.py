import argparse
import json
import os

def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('tex_file')
    args = parser.parse_args()

    if args.tex_file:
        return args.tex_file

if __name__ == "__main__":
    file_name = parse_cli_args()

    if file_name:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        full_path_to_file = '{}\{}'.format(dir_path, file_name)

        # Get line number of header values.
        label = '\label{{{}}}'.format('Heading')
        found_header = False
        header_lines = dict()
        all_lines = list()
        with open(full_path_to_file, 'r') as tex_file:
            line_counter = 0
            for line in tex_file:
                all_lines.append(line)
                if '\label' in line:
                    if line.split()[0] == label:
                        found_header = True
                    else:
                        found_header = False
                if found_header:
                    header_lines[line_counter] = line
                line_counter += 1

        # Parse out header values that need to be replaced using proper values.
        full_path_to_json_file = '{}\{}'.format(dir_path, 'proper_values.json')
        with open(full_path_to_json_file, 'r') as proper_values_file:
            proper_values = json.load(proper_values_file)
        proper_value_dictionary = { 'firstname_lastname': proper_values['firstname_lastname'],
                                    'email_first@email_service': proper_values['email_first@email_service'],
                                    'www.linkedinprofile.com': proper_values['www.linkedinprofile.com'],
                                    'mobile_number': proper_values['mobile_number'],
                                    'github_profile': proper_values['github_profile'] }

        for line_number, line_content in header_lines.items():
            for phony_value, real_value in proper_value_dictionary.items():
                if phony_value in line_content:
                    line_content = line_content.replace(phony_value, real_value)
                    header_lines[line_number] = line_content

        # Print back the real values to the tex document.
        for line_number in range(len(all_lines)):
            if header_lines.get(line_number):
                all_lines[line_number] = header_lines[line_number]

        with open(full_path_to_file, 'w') as tex_file:
            tex_file.writelines(all_lines)
