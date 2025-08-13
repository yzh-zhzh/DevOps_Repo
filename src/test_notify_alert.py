import pytest
import builtins
import notify_alert
from unittest import mock

@pytest.fixture
def config_dict():
	return {
		"location": "Test Lab",
		"recipient_email": "test@example.com",
		"telegram_bot_token": "123:abc",
		"telegram_chat_id": "456"
	}

def test_send_email_alert(monkeypatch):
	with mock.patch("smtplib.SMTP") as smtp_mock:
		smtp_instance = smtp_mock.return_value
		notify_alert.send_email_alert("Test Lab", "test@example.com")
		smtp_mock.assert_called_with("smtp.gmail.com", 587)
		smtp_instance.starttls.assert_called_once()
		smtp_instance.login.assert_called_once()
		smtp_instance.send_message.assert_called_once()
		smtp_instance.quit.assert_called_once()

def test_send_telegram_alert(monkeypatch):
	with mock.patch("requests.post") as post_mock:
		notify_alert.send_telegram_alert("123:abc", "456", "Test Lab")
		post_mock.assert_called_once()
		args, kwargs = post_mock.call_args
		assert "https://api.telegram.org/bot123:abc/sendMessage" in args[0]
		assert kwargs["data"]["chat_id"] == "456"
		assert "FIRE ALERT" in kwargs["data"]["text"]

def test_load_notification_config(monkeypatch, config_dict):
	fake_file = mock.mock_open(read_data='{"location": "Test Lab", "recipient_email": "test@example.com", "telegram_bot_token": "123:abc", "telegram_chat_id": "456"}')
	monkeypatch.setattr(builtins, "open", fake_file)
	config = notify_alert.load_notification_config()
	assert config["location"] == "Test Lab"
	assert config["recipient_email"] == "test@example.com"

def test_notify_fire_alert(monkeypatch, config_dict):
	monkeypatch.setattr(notify_alert, "load_notification_config", lambda: config_dict)
	email_mock = mock.Mock()
	telegram_mock = mock.Mock()
	monkeypatch.setattr(notify_alert, "send_email_alert", email_mock)
	monkeypatch.setattr(notify_alert, "send_telegram_alert", telegram_mock)
	monkeypatch.setattr(notify_alert, "time", mock.Mock(sleep=mock.Mock(side_effect=Exception("break"))))
	system_state = {"fire_detected": True, "system_override": False}
	try:
		notify_alert.notify_fire_alert(system_state)
	except Exception:
		pass
	email_mock.assert_called_once_with("Test Lab", "test@example.com")
	telegram_mock.assert_called_once_with("123:abc", "456", "Test Lab")
