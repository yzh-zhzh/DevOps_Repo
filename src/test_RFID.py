import pytest
from unittest import mock
import sys

@pytest.fixture(autouse=True)
def patch_hal_rfid_reader():
	# Patch hal.hal_rfid_reader and its init().read_id() for compatibility with the current RFID.py
	hal_rfid_reader_mock = mock.Mock()
	rfid_reader_mock = mock.Mock()
	hal_rfid_reader_mock.init.return_value = rfid_reader_mock
	sys.modules['hal.hal_rfid_reader'] = hal_rfid_reader_mock
	sys.modules['rfid_reader_mock'] = rfid_reader_mock
	return rfid_reader_mock

def import_RFID():
	import importlib
	if 'RFID' in sys.modules:
		del sys.modules['RFID']
	return importlib.import_module('RFID')

def test_rfid_card_detected(capsys, patch_hal_rfid_reader):
	patch_hal_rfid_reader.read_id.return_value = 12345
	RFID = import_RFID()
	result = RFID.RFID_reader()
	captured = capsys.readouterr()
	assert result is True
	assert "RFID card detected! ID = 12345" in captured.out or "RFID card detected! ID = '12345'" in captured.out

def test_no_rfid_card_detected(capsys, patch_hal_rfid_reader):
	patch_hal_rfid_reader.read_id.return_value = None
	RFID = import_RFID()
	result = RFID.RFID_reader()
	captured = capsys.readouterr()
	assert result is False
	assert "No RFID card detected" in captured.out