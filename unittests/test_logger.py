import os
import logging
from unittest.mock import patch, call
from GenericFunctions.Logger import Logger


def test_logger_debug_enabled():
    debug = os.environ.get('DEBUG', '')
    os.environ['DEBUG'] = 'true'
    logger = Logger()

    with patch('builtins.print') as mocked_print:
        logger.info('info')
        assert mocked_print.call_args_list == [call('info', flush=True)]

    with patch('builtins.print') as mocked_print:
        logger.debug('debug')
        assert mocked_print.call_args_list == [call('debug', flush=True)]

    with patch('builtins.print') as mocked_print:
        logger.error('error')
        assert mocked_print.call_args_list == [call('error', flush=True)]

    os.environ['DEBUG'] = debug


def test_logger_debug_disabled():
    debug = os.environ.get('DEBUG', '')
    os.environ['DEBUG'] = 'false'

    logger = Logger()
    mock_logging = logging.getLogger('GenericFunctions.Logger')
    with patch.object(mock_logging, 'info') as mocked_log:
        logger.info('info')
        assert mocked_log.call_args_list == [call('info')]

    with patch.object(mock_logging, 'debug') as mocked_log:
        logger.debug('debug')
        assert mocked_log.call_args_list == [call('debug')]

    with patch.object(mock_logging, 'error') as mocked_log:
        logger.error('error')
        assert mocked_log.call_args_list == [call('error')]

    os.environ['DEBUG'] = debug
