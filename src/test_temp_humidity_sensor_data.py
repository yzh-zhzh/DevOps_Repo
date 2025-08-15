import pytest
from unittest import mock
import sys

@pytest.fixture(autouse=True)
def patch_hal_temp_humidity():
	mock_hal = mock.Mock()
	mock_hal.init = mock.Mock()
	mock_hal.read_temp_humidity = mock.Mock(return_value=(25.5, 60.2))
	sys.modules['src.hal.hal_temp_humidity_sensor'] = mock_hal

def import_temp_humidity_sensor_data():
	import importlib
	if 'temp_humidity_sensor_data' in sys.modules:
		del sys.modules['temp_humidity_sensor_data']
	return importlib.import_module('temp_humidity_sensor_data')

def test_read_data():
	mod = import_temp_humidity_sensor_data()
	temp, humid = mod.read_data()
	assert temp == 25.5
	assert humid == 60.2

def test_main(monkeypatch):
	mod = import_temp_humidity_sensor_data()
	# Patch sleep to avoid delay
	monkeypatch.setattr(mod, 'sleep', lambda x: None)
	result = mod.main()
	assert result == (25.5, 60.2)
