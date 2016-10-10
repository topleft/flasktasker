import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):


    ############################
    ####    fixtures        ####
    ############################

    user = dict(name="michael", email="michael@mherman.org", password="python")

    ############################
    ####    helpers         ####
    ############################

    def register(self, name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(name=name, email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def registerMichael(self):
        return self.register(self.user['name'], self.user['email'], self.user['password'], self.user['password'])

    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # each test should start with 'test'
    def test_user_setup(self):
        new_user = User(self.user['name'], self.user['email'], self.user['password'])
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t
        assert t.name == 'michael'

    def test_form_is_present(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to access your task list', response.data)

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_users_can_login(self):
        self.registerMichael()
        response = self.login(self.user['name'], self.user['password'])
        self.assertIn(b'Welcome!', response.data)

    def test_invalid_form_data(self):
        self.registerMichael()
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.', response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.registerMichael()
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.registerMichael()
        self.app.get('register/', follow_redirects=True)
        response = self.registerMichael()
        self.assertIn(
            b'That username and/or email already exist.',
            response.data
        )

if __name__ == "__main__":
    unittest.main()
