from django.test import TestCase1
from sign.models import Event, Guest
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        # 不会真正地想数据库表中插入数据
        Event.objects.create(id=1, name='oneplus 3 event', status=True, limit=200, address='shenzhen', start_time='2016-08-31 02:18:22')
        Guest.objects.create(id=1, event_id=1, realname='alen', phone='13333333333', email='alen@mail.com', sign=False)

    def tearDown(self):
        pass

    def test_event_models(self):
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(realname='alen')
        self.assertEqual(result.phone, '13333333333')
        self.assertEqual(result.email, 'alen@mail.com')
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):
    """测试index登录页"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_index_page_renders_index_template(self):
        """测试index视图"""

        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):
    """测试登录动作"""

    def setUp(self):
        User.objects.create_user('user1', '912908216@qq.com', 'admin123456')

    def tearDown(self):
        pass

    def test_add_admin(self):
        """添加用户"""
        result = User.objects.get(username='user1')
        self.assertEqual(result.username, 'user1')
        # self.assertEqual(result.password, make_password('admin123456'))
        self.assertTrue(check_password('admin123456', result.password))

    def test_login_action_username_password_null(self):
        """用户名、密码为空"""
        test_data = {'username': '', 'password': ''}
        reponse = self.client.post('/login_action/', data=test_data)
        self.assertEqual(reponse.status_code, 200)
        self.assertIn(reponse.content, b'username or password is Error')

    def test_login_action_username_password_error(self):
        """用户名、密码错误"""
        test_data = {'username': 'user99', 'password': '1'}
        response = self.client.post('/login_action/', test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.content, b'username or password is Error')

    def test_login_action_success(self):
        """登录成功"""
        test_data = {'username': 'user1', 'password': 'admin123456'}
        response = self.client.post('/login_action/', test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    """发布会管理"""

    def setUp(self):
        User.objects.create_user(username='admin', password='admin123456')
        Event.objects.create(name='发布会1', limit=100, status=True, address='hangzhou'
                             , start_time='2019-06-15 0:0:0', create_time='2019-06-15 0:0:0')
        self.login_user = {'username': 'admin', 'password': 'admiin123456'}

    def tearDown(self):
        pass

    def test_event_manage_success(self):
        """测试发布会：发布会1"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('发布会1', response.content)
        self.assertEqual('beijing', response.content)

    def test_event_manage_search_success(self):
        """测试发布会搜索:发布会1"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/', {'name': '发布会1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('发布会1', response.content)
        self.assertEqual('beijing', response.content)


class GuessManagTest(TestCase):
    """嘉宾管理"""
    def setUp(self):
        User.objects.create(username='admin', password='admin123456')
        Event.objects.create(name='发布会1', limit=100, status=True, address='hangzhou'
                             , start_time='2019-06-15 0:0:0', create_time='2019-06-15 0:0:0')
        Guest.objects.create(event_id=1, realname='user1', phone='13353333333', email='xx@mail.com', sign= False, create_time='2019-06-15 0:0:0')
        self.login_user = {'username': 'admin', 'password': 'admiin123456'}

    def tearDown(self):
        pass

    def test_guest_manage_success(self):
        response = self.client.post('/login_action/', data= self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user1', response.content)
        self.assertIn('13353333333', response.content)

    def test_guess_manage_search_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_guest/', {'realname': 'user1', 'phone': '13353333333'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('user1', response.content)
        self.assertIn('13353333333', response.content)


class SignIndexAtionTest(TestCase):
    """发布会签到"""
    def setUp(self):
        User.objects.create(username='admin', password='admin123456')
        Event.objects.create(name='发布会1', limit=100, status=True, address='hangzhou'
                             , start_time='2019-06-15 0:0:0', create_time='2019-06-15 0:0:0')
        Event.objects.create(name='发布会2', limit=200, status=True, address='hangzhou'
                             , start_time='2019-06-15 0:0:0', create_time='2019-06-15 0:0:0')
        Guest.objects.create(event_id=1, realname='user1', phone='13353333333', email='xx@mail.com', sign= False, create_time='2019-06-15 0:0:0')
        Guest.objects.create(event_id=2, realname='user2', phone='13353333334', email='xx@mail.com', sign= True, create_time='2019-06-15 0:0:0')
        self.login_user = {'username': 'admin', 'password': 'admiin123456'}

    def tearDown(self):
        pass

    def test_sign_index_action_phone_null(self):
        """测试手机号为空"""
        response = self.client.post('/login_action/', self.login_user)
        response = self.client.post('/sign_index_action/1/', {'phone': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Phone error.', response.content)

    def test_sign_index_action_phone_or_event_id_Error(self):
        """测试手机号或eid错误"""
        response = self.client.post('/login_action/', self.login_user)
        response = self.client.post('/sign_index_adtion/1/', {'phone': '13353333333'} )
        self.assertEqual(response.status_code, 200)
        self.assertIn('event id or phone error.', response.content)

    def test_sign_index_action_user_has_sign_in_Error(self):
        """测试用户已签到"""
        response = self.client.post('/lohin_action/', self.login_user)
        response = self.client.post('/sign_index_action/2/',{'phone': '13353333334'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('user has sign in.', response.content)

    def test_sign_index_action_success(self):
        """测试用户签到成功"""
        response = self.client.post('/index_action/',self.login_user)
        response = self.client.post('/sign_index_action/1/', {'phone': '13353333333'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('sign in success!', response.content)
