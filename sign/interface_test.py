# coding=utf-8
import requests
import unittest


class GetEventListTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/get_event_list/'

    def tearDown(self):
        pass

    def test_get_event_null(self):
        """发布会id为空"""
        r = requests.get(self.url)
        result = r.json()

        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'parameter error')

    def test_get_event_error(self):
        """发布会id不存在"""
        r = requests.get(self.url,params={'eid': 999})
        result = r.json()

        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_event_success(self):
        """发布会id为1时，查询成功"""
        r = requests.get(self.url, params={'eid': 1})
        result = r.json()

        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], '发布会1')
        self.assertEqual(result['data']['limit'], 200)
        self.assertEqual(result['data']['address'], '浙江杭州')
        self.assertTrue(result['data']['start_time'], '2019-06-30T01:19:24')


class GetGuestListTest(unittest.TestCase):
    """查询嘉宾接口测试"""
    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/get_guest_list'

    def tearDown(self):
        pass

    def test_get_event_id_null(self):
        """eid为空"""
        r = requests.get(self.url)
        result = r.json()

        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'eid cannot be empty')

    def test_query_result_empty(self):
        """查询结果为空"""
        r = requests.get(self.url, params={'eid': 999})
        result = r.json()

        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_guest_list_success(self):
        """查询guest成功"""
        r = requests.get(self.url, params={'eid': 1, 'phone': '13353320708'})
        result = r.json()

        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['realname'], '蔡慧娜')
        self.assertEqual(result['data']['phone'], '13353320708')
        self.assertEqual(result['data']['email'], 'caihn@shinemo.com')
        self.assertTrue(result['data']['sign'])


class AddEventTest(unittest.TestCase):
    """添加发布会接口测试"""
    def setUp(self):
        pass

    def tearDown(self):
        pass


class AddGuestTest(unittest.TestCase):
    """添加嘉宾接口测试"""
    pass


class UserSignTest(unittest.TestCase):
    """签到接口测试"""
    pass


if __name__ == '__main__':
    unittest.main()