import pytest
import time
from unittest import mock

@pytest.fixture
def mock_buzzer():
	return mock.Mock()

@pytest.fixture(autouse=True)
def patch_hal_buzzer(monkeypatch, mock_buzzer):
	monkeypatch.setattr('hal.hal_buzzer', mock_buzzer)

def import_play_fire_tone():
	import importlib
	return importlib.reload(importlib.import_module('play_fire_tone'))

def run_thread_once(thread_func, system_state):
	import threading
	t = threading.Thread(target=thread_func, args=(system_state,), daemon=True)
	t.start()
	time.sleep(0.2)
	return t

def test_fire_detected_buzzer_on_off(monkeypatch, patch_hal_buzzer, mock_buzzer):
	play_fire_tone = import_play_fire_tone()
	system_state = {'fire_detected': True, 'motor_locked': False}
	monkeypatch.setattr(play_fire_tone, 'time', mock.Mock(sleep=mock.Mock(side_effect=Exception('break'))))
	try:
		play_fire_tone.play_fire_alert_tone(system_state)
	except Exception:
		pass
	mock_buzzer.turn_on.assert_called_once()
	mock_buzzer.turn_off.assert_called()

def test_no_fire_detected_buzzer_off(monkeypatch, patch_hal_buzzer, mock_buzzer):
	play_fire_tone = import_play_fire_tone()
	system_state = {'fire_detected': False, 'motor_locked': False}
	monkeypatch.setattr(play_fire_tone, 'time', mock.Mock(sleep=mock.Mock(side_effect=Exception('break'))))
	try:
		play_fire_tone.play_fire_alert_tone(system_state)
	except Exception:
		pass
	mock_buzzer.turn_on.assert_not_called()
	mock_buzzer.turn_off.assert_called_once()
