import unittest
import re
from app import app
from flask.testing import FlaskClient

def login_user_for_test(email:str, pwd:str , c:FlaskClient):
    rv = c.get('/login')
    m = re.search(b'(<input id="csrf_token" name="csrf_token" type="hidden" value=")([-A-Za-z.0-9]+)', rv.data)
    c.post(
        f'/login?next=%2F', 
        data=dict(
            email=email,
            password=pwd,
            csrf_token=m.group(2).decode("utf-8")
            ), 
        follow_redirects=True)

class StartSidanTestCases(unittest.TestCase):
    
    def setUp(self) -> None:
        # Here you can setup configuration for testing!
        app.config.from_object('config.ConfigTest')

    def tearDown(self) -> None:
        with app.test_client() as c:
            c.get('/logout')
   
    def test_login_start_page(self):
        with app.test_client() as c:
            # Assert login is demanded
            rv = c.get('/')
            self.assertEqual(rv.status_code, 302)

            login_user_for_test('test@example.com', 'password', c)

            # Assert login was successful
            rv = c.get('/')
            self.assertEqual(rv.status_code, 200)
            # print(rv4.data.decode('utf-8'))

            rv = c.get("/logout")
            self.assertEqual(rv.status_code, 302)
            
            rv = c.get("/")
            self.assertEqual(rv.status_code, 302)

class KontaktSidanTestCases(unittest.TestCase):
    
    def setUp(self) -> None:
        # Här kan vi sätta upp config för testet
        app.config.from_object('config.ConfigTest')

   
    def test_kontakt_form_valid_input(self):
        with app.test_client() as c:

            login_user_for_test('test@example.com', 'password', c)

            rv = c.get('/kontakt')
            self.assertEqual(rv.status_code, 200)
            self.assertIn('Kontakta Oss', rv.text)

            csrf = re.search(b'(<input id="csrf_token" name="csrf_token" type="hidden" value=")([-A-Za-z.0-9]+)', rv.data)
            rv = c.post(
                    f'/login?next=%2F', 
                    data=dict(
                        name='Kalle',
                        email='ankeborgsposten@exempel.se',
                        text='Message',
                        csrf_token=csrf.group(2).decode("utf-8")
                        ), 
                    follow_redirects=True)
            
            self.assertEqual(rv.status_code, 200)

            rv = c.get("/logout")
            self.assertEqual(rv.status_code, 302)

    def test_kontakt_form_invalid_name_input(self):
        with app.test_client() as c:

            login_user_for_test('test@example.com', 'password', c)

            # Test name less then 2 chars
            rv = c.get('/kontakt')
            self.assertEqual(rv.status_code, 200)
            self.assertIn('Kontakta Oss', rv.data.decode('utf-8'))

            csrf = re.search(b'(<input id="csrf_token" name="csrf_token" type="hidden" value=")([-A-Za-z.0-9]+)', rv.data)
            rv = c.post(
                    f'/login?next=%2F', 
                    data=dict(
                        name='',
                        email='ankeborgsposten@exempel.se',
                        text='Message',
                        csrf_token=csrf.group(2).decode("utf-8")
                        ), 
                    follow_redirects=True)
            
            self.assertNotEqual(rv.status_code,302)

            # Test name greater then 8 chars
            rv = c.get('/kontakt')
            csrf = re.search(b'(<input id="csrf_token" name="csrf_token" type="hidden" value=")([-A-Za-z.0-9]+)', rv.data)
            rv = c.post(
                    f'/login?next=%2F', 
                    data=dict(
                        name='more then eight',
                        email='ankeborgsposten@exempel.se',
                        text='Message',
                        csrf_token=csrf.group(2).decode("utf-8")
                        ), 
                    follow_redirects=True)
            
            self.assertNotEqual(rv.status_code,302)

            rv = c.get("/logout")
            self.assertEqual(rv.status_code, 302)

if __name__ == '__main__':
    unittest.main()