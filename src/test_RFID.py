import pytest
from unittest import mock
import sys

@pytest.fixture(autouse=True)
def patch_hal_rfid_reader():
    # Patch hal.hal_rfid_reader.init() to return a mock with .read_id()
    mock_reader = mock.Mock()
    hal_mock = mock.Mock()
    hal_mock.init.return_value = mock_reader
    sys.modules['hal.hal_rfid_reader'] = hal_mock

def import_RFID():
    import importlib
    if 'RFID' in sys.modules:
        del sys.modules['RFID']
    return importlib.import_module('RFID')

def test_rfid_card_detected(capsys):
    # Patch the return value for read_id()
    sys.modules['hal.hal_rfid_reader'].init.return_value.read_id.return_value = 12345
    RFID = import_RFID()
    result = RFID.RFID_reader()
    captured = capsys.readouterr()
    assert result is True
    assert "RFID card detected! ID = 12345" in captured.out

def test_no_rfid_card_detected(capsys):
    # Patch the return value for read_id() to None
    sys.modules['hal.hal_rfid_reader'].init.return_value.read_id.return_value = None
    RFID = import_RFID()
    result = RFID.RFID_reader()
    captured = capsys.readouterr()
    assert result is False
    assert "No RFID card detected" in captured.out