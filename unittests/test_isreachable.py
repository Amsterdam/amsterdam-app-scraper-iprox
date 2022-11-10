import socket
from unittest.mock import patch
from mock_functions import mocked_socket_connect_ok, mocked_socket_connect_fail
from GenericFunctions.IsReachable import IsReachable


@patch('builtins.print')
@patch.object(socket.socket, 'connect', side_effect=mocked_socket_connect_ok)
def test_is_reachable(mocked_socket_connect_ok, mock_print):
    reachable = IsReachable()
    result = reachable.check()
    assert result is True
    mock_print.assert_called_with('api_server:8000 is reachable', flush=True)


@patch('builtins.print')
@patch('time.sleep', return_value=None)
@patch.object(socket.socket, 'connect', side_effect=mocked_socket_connect_fail)
def test_is_not_reachable(mocked_socket_connect_fail, sleep, mock_print):
    reachable = IsReachable()
    result = reachable.check()
    assert result is False
    mock_print.assert_called_with('api_server:8000 is unreachable', flush=True)
