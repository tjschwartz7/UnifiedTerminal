import os
import subprocess
import Config

def load_file_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()
    
def load_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def write_text_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(f"{line}\n" for line in lines)

def write_text_file(file_path, file_string):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_string)

def create_empty_file(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        pass #Create the file without writing

def print_file(lines):
    lineNum = 0
    for line in lines:
        print(f'{lineNum} {line}')

def edit(page):
    cmd = [Config.getDefaultEditor(), page]
    subprocess.run(cmd, check=True)
    
