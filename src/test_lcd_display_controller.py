import pytest
import builtins
import time
from unittest.mock import MagicMock, patch
import lcd_display_controller as lcd_ctrl

@pytest.fixture(autouse=True)
def mock_lcd():
    with patch("lcd_display_controller.LCD.lcd") as mock_lcd_class:
        mock_lcd_instance = MagicMock()
        mock_lcd_class.return_value = mock_lcd_instance
        lcd_ctrl.lcd = mock_lcd_instance
        yield mock_lcd_instance


def run_display_once():
    with patch("time.sleep", side_effect=StopIteration):
        try:
            lcd_ctrl.lcd_display_thread()
        except StopIteration:
            pass


def test_default_ready_message(mock_lcd):
    lcd_ctrl.override_success = False
    lcd_ctrl.fire_detected = False
    run_display_once()

    mock_lcd.lcd_display_string.assert_any_call("Smart Fire Alert".ljust(16), 1)
    mock_lcd.lcd_display_string.assert_any_call("System Ready!".ljust(16), 2)


def test_override_success_message(mock_lcd):
    lcd_ctrl.override_success = True
    run_display_once()

    mock_lcd.lcd_display_string.assert_any_call("Override Success".ljust(16), 1)
    mock_lcd.lcd_display_string.assert_any_call("System Off!".ljust(16), 2)


def test_fire_detected_with_password(mock_lcd):
    lcd_ctrl.fire_detected = True
    lcd_ctrl.awaiting_password = True
    lcd_ctrl.entered_passcode = "12"
    lcd_ctrl.passcode_error = False
    run_display_once()

    mock_lcd.lcd_display_string.assert_any_call("Enter Passcode:".ljust(16), 1)
    mock_lcd.lcd_display_string.assert_any_call("12".ljust(16), 2)


def test_fire_detected_with_wrong_password(mock_lcd):
    lcd_ctrl.fire_detected = True
    lcd_ctrl.awaiting_password = True
    lcd_ctrl.entered_passcode = "99"
    lcd_ctrl.passcode_error = True
    run_display_once()

    mock_lcd.lcd_display_string.assert_any_call("Wrong Passcode!".ljust(16), 1)
    mock_lcd.lcd_display_string.assert_any_call("Try Again!".ljust(16), 2)


def test_update_sprinkler_status_and_water_volume():
    lcd_ctrl.update_sprinkler_status("Sprinkler OK")
    assert lcd_ctrl.sprinkler_status_message == "Sprinkler OK"

    lcd_ctrl.update_water_volume("Vol: 50%")
    assert lcd_ctrl.water_volume_message == "Vol: 50%"


def test_update_lcd_lines(mock_lcd):
    lcd_ctrl.update_lcd_line1("Hello")
    mock_lcd.lcd_display_string.assert_called_with("Hello".ljust(16), 1)

    lcd_ctrl.update_lcd_line2("World")
    mock_lcd.lcd_display_string.assert_called_with("World".ljust(16), 2)