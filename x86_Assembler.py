# Define dictionaries and lists for registers, memories, and instructions
register_values = {
    "al": "000", "ah": "100", "ax": "000", "eax": "000",
    "bl": "011", "bh": "111", "bx": "011", "ebx": "011",
    "cl": "001", "ch": "101", "cx": "001", "ecx": "001",
    "dl": "010", "dh": "110", "dx": "010", "edx": "010",
    "sp": "100", "esp": "100", "bp": "101", "ebp": "101",
    "si": "110", "esi": "110", "di": "111", "edi": "111"
}

memory_values = {
    "[al]": "000", "[ah]": "100", "[ax]": "000", "[eax]": "000",
    "[bl]": "011", "[bh]": "111", "[bx]": "011", "[ebx]": "011",
    "[cl]": "001", "[ch]": "101", "[cx]": "001", "[ecx]": "001",
    "[dl]": "010", "[dh]": "110", "[dx]": "010", "[edx]": "010",
    "[sp]": "100", "[esp]": "100", "[bp]": "101", "[ebp]": "101",
    "[si]": "110", "[esi]": "110", "[di]": "111", "[edi]": "111"
}

instruction_table_word_or_dword = {
    "add": "x01",
    "sub": "x29",
    "and": "x21",
    "or": "x09"
}

instruction_table_byte = {
    "add": "x00",
    "sub": "x28",
    "and": "x20",
    "or": "x08"
}

instruction_table_word_or_dword_memory = {
    "add": "x03",
    "sub": "x2b",
    "and": "x23",
    "or": "x0b"
}

instruction_table_byte_memory = {
    "add": "x02",
    "sub": "x2a",
    "and": "x22",
    "or": "x0a"
}

registers_8bit = ["al", "bl", "cl", "dl", "ah", "bh", "ch", "dh"]
registers_16bit = ["ax", "bx", "cx", "dx", "sp", "bp", "si", "di"]
registers_32bit = ["eax", "ebx", "ecx", "edx", "esp", "ebp", "esi", "edi"]

memories_8bit = ["[al]", "[bl]", "[cl]", "[dl]", "[ah]", "[bh]", "[ch]", "[dh]"]
memories_16bit = ["[ax]", "[bx]", "[cx]", "[dx]", "[sp]", "[bp]", "[si]", "[di]"]
memories_32bit = ["[eax]", "[ebx]", "[ecx]", "[edx]", "[esp]", "[ebp]", "[esi]", "[edi]"]


def input_elements(input_str):
    # Split input string and format it into a list
    input_list = input_str.replace(",", " ").split()
    input_list.insert(2, ",")
    final_input = []
    for item in input_list:
        if "[" in item and "]" in item:
            item = item.replace("[", "").replace("]", "")
            final_input += ["["] + [item] + ["]"]
        else:
            final_input += [item]
    if len(input_list) != 0:
        return final_input
    else:
        print("Please enter something!")
        return False


def check_errors(input_list):
    input_length = len(input_list)
    
    # Checking the syntax
    if (input_length != 4 and input_length != 6) or (input_length == 4 and input_list[2] != ",") or \
            (input_length == 6 and ((input_list[1] != "[" and input_list[3] != "[") or
                                    (input_list[3] != "]" and input_list[5] != "]") or
                                    (input_list[1] == "[" and input_list[3] != "]") or
                                    (input_list[3] == "[" and input_list[5] != "]"))):
        print("Error! Wrong syntax in instruction.")
        return True
    
    # Checking for valid instruction
    elif input_list[0] not in list(instruction_table_byte.keys()):
        print("Error! Invalid instruction.")
        return True
    
    # Checking for valid operands
    elif (input_length == 4 and (input_list[1] not in register_values.keys() or
                                 input_list[3] not in register_values.keys())) or \
            (input_length == 6 and ((input_list[1] == "[" and
                                     (input_list[2] not in register_values.keys() or
                                      input_list[5] not in register_values.keys())) or
                                    (input_list[3] == "[" and
                                     (input_list[1] not in register_values.keys() or
                                      input_list[4] not in register_values.keys())))):
        print("Error! Invalid operands.")
        return True
    
    # Checking for valid size of operands
    else:
        if input_length == 4:
            first_operand = input_list[1]
            second_operand = input_list[3]
        elif input_list[1] == "[":
            first_operand = input_list[2]
            second_operand = input_list[5]
        elif input_list[3] == "[":
            first_operand = input_list[1]
            second_operand = input_list[4]
        
        equal_size = ((first_operand in registers_8bit) == (second_operand in registers_8bit)) and \
                     ((first_operand in registers_16bit) == (second_operand in registers_16bit))
        
        if equal_size:
            return False  # Return False if there were no errors
        else:
            print("Error! Invalid size.")
            return True


def generate_prefix(instruction):
    if len(instruction):
        first_operand = instruction[1]
        second_operand = instruction[3]
    elif instruction[1] == "[":
        first_operand = instruction[2]
        second_operand = instruction[5]
    elif instruction[3] == "[":
        first_operand = instruction[1]
        second_operand = instruction[4]
    
    if (first_operand in registers_16bit) and (second_operand in registers_16bit):
        return "\\x66"
    else:
        return ""


def generate_first_byte(instruction):
    if len(instruction) == 4 and (instruction[1] in registers_16bit or instruction[1] in registers_32bit) or \
            (instruction[1] == "[" and (instruction[2] in registers_16bit or instruction[2] in registers_32bit)):
        return instruction_table_word_or_dword[instruction[0]]
    elif len(instruction) == 4 and instruction[1] in registers_8bit or \
            (instruction[1] == "[" and (instruction[2] in registers_8bit)):
        return instruction_table_byte[instruction[0]]
    elif len(instruction) == 6 and instruction[3] == "[" and (instruction[1] in registers_16bit or
                                                              instruction[1] in registers_32bit):
        return instruction_table_word_or_dword_memory[instruction[0]]
    else:
        return instruction_table_byte_memory[instruction[0]]


def generate_second_byte(instruction):
    mod = ["11", "00"]
    if len(instruction) == 4:
        return hex(int("0b" + mod[0] + register_values[instruction[3]] + register_values[instruction[1]], 2))
    elif instruction[1] == "[":
        return hex(int("0b" + mod[1] + register_values[instruction[5]] + register_values[instruction[2]], 2))
    elif instruction[3] == "[":
        return hex(int("0b" + mod[1] + register_values[instruction[1]] + register_values[instruction[4]], 2))


def assemble(instruction):
    prefix = generate_prefix(instruction)
    first_byte = generate_first_byte(instruction)
    second_byte = generate_second_byte(instruction)
    return prefix + "\\" + first_byte + "\\" + second_byte[1:]


# Get input from the user (supporting lower and uppercase letters)
input_instruction = input("Please enter your assembly code:\n").lower()
instruction_list = input_elements(input_instruction)  # Turn input into list
if instruction_list != False:
    errors_in_input = check_errors(instruction_list)
    # Check for possible errors
    if not errors_in_input:  # If there were no errors, assemble the code
        print("Your machine code:\n" + assemble(instruction_list))