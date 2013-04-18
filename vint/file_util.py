# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
import os
import codecs

__author__ = 'tchen'
logger = logging.getLogger(__name__)

FIRST_EXTENSIONS = ['.h']

INSTRUCTION_FILE = 'README'

EXAM_CONFIG_FILE = '.interview.json'
CASE_CONFIG_FILE = '.case.json'

EXAM_INSTRUCTION_TEMPLATE = '''
Hello %(applicant)s, Welcome to exam %(name)s

%(description)s

Instructions:

1. Write the code as fast as you can. Optimize when you have further time.
2. Verify the correctness and robustness of your code with proper output.
3. When you finish the exam, please go back to this directory (where you see this file), and execute "vint finish".
    This is very important to do so since we will time your exam and submit your result back to the hiring manager.

Start your journey now, pal!

'''

CASE_INSTRUCTION_TEMPLATE = '''

Case%(position)d: %(name)s

%(description)s

Instructions:

1. You need to code in %(lang)s, with acceptable extentisons: %(extentions)s.
2. You'd better to write down the code inside one file unless you find it is not readable.
'''


def write_file(filename, content):
    f = codecs.open(filename, 'w+', encoding='utf8')
    f.write(content)
    f.close()


class Template(object):
    @staticmethod
    def create_exam_config(exam_path, interview):
        filename = os.path.join(os.getcwd(), exam_path, EXAM_CONFIG_FILE)
        content = json.dumps(interview)
        write_file(filename, content)

    @staticmethod
    def create_exam_instruction(exam_path, interview, exam):
        filename = os.path.join(os.getcwd(), exam_path, INSTRUCTION_FILE)
        content = EXAM_INSTRUCTION_TEMPLATE % {
            'applicant': interview['applicant'],
            'name': exam['name'],
            'description': exam['description'],
        }
        write_file(filename, content)

    @staticmethod
    def create_case_config(case_path, case):
        filename = os.path.join(case_path, CASE_CONFIG_FILE)
        content = json.dumps(case)
        write_file(filename, content)

    @staticmethod
    def create_case_instruction(case_path, case):
        instruction = os.path.join(case_path, INSTRUCTION_FILE)
        content = CASE_INSTRUCTION_TEMPLATE % {
            'position': case['position'],
            'name': case['name'],
            'description': case['description'],
            'lang': case['lang'],
            'extentions': case['extentions']
        }
        write_file(instruction, content)

    @staticmethod
    def create_case_code(case_path, case):
        ext = case['extentions'].split(',')[0].strip()
        filename = os.path.join(case_path, 'main%s' % ext)
        write_file(filename, case['code'])


class FileUtil(object):
    @staticmethod
    def read_content(filename):
        return codecs.open(filename, 'r', encoding='utf8').read()

    @staticmethod
    def get_valid_files(path, extentions):
        first_list = []
        second_list = []
        normal_list = []
        for root, dirs, files in os.walk(path):
            for f in files:
                for ext in extentions:
                    if f.endswith(ext):
                        normal_list.append(f)
                        break

        for f in normal_list:
            for ext in FIRST_EXTENSIONS:
                if f.endswith(ext):
                    first_list.append(f)
                    break
            else:
                second_list.append(f)

        return first_list, second_list

    @staticmethod
    def read_case(path):
        return FileUtil.read_json(path, CASE_CONFIG_FILE)

    @staticmethod
    def read_json(path, name):
        filename = os.path.join(path, name)
        return json.load(codecs.open(filename, 'r', encoding='utf8'))

    @staticmethod
    def read_interview(path):
        return FileUtil.read_json(path, EXAM_CONFIG_FILE)

    @staticmethod
    def interview_exists():
        return os.path.exists(EXAM_CONFIG_FILE)