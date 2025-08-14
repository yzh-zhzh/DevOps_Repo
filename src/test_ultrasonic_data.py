import pytest
from unittest import mock
import sys

@pytest.fixture(autouse=True)
def patch_hal_usonic():
	mock_usonic = mock.Mock()
	mock_usonic.init = mock.Mock()
	mock_usonic.get_distance = mock.Mock(return_value=50)
	sys.modules['hal.hal_usonic'] = mock_usonic

def import_ultrasonic_data():
	import importlib
	if 'ultrasonic_data' in sys.modules:
		del sys.modules['ultrasonic_data']
	return importlib.import_module('ultrasonic_data')

def test_read_data():
	mod = import_ultrasonic_data()
	assert mod.read_data() == 50

@pytest.mark.parametrize('distance,expected', [(50, True), (150, False)])
def test_detect_presence(distance, expected):
	mod = import_ultrasonic_data()
	assert mod.detect_presence(distance) == expected

def test_ultrasonic_data_thread_presence_detected(monkeypatch, capsys):
	mod = import_ultrasonic_data()
	monkeypatch.setattr(mod, 'read_data', lambda: 50)
	monkeypatch.setattr(mod, 'time', mock.Mock(sleep=mock.Mock(side_effect=Exception('break'))))
	system_state = {'fire_detected': True, 'system_override': False}
	try:
		mod.ultrasonic_data_thread(system_state)
	except Exception:
		pass
	captured = capsys.readouterr()
	assert "Presence detected during fire" in captured.out

def test_ultrasonic_data_thread_no_presence(monkeypatch, capsys):
	mod = import_ultrasonic_data()
	monkeypatch.setattr(mod, 'read_data', lambda: 150)
	monkeypatch.setattr(mod, 'time', mock.Mock(sleep=mock.Mock(side_effect=Exception('break'))))
	system_state = {'fire_detected': True, 'system_override': False}
	try:
		mod.ultrasonic_data_thread(system_state)
	except Exception:
		pass
	captured = capsys.readouterr()
	assert "No presence detected" in captured.out

def test_ultrasonic_data_thread_no_fire(monkeypatch, capsys):
	mod = import_ultrasonic_data()
	monkeypatch.setattr(mod, 'time', mock.Mock(sleep=mock.Mock(side_effect=Exception('break'))))
	system_state = {'fire_detected': False, 'system_override': False}
	try:
		mod.ultrasonic_data_thread(system_state)
	except Exception:
		pass
	captured = capsys.readouterr()
	assert captured.out == ''

def test_main_presence_detected(monkeypatch, capsys):
	mod = import_ultrasonic_data()
	monkeypatch.setattr(mod, 'read_data', lambda: 50)
	monkeypatch.setattr(mod, 'sleep', lambda x: None)
	monkeypatch.setattr(mod, 'detect_presence', lambda d: True)
	called = {'count': 0}
	orig_print = print
	def fake_print(*args, **kwargs):
		called['count'] += 1
		orig_print(*args, **kwargs)
		if called['count'] > 0:
			raise Exception('break')
	monkeypatch.setattr('builtins.print', fake_print)
	try:
		mod.main()
	except Exception:
		pass
	captured = capsys.readouterr()
	assert "Presence Detected" in captured.out

def test_main_no_presence_detected(monkeypatch, capsys):
	mod = import_ultrasonic_data()
	monkeypatch.setattr(mod, 'read_data', lambda: 150)
	monkeypatch.setattr(mod, 'sleep', lambda x: None)
	monkeypatch.setattr(mod, 'detect_presence', lambda d: False)
	called = {'count': 0}
	orig_print = print
	def fake_print(*args, **kwargs):
		called['count'] += 1
		orig_print(*args, **kwargs)
		if called['count'] > 0:
			raise Exception('break')
	monkeypatch.setattr('builtins.print', fake_print)
	try:
		mod.main()
	except Exception:
		pass
	captured = capsys.readouterr()
	assert "No Presence Detected" in captured.out
