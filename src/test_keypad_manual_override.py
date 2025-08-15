import pytest
import queue
import time
from unittest import mock

@pytest.fixture
def mock_dc_motor():
	return mock.Mock()

@pytest.fixture
def mock_servo():
	return mock.Mock()

@pytest.fixture
def mock_led():
	return mock.Mock()

@pytest.fixture
def mock_lcd_ctrl():
	lcd = mock.Mock()
	lcd.awaiting_password = False
	lcd.entered_passcode = ''
	lcd.override_success = False
	lcd.passcode_error = False
	return lcd

@pytest.fixture(autouse=True)
def patch_hal(monkeypatch, mock_dc_motor, mock_servo, mock_led, mock_lcd_ctrl):
	import sys
	sys.modules['hal.hal_dc_motor'] = mock.Mock(set_motor_speed=mock_dc_motor.set_motor_speed)
	sys.modules['hal.hal_servo'] = mock.Mock(set_servo_position=mock_servo.set_servo_position)
	sys.modules['hal.hal_led'] = mock.Mock(set_output=mock_led.set_output)
	sys.modules['lcd_display_controller'] = mock_lcd_ctrl
	monkeypatch.setattr('keypad_manual_override.set_override_mode', lambda x=True: None)
	monkeypatch.setattr('keypad_manual_override.set_awaiting_password', lambda x=True: setattr(mock_lcd_ctrl, 'awaiting_password', x))
	monkeypatch.setattr('keypad_manual_override.update_lcd_line1', lambda msg: None)
	monkeypatch.setattr('keypad_manual_override.update_lcd_line2', lambda msg: None)

def import_keypad_manual_override():
	import importlib
	return importlib.reload(importlib.import_module('keypad_manual_override'))

def run_thread_once(thread_func, system_state):
	import threading
	t = threading.Thread(target=thread_func, args=(system_state,), daemon=True)
	t.start()
	time.sleep(0.3)
	return t

def test_correct_passcode(monkeypatch, patch_hal, mock_dc_motor, mock_servo, mock_led, mock_lcd_ctrl):
	keypad_manual_override = import_keypad_manual_override()
	shared_keypad_queue = queue.Queue()
	system_state = {
		'fire_detected': True,
		'system_override': False,
		'motor_locked': False,
		'shared_keypad_queue': shared_keypad_queue
	}
	shared_keypad_queue.put('*')
	mock_lcd_ctrl.awaiting_password = True
	for k in ['1', '2', '3', '4', '#']:
		shared_keypad_queue.put(k)
	t = run_thread_once(keypad_manual_override.keypad_manual_override_thread, system_state)
	import time
	for _ in range(20):
		if system_state['fire_detected'] is False and system_state['motor_locked'] is True:
			break
		time.sleep(0.1)
	assert system_state['fire_detected'] is False
	assert system_state['motor_locked'] is True
	mock_dc_motor.set_motor_speed.assert_any_call(0)
	mock_servo.set_servo_position.assert_any_call(0)
	mock_led.set_output.assert_any_call(0, 0)

def test_incorrect_passcode(monkeypatch, patch_hal, mock_dc_motor, mock_servo, mock_led, mock_lcd_ctrl):
	keypad_manual_override = import_keypad_manual_override()
	shared_keypad_queue = queue.Queue()
	system_state = {
		'fire_detected': True,
		'system_override': False,
		'motor_locked': False,
		'shared_keypad_queue': shared_keypad_queue
	}
	shared_keypad_queue.put('*')
	mock_lcd_ctrl.awaiting_password = True
	for k in ['9', '9', '9', '9', '#']:
		shared_keypad_queue.put(k)
	t = run_thread_once(keypad_manual_override.keypad_manual_override_thread, system_state)
	import time
	for _ in range(20):
		if (mock_lcd_ctrl.entered_passcode == '9999' and
			system_state['fire_detected'] is True and
			system_state['motor_locked'] is False and
			mock_lcd_ctrl.passcode_error is False):
			break
		time.sleep(0.1)
	assert system_state['fire_detected'] is True
	assert system_state['motor_locked'] is False
	assert mock_lcd_ctrl.passcode_error is False
	assert mock_lcd_ctrl.entered_passcode == '9999'

def test_no_fire_detected(monkeypatch, patch_hal, mock_dc_motor, mock_servo, mock_led, mock_lcd_ctrl):
	keypad_manual_override = import_keypad_manual_override()
	shared_keypad_queue = queue.Queue()
	system_state = {
		'fire_detected': False,
		'system_override': False,
		'motor_locked': False,
		'shared_keypad_queue': shared_keypad_queue
	}
	shared_keypad_queue.put('*')
	t = run_thread_once(keypad_manual_override.keypad_manual_override_thread, system_state)
	t.join(timeout=0.5)
	assert mock_lcd_ctrl.awaiting_password is False