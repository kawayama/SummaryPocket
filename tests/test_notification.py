import pytest

from summary_pocket import notification


def test_notify_to_slack():
    """Slackに通知できるか"""
    assert notification.notify_to_slack('test', '#error') is True
    assert notification.notify_to_slack('test', '#notify') is True


def test_notify_to_slack_error():
    """Slackに通知できないときはFalseを返すか"""
    assert notification.notify_to_slack('test', '#hoge') is False
    # AssertionErrorが出る
    with pytest.raises(AssertionError):
        notification.notify_to_slack('test', 'hoge')
