""" UNITTESTS """
import socket
import unittest
from unittest.mock import patch
from unittests.mock_functions import mocked_socket_connect_ok, mocked_socket_connect_fail
from GenericFunctions.IsReachable import IsReachable


class Unittests(unittest.TestCase):
    """ Unittests """
    @staticmethod
    @patch('builtins.print')
    @patch.object(socket.socket, 'connect', side_effect=mocked_socket_connect_ok)
    def test_is_reachable(_mocked_socket_connect_ok, mock_print):
        """ Test if server is reachable """
        reachable = IsReachable()
        result = reachable.check()
        assert result is True
        mock_print.assert_called_with('api_server:8000 is reachable', flush=True)

    @staticmethod
    @patch('builtins.print')
    @patch('time.sleep', return_value=None)
    @patch.object(socket.socket, 'connect', side_effect=mocked_socket_connect_fail)
    def test_is_not_reachable(_mocked_socket_connect_fail, _sleep, _mock_print):
        """ Test if server is not reachable """
        reachable = IsReachable()
        result = reachable.check()
        assert result is False
        _mock_print.assert_called_with('api_server:8000 is unreachable', flush=True)
