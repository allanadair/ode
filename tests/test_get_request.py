#!/usr/bin/env python
"""
tests
"""
import json
import ode
import unittest


class GetRequestTestCase(unittest.TestCase):
    def setUp(self):
        ode.app.config['TESTING'] = True
        self.app = ode.app.test_client()

    def test_get_request(self):
        response = self.app.get('/listings?min_bath=3&min_bed=5&min_price=280000',
                                follow_redirects=True)
        json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()
