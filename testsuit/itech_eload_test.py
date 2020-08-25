# -*- encoding: utf-8 -*-
"""
@File    : itech_eload_test.py
@Time    : 2020/8/25 8:40
@Author  : blockish
@Email   : blockish@yeah.net
"""
import time
import unittest

from instrument.eloads.itech import It8500, It8500Plus, CC, CONTINUOUS, MANUAL


class It8500PlusTest(unittest.TestCase):

    dcload = It8500Plus('COM12')

    @classmethod
    def setUpClass(cls):
        cls.dcload.remote('ON')

    @classmethod
    def tearDownClass(cls):
        cls.dcload.remote('OFF')
        cls.dcload.close()

    def test_initial(self):
        self.dcload.initialize()
        self.assertTrue(self.dcload.info is not None)
        self.assertEqual(self.dcload.max_current, 30, 'max current')
        self.assertEqual(self.dcload.max_voltage, 150, 'max voltage')
        self.assertEqual(self.dcload.min_voltage, 0.1, 'min voltage')
        self.assertEqual(self.dcload.max_resistance, 7500, 'max resistance')
        self.assertEqual(self.dcload.min_resistance, 0.05, 'min_resistance')

    @unittest.skip('tested')
    def test_sn(self):
        self.dcload.sn()

    @unittest.skip('tested')
    def test_load(self):
        # self.dcload.load('ON')
        self.dcload.load('OFF')

    @unittest.skip('tested')
    def test_short(self):
        self.assertTrue(self.dcload.short('ON'))
        self.assertFalse(self.dcload.short('OFF'))

    @unittest.skip('tested')
    def test_list_mode(self):
        step1 = {'value': 1, 'time': 0.5, 'slew': 3}
        step2 = {'value': 0, 'time': 0.5, 'slew': 2}
        print(self.dcload.list_mode(CC, 30, 20, step1, step2))
        self.dcload.load('ON')
        self.dcload.trg()
        print(self.dcload.content())
        time.sleep(5)
        print(self.dcload.content())

    @unittest.skip('tested')
    def test_input_limit(self):
        self.assertEqual((150.0, 30.0, 30.0, 7500.0), self.dcload.input_limit(150, 30, 300, 7500))

    @unittest.skip('tested')
    def test_trigger_source(self):
        self.assertEqual(MANUAL, self.dcload.trigger_source(MANUAL))

    @unittest.skip('tested')
    def test_tran_mode(self):
        self.assertEqual((3.0, 0.5, 0.0, 0.1, 'continuous'), self.dcload.tran_mode(CC, 3, 0.5, 0, 0.1, CONTINUOUS))

    @unittest.skip('tested')
    def test_get_ripple(self):
        print(self.dcload.get_ripple())

    @unittest.skip('tested')
    def test_auto_range(self):
        self.assertFalse(self.dcload.auto_range('OFF'))
        self.assertTrue(self.dcload.auto_range('ON'))

    def test_auto_test_mode(self):
        pass

    @unittest.skip('tested')
    def test_curr_protection(self):
        print(self.dcload.curr_protection(enable=True))

    @unittest.skip('tested')
    def test_power_protection(self):
        print(self.dcload.power_protection())

    @unittest.skip('tested')
    def test_von_mode(self):
        print(self.dcload.von_mode())

    @unittest.skip('tested')
    def test_cr_led_mode(self):
        print(self.dcload.cr_led_mode('OFF'))

    @unittest.skip('tested')
    def test_curr_slew(self):
        """无需测试"""
        pass

    # @unittest.skip('tested')
    def test_content(self):
        # self.dcload.load('ON')
        # print(self.dcload.content())
        # time.sleep(60)
        # self.dcload.load('OFF')
        print(self.dcload.content())


if __name__ == '__main__':
    unittest.main()
