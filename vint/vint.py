# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os
from cerf_api import Cerf
from file_util import Template, FileUtil
from misc import calc_time_spent

__author__ = 'tchen'
logger = logging.getLogger(__name__)


class InterviewManager(object):

    def __init__(self, id=None):
        self.id = id
        if self.id:
            self.exam_path = 'exam%s' % self.id
        else:
            self.exam_path = None
        self.code = None
        self.interview = None
        self.exam_id = None
        self.cerf_api = None

    def generate_environment(self):
        # create exam dir
        os.mkdir(self.exam_path)

        # write .interview.json for further use
        Template.create_exam_config(os.path.join(os.getcwd(), self.exam_path), self.interview)

        # retrieve exam and write general instruction file
        exam = self.cerf_api.exam.retrieve(self.exam_id)
        if len(exam) == 0:
            print('Can not retrieve proper exam by id %s. Please contact your hiring manager.' % self.exam_id)
            exit(-1)

        Template.create_exam_instruction(self.exam_path, self.interview, exam)

        # generate cases
        for case in exam['cases']:
            self.generate_case(case)

    def generate_case(self, case):
        os.mkdir('%s/case%s' % (self.exam_path, case['position']))
        path = os.path.join(os.getcwd(), self.exam_path, 'case%s' % str(case['position']))

        # write .case.json for further use
        Template.create_case_config(path, case)

        # write instruction
        Template.create_case_instruction(path, case)

        # write code
        Template.create_case_code(path, case)

    def start(self):
        code = raw_input('Please provide your authentication code:')
        self.code = code
        self.cerf_api = Cerf(self.id, code)
        data = self.cerf_api.interview.start()
        if len(data) == 0:
            print('Can not retrieve proper interview by id %s. Please contact your hiring manager.' % self.id)
            exit(-1)

        if calc_time_spent(data['started']) > 1 or os.path.exists(self.exam_path):
            print('This interview has been started already!')
            exit(-1)

        self.interview = data
        self.exam_id = self.interview['exam']

        print('Nice to meet you, %s! Thanks for your interest in Juniper China R&D.' % data['applicant'])
        print('Creating the exam environment...'),
        self.generate_environment()
        print('Done!\nYou can "cd %s" to start your exam now.' % self.exam_path)

    def load_data(self, interview):
        self.id = interview['id']
        self.code = interview['authcode']
        self.interview = interview
        self.exam_id = interview['exam']
        self.exam_path = 'exam%d' % self.exam_id

    def submit_case(self, case):
        path = os.path.join(os.getcwd(), 'case%s' % case['position'])
        print('\tSubmit case%s...' % case['position']),
        extentions = [ext.strip() for ext in case['extentions'].split(',')]
        first_list, second_list = FileUtil.get_valid_files(path, extentions)
        content = ''
        for name in first_list + second_list:
            s = '/* %s */\n\n%s' % (name, FileUtil.read_content(os.path.join(path, name)))
            content += s

        data = {
            'interview': self.id,
            'applicant': self.interview['applicant_id'],
            'case': case['cid'],
            'content': content
        }

        if not self.cerf_api.answer.create(data):
            print('Cannot submit case%s, please contact your hiring manager.' % case['position'])
            # do not bail out so that we could try the latter cases.
            # exit(-1)
        else:
            print('Done!')

    def submit_cases(self):
        path = os.getcwd()
        for root, dirs, files in os.walk('.'):
            for d in dirs:
                if d.startswith('case'):
                    config = FileUtil.read_case(os.path.join(path, d))
                    self.submit_case(config)

    def finish_interview(self):
        data = self.cerf_api.interview.finish()
        if len(data) == 0:
            print('Can not finish interview by id %s. Please contact your hiring manager.' % self.id)
            exit(-1)

    def finish(self):
        if not FileUtil.interview_exists():
            print('Please change to the root of the exam directory, then execute this command again.')
            exit(-1)

        # do not trust existing data, retrieve interview data from server again
        interview = FileUtil.read_interview('.')
        self.cerf_api = Cerf(interview['id'], interview['authcode'])

        interview = self.cerf_api.interview.retrieve(interview['id'])
        self.load_data(interview)

        if interview['time_spent']:
            print('Your exam is over. Please stay tuned.')
            exit(-1)

        spent = calc_time_spent(interview['started'])
        print('Thank you! Your exam is done! Total time spent: %d minutes.' % spent)

        print('Submitting your code to generate report...')
        self.submit_cases()
        print('Done!')

        print('Notifying the hiring manager...'),
        self.finish_interview()
        print('Done!')

        print('Please wait for a short moment. If no one comes in 5m, please inform frontdesk.')


def main(arguments):
    is_finish = arguments['finish']
    is_start = arguments['start']
    # sanity check
    if is_finish:
        InterviewManager().finish()
    elif is_start:
        try:
            id = int(arguments['<id>'])
        except:
            print('Interview id is not valid. Please contact your hiring manager.')
            exit(-1)

        InterviewManager(id).start()
    else:
        print("Please specify a correct command.")
