import pytest
import time
from unittest import mock
import sys

@pytest.fixture
def mock_moisture_sensor():
	sensor = mock.Mock()
	sensor.init = mock.Mock()
	sensor.read_sensor = mock.Mock()
	return sensor

@pytest.fixture
def mock_update_sprinkler_status():
	return mock.Mock()

@pytest.fixture(autouse=True)
def patch_hal(monkeypatch, mock_moisture_sensor, mock_update_sprinkler_status):
	monkeypatch.setitem(sys.modules, 'hal.hal_moisture_sensor', mock_moisture_sensor)
	monkeypatch.setattr('lcd_display_controller.update_sprinkler_status', mock_update_sprinkler_status)

def import_sprinkler_confirmation():
	import importlib
	return importlib.reload(importlib.import_module('sprinkler_confirmation'))

def run_thread_once(thread_func, system_state):
	import threading
	t = threading.Thread(target=thread_func, args=(system_state,), daemon=True)
	t.start()
	time.sleep(0.2)
	return t

def test_water_released(monkeypatch, patch_hal, mock_moisture_sensor, mock_update_sprinkler_status):
	mock_moisture_sensor.read_sensor.return_value = 100
	sprinkler_confirmation = import_sprinkler_confirmation()
	system_state = {'fire_detected': True, 'system_override': False}
	t = run_thread_once(sprinkler_confirmation.moisture_sensor_sprinkler_confirmation_thread, system_state)
	t.join(timeout=0.3)
	mock_update_sprinkler_status.assert_any_call('Water Released!')

def test_check_sensor(monkeypatch, patch_hal, mock_moisture_sensor, mock_update_sprinkler_status):
	mock_moisture_sensor.read_sensor.return_value = 0
	sprinkler_confirmation = import_sprinkler_confirmation()
	system_state = {'fire_detected': True, 'system_override': False}
	t = run_thread_once(sprinkler_confirmation.moisture_sensor_sprinkler_confirmation_thread, system_state)
	t.join(timeout=0.3)
	mock_update_sprinkler_status.assert_any_call('Check Sensor!')

def test_no_fire_detected(monkeypatch, patch_hal, mock_moisture_sensor, mock_update_sprinkler_status):
	sprinkler_confirmation = import_sprinkler_confirmation()
	system_state = {'fire_detected': False, 'system_override': False}
	t = run_thread_once(sprinkler_confirmation.moisture_sensor_sprinkler_confirmation_thread, system_state)
	t.join(timeout=0.3)
	mock_update_sprinkler_status.assert_not_called()
