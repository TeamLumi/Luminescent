import os
import re
import json

directory_path = os.path.join(os.getcwd(), 'scripts')
filenames = [filename for filename in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, filename))]

item_event_keyword = "_CHG_COMMON_SCR('ev_item_event_keywait')"
parameter_regex = r'\([^,]*,\s*(.*?)\)'
item_data = {}

special_cases = {
    'ev_d26r0104_item_event_ok': 1,
    'ev_turearuki_poke_item_get': 0,
    'ev_tower_gate_talk_prize_get': [],
    'ev_tower_gate_return_prize_get': [],
    'ev_tower_gate_prize_get': [],
    'ev_tower_gate_prize_get_10_loop': [],
    'ev_tower_gate_prize_get_20': [],
    'ev_d01r0102_leader_01_stone': [80, 81, 82, 83, 84, 85, 849],
    'ev_r221r0101_item_add': [149, 150, 151, 152, 153, 154, 155, 156, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 157, 158, 169, 170, 171, 172, 173, 174]
}

ldval_map = {
    'ev_c01r0201_kuji_no_4': '_LDVAL(@SCWK_PARAM3,',
    'ev_c01r0201_kuji_no_3': '_LDVAL(@SCWK_PARAM3,',
    'ev_c01r0201_kuji_no_2': '_LDVAL(@SCWK_PARAM3,',
    'ev_c01r0201_kuji_no_1': '_LDVAL(@SCWK_PARAM3,',
    'ev_c01r0201_kuji_no_0': '_LDVAL(@SCWK_PARAM3,',
    'common_vm_03': '_LDVAL(@SCWK_PARAM1,',
    'ev_c10r0101_tm_handler_common_no_flag': '_LDVAL(@SCWK_TEMP0,',
    'ev_c10r0101_tm_handler_common': '_LDVAL(@SCWK_TEMP0,',
    'ev_c01r0201_kuji_item_get_chk': '_LDWK(@SCWK_TEMP0,',
    'ev_turearuki_poke_item_get': '_LDVAL(@SCWK_TEMP0,',
    'ev_tower_gate_prize_get_common': '_LDWK(@SCWK_TEMP0,',
    'r209_fishing1_yes': '_LDVAL(@SCWK_TEMP0,',
    'r218r0101_fishing_yes': '_LDVAL(@SCWK_TEMP0,',
    'ev_item_fanatic_give_item': '_LDVAL(@SCWK_TEMP0,',
    'ev_item_fanatic_give_item_two': '_LDVAL(@SCWK_TEMP0,'
}

def get_indices(file_lines, command):
    return [index for index, value in enumerate(file_lines) if value == command]

def remove_after_semicolon(input_string):
    result_string = input_string.split(';')[0]
    return result_string.strip()

def find_jumped_value(function_name, file_lines, ldval_command):
    indices = get_indices(file_lines, f"_JUMP('{function_name[:-1]}')")
    item_ids = []
    if len(indices) == 0:
        indices = get_indices(file_lines, f"_CALL('{function_name[:-1]}')")
    if len(indices) == 0:
        if function_name[:-1] in special_cases.keys():
            return special_cases[function_name[:-1]]
        raise Exception(function_name)
    for index in indices:
        command_start_index = find_closest_previous_index(file_lines, index, ':')
        ldval_map_command = 0
        if file_lines[command_start_index][:-1] in ldval_map.keys():
            ldval_map_command = ldval_map[file_lines[command_start_index][:-1]]
        else:
            ldval_map_command = ldval_command
        print(file_lines[command_start_index][:-1])
        item_ids.append(extract_item_id(command_start_index, index, file_lines, ldval_map_command))
    return item_ids

def get_normal_item_id(item_id_command):
    match = re.search(r'\b\d+\b', item_id_command)
    if match:
        return int(match.group())
    raise Exception(item_id_command)

def extract_item_id(command_start_index, ldval_index, file_lines, ldval_command):
    item_ids = []
    extracted_lines = file_lines[command_start_index:ldval_index + 1]
    item_id_commands = [remove_after_semicolon(value) for index, value in enumerate(extracted_lines) if value.startswith(ldval_command)]
    if extracted_lines[0][:-1] in special_cases.keys():
        return special_cases[extracted_lines[0][:-1]]
    if len(item_id_commands) == 0:
        ldval_map_command = ldval_map[extracted_lines[0][:-1]]
        item_ids.append(find_jumped_value(extracted_lines[0], file_lines, ldval_map_command))
    for item_id_command in item_id_commands:
        counted_chars = item_id_command.count('@')
        if counted_chars == 1:
            item_ids.append(get_normal_item_id(item_id_command))
        elif counted_chars == 2:
            work_value = re.search(parameter_regex, item_id_command).group(1)
            ldval_command = f"_LDVAL({work_value},"
            item_ids.append(find_jumped_value(extracted_lines[0], file_lines, ldval_command))
        else:
            print('Whoops')

    return item_ids

def find_closest_previous_index(array, start_index, target_character):
    for i in range(start_index - 1, -1, -1):
        if target_character in array[i]:
            return i
    return None

def find_item_id(file_lines, room_name):
    item_ids = []
    item_event_keyword_indices = [index for index, value in enumerate(file_lines) if value == item_event_keyword]
    for ldval_index in item_event_keyword_indices:
        command_start_index = find_closest_previous_index(file_lines, ldval_index, ':')
        item_ids.append(extract_item_id(command_start_index, ldval_index, file_lines, '_LDVAL(@SCWK_TEMP0'))
    return item_ids

for filename in filenames:
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_data = file.read()
            room_name = filename.replace('.ev', '')
            data_lines = file_data.split('\n')
            file_lines = [s.strip() for s in data_lines]
            items = find_item_id(file_lines, room_name)
            if len(items) > 0:
                item_data[room_name] = items

file_path = "item_map.json"

with open(file_path, 'w') as json_file:
    json.dump(item_data, json_file, indent=4)