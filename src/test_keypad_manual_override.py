import pytest
import queue
import time
from unittest import mock

@pytest.fixture
def system_state():
    return {
        'fire_detected': True,
        'motor_locked': False,
        'shared_keypad_queue': queue.Queue()
    }

@pytest.fixture
def lcd_ctrl():
    lcd = mock.MagicMock()
    lcd.awaiting_password = False
    lcd.entered_passcode = ''
    lcd.override_success = False
    lcd.passcode_error = False
    return lcd

def run_thread_once(thread_func, system_state):
    import threading
    t = threading.Thread(target=thread_func, args=(system_state,), daemon=True)
    t.start()
    time.sleep(0.3)
    return t

def test_correct_passcode(system_state, lcd_ctrl, monkeypatch):
    with mock.patch('keypad_manual_override.dc_motor') as dc_motor, \
         mock.patch('keypad_manual_override.servo') as servo, \
         mock.patch('keypad_manual_override.led') as led, \
         mock.patch('keypad_manual_override.lcd_display_controller', lcd_ctrl), \
         mock.patch('keypad_manual_override.set_override_mode'), \
         mock.patch('keypad_manual_override.set_awaiting_password'):
        import keypad_manual_override
        q = system_state['shared_keypad_queue']
        for k in ['*', '1', '2', '3', '4', '#']:
            q.put(k)
        t = run_thread_once(keypad_manual_override.keypad_manual_override_thread, system_state)
        t.join(timeout=0.5)
        assert system_state['fire_detected'] is False
        assert system_state['motor_locked'] is True
        dc_motor.set_motor_speed.assert_called_with(0)
        servo.set_servo_position.assert_called_with(0)
        led.set_output.assert_called_with(0, 0)
        assert lcd_ctrl.override_success is True

def test_incorrect_passcode(system_state, lcd_ctrl, monkeypatch):
    with mock.patch('keypad_manual_override.dc_motor'), \
         mock.patch('keypad_manual_override.servo'), \
         mock.patch('keypad_manual_override.led'), \
         mock.patch('keypad_manual_override.lcd_display_controller', lcd_ctrl), \
         mock.patch('keypad_manual_override.set_override_mode'), \
         mock.patch('keypad_manual_override.set_awaiting_password'):
        import keypad_manual_override
        q = system_state['shared_keypad_queue']
        for k in ['*', '9', '9', '9', '9', '#']:
            q.put(k)
        t = run_thread_once(keypad_manual_override.keypad_manual_override_thread, system_state)
        t.join(timeout=0.5)
        assert system_state['fire_detected'] is True
        assert system_state['motor_locked'] is False
        assert lcd_ctrl.passcode_error is True
        assert lcd_ctrl.entered_passcode == '9999'