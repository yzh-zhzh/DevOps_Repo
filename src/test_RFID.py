import pytest
from unittest import mock
import sys

@pytest.fixture(autouse=True)
def patch_hal_rfid_reader():
	sys.modules['hal.hal_rfid_reader'] = mock.Mock()

def import_RFID():
	import importlib
	if 'RFID' in sys.modules:
		del sys.modules['RFID']
	return importlib.import_module('RFID')

def test_rfid_card_detected(capsys):
	import sys
	sys.modules['hal.hal_rfid_reader'].read_id_no_block.return_value = 12345
	RFID = import_RFID()
	result = RFID.RFID_reader()
	captured = capsys.readouterr()
	assert result is True
	assert "RFID card detected! ID = 12345" in captured.out

def test_no_rfid_card_detected(capsys):
	import sys
	sys.modules['hal.hal_rfid_reader'].read_id_no_block.return_value = None
	RFID = import_RFID()
	result = RFID.RFID_reader()
	captured = capsys.readouterr()
	assert result is False
	assert "No RFID card detected" in captured.out