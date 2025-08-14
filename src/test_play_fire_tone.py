import pytest
import time
from unittest import mock
import sys

@pytest.fixture
def mock_buzzer():
	return mock.Mock()

@pytest.fixture(autouse=True)
def patch_hal_buzzer(mock_buzzer):
	# Patch RPi.GPIO and hal.hal_buzzer in sys.modules before import
	sys.modules['RPi'] = mock.MagicMock()
	sys.modules['RPi.GPIO'] = mock.MagicMock()
	hal_buzzer_mock = mock.Mock()
	hal_buzzer_mock.turn_on = mock_buzzer.turn_on
	hal_buzzer_mock.turn_off = mock_buzzer.turn_off
	sys.modules['hal.hal_buzzer'] = hal_buzzer_mock

def import_play_fire_tone():
	import importlib
	if 'play_fire_tone' in sys.modules:
		del sys.modules['play_fire_tone']
	return importlib.import_module('play_fire_tone')

def test_fire_detected_buzzer_on_off(monkeypatch, mock_buzzer):
	play_fire_tone = import_play_fire_tone()
	system_state = {'fire_detected': True, 'motor_locked': False}
	monkeypatch.setattr(play_fire_tone, 'time', mock.Mock(sleep=mock.Mock(side_effect=Exception('break'))))
	try:
		play_fire_tone.play_fire_alert_tone(system_state)
	except Exception:
		pass
	mock_buzzer.turn_on.assert_called_once()

def test_no_fire_detected_buzzer_off(monkeypatch, mock_buzzer):
	play_fire_tone = import_play_fire_tone()
	system_state = {'fire_detected': False, 'motor_locked': False}
	monkeypatch.setattr(play_fire_tone, 'time', mock.Mock(sleep=mock.Mock(side_effect=Exception('break'))))
	try:
		play_fire_tone.play_fire_alert_tone(system_state)
	except Exception:
		pass
	mock_buzzer.turn_on.assert_not_called()
	mock_buzzer.turn_off.assert_called_once()