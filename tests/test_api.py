#!/usr/bin/env python
import unittest

import sys
sys.path.append('../')
from vint.cerf_api import Interview, Exam, Answer


class CerfInterviewSuite(unittest.TestCase):
    def setUp(self):
        self.id = 1
        self.authcode = 'KZZ2NG'
        self.interview = Interview(self.authcode, self.id)

    def tearDown(self):
        self.interview.reset()
        pass

    def test_interview_retrieve(self):
        data = self.interview.retrieve(self.id)
        self.assertTrue(data)
        self.assertEqual(data['id'], self.id)
        self.assertEqual(data['authcode'], self.authcode)

    def test_interview_start_stop(self):
        self.interview.reset()
        data = self.interview.start()
        self.assertTrue(data['started'])
        self.assertFalse(data['time_spent'])
        data = self.interview.finish()
        self.assertEqual(data['time_spent'], 1)


class CerfExamSuite(unittest.TestCase):
    def setUp(self):
        self.id = 1
        self.exam_id = 1
        self.authcode = 'KZZ2NG'
        self.exam = Exam(self.authcode)

    def tearDown(self):
        pass

    def test_exam_retrieve(self):
        data = self.exam.retrieve(self.exam_id)
        self.assertTrue(data)
        self.assertTrue(data['name'])
        self.assertTrue(data['cases'])


class CerfAnswerSuite(unittest.TestCase):
    def setUp(self):
        self.data = {
            'interview': 1,
            'author': 2,
            'case': 1,
            'content': 'Hello world'
        }
        self.answer_id = None
        self.authcode = 'KZZ2NG'
        self.answer = Answer(self.authcode)

    def tearDown(self):
        if self.answer_id:
            self.answer.delete(self.answer_id)

    def test_answer_submit(self):
        answer = self.answer.create(self.data)
        self.assertTrue(answer)
        self.answer_id = answer['id']

        self.assertEqual(answer['interview'], self.data['interview'])
        self.assertEqual(answer['author'], self.data['author'])
        self.assertEqual(answer['case'], self.data['case'])
        self.assertEqual(answer['content'], self.data['content'])



unittest.main()