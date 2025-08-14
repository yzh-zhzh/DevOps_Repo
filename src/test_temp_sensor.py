import pytest
from unittest import mock
import sys

@pytest.fixture(autouse=True)
def patch_hal_and_deps():
	sys.modules['hal.hal_temp_humidity_sensor'] = mock.Mock()
	sys.modules['hal.hal_servo'] = mock.Mock(set_servo_position=mock.Mock())
	sys.modules['hal.hal_dc_motor'] = mock.Mock(set_motor_speed=mock.Mock())
	sys.modules['hal.hal_buzzer'] = mock.Mock()
	sys.modules['lcd_display_controller'] = mock.Mock(set_fire_detected=mock.Mock(), set_override_mode=mock.Mock())
	sys.modules['play_fire_tone'] = mock.Mock(play_fire_alert_tone=mock.Mock())
	sys.modules['Fire_detection'] = mock.Mock(fire_detected=mock.Mock(return_value=True))

def import_temp_sensor():
	import importlib
	if 'temp_sensor' in sys.modules:
		del sys.modules['temp_sensor']
	return importlib.import_module('temp_sensor')

def test_fire_detection_thread(monkeypatch):
	temp_sensor = import_temp_sensor()
	monkeypatch.setattr(temp_sensor, 'time', mock.Mock(sleep=mock.Mock(side_effect=Exception('break'))))
	system_state = {'fire_detected': False, 'motor_locked': False}
	try:
		temp_sensor.fire_detection_thread(system_state)
	except Exception:
		pass
	assert system_state['fire_detected'] is True
	assert system_state['motor_locked'] is False
