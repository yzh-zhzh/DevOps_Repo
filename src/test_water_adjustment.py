
import pytest
import time
from unittest import mock
import sys

@pytest.fixture
def mock_dc_motor():
	return mock.Mock()

@pytest.fixture
def mock_servo():
	return mock.Mock()

@pytest.fixture
def mock_adc():
	adc = mock.Mock()
	adc.get_adc_value.return_value = 512
	return adc

@pytest.fixture
def mock_update_water_volume():
	return mock.Mock()

@pytest.fixture(autouse=True)
def patch_hal_modules(mock_dc_motor, mock_servo, mock_adc, mock_update_water_volume):
	sys.modules['hal.hal_dc_motor'] = mock.Mock(set_motor_speed=mock_dc_motor.set_motor_speed)
	sys.modules['hal.hal_servo'] = mock.Mock(set_servo_position=mock_servo.set_servo_position)
	sys.modules['hal.hal_adc'] = mock_adc
	sys.modules['lcd_display_controller'] = mock.Mock(update_water_volume=mock_update_water_volume)

def import_water_adjustment():
	import importlib
	if 'water_adjustment' in sys.modules:
		del sys.modules['water_adjustment']
	return importlib.import_module('water_adjustment')

def run_thread_once(thread_func, system_state):
	import threading
	t = threading.Thread(target=thread_func, args=(system_state,), daemon=True)
	t.start()
	time.sleep(0.2)
	return t

def test_fire_detected_controls_motor_servo(mock_dc_motor, mock_servo, mock_adc, mock_update_water_volume):
	water_adjustment = import_water_adjustment()
	system_state = {'fire_detected': True, 'motor_locked': False}
	t = run_thread_once(water_adjustment.water_adjustment_thread, system_state)
	t.join(timeout=0.3)
	mock_dc_motor.set_motor_speed.assert_any_call(50)
	mock_servo.set_servo_position.assert_any_call(0)
	mock_update_water_volume.assert_any_call('Water Lvl: 50%')

def test_motor_locked_stops_motor_and_servo(mock_dc_motor, mock_servo, mock_update_water_volume):
	water_adjustment = import_water_adjustment()
	system_state = {'fire_detected': True, 'motor_locked': True}
	t = run_thread_once(water_adjustment.water_adjustment_thread, system_state)
	t.join(timeout=0.3)
	mock_dc_motor.set_motor_speed.assert_any_call(0)
	mock_servo.set_servo_position.assert_any_call(0)
	mock_update_water_volume.assert_any_call('Motor Locked!')

def test_no_fire_detected_stops_motor_and_servo(mock_dc_motor, mock_servo, mock_update_water_volume):
	water_adjustment = import_water_adjustment()
	system_state = {'fire_detected': False, 'motor_locked': False}
	t = run_thread_once(water_adjustment.water_adjustment_thread, system_state)
	t.join(timeout=0.3)
	mock_dc_motor.set_motor_speed.assert_any_call(0)
	mock_servo.set_servo_position.assert_any_call(0)
	mock_update_water_volume.assert_any_call('Water Lvl: 0%')
