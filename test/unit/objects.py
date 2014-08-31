import unittest
import mock
import onion_py
from onion_py.objects import *
from onion_py.manager import *

class FakeResponse:
    def __init__(self, code):
        self.status_code = code
        self.headers = None
        self.reason = ""
        self.url = ""

    def json(self):
        return {'relays': [], 'bridges': []}


class TestExceptions(unittest.TestCase):
    """ Test case for checking exceptions """

    def setUp(self):
        self.req = Manager()

    def test_invalid_document(self):
        with self.assertRaises(InvalidDocumentTypeError):
            self.req.query('invalid_document_type')

    def test_invalid_parameter(self):
        with self.assertRaises(InvalidParameterError):
            self.req.query('details', params={'typo': 'relay'})

    @mock.patch('onion_py.manager.requests')
    def test_onionoo_error(self, mock_requests):
        with self.assertRaises(OnionPyError):
            mock_requests.get.return_value = FakeResponse(400)
            self.req.query('details', type='node')


class TestRequest(unittest.TestCase):
    """ Test case for the Manager object """

    def setUp(self):
        self.req = Manager()

    @mock.patch('onion_py.manager.requests')
    def test_without_parameters(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        self.req.query('details')
        mock_requests.get.assert_called_with(
            self.req.OOO_URL + 'details', params={})

    @mock.patch('onion_py.manager.requests')
    def test_with_parameters(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        self.req.query(
            'details', type='relay', running='true')
        mock_requests.get.assert_called_with(
            self.req.OOO_URL + 'details',
            params={'type': 'relay', 'running': 'true'})


class TestResponseType(unittest.TestCase):
    """ Test case for checking response document types """

    def setUp(self):
        self.req = Manager()

    @mock.patch('onion_py.manager.requests')
    def test_summary_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.query('summary')
        self.assertEqual(type(resp), Summary)

    @mock.patch('onion_py.manager.requests')
    def test_details_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.query('details')
        self.assertEqual(type(resp), Details)

    @mock.patch('onion_py.manager.requests')
    def test_bandwidth_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.query('bandwidth')
        self.assertEqual(type(resp), Bandwidth)

    @mock.patch('onion_py.manager.requests')
    def test_weights_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.query('weights')
        self.assertEqual(type(resp), Weights)

    @mock.patch('onion_py.manager.requests')
    def test_clients_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.query('clients')
        self.assertEqual(type(resp), Clients)

    @mock.patch('onion_py.manager.requests')
    def test_uptime_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.query('uptime')
        self.assertEqual(type(resp), Uptime)

if __name__ == '__main__':
    unittest.main()
