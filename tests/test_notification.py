import pytest

from summary_pocket.utils import notification_util


def test_notify_to_slack():
    """Slackに通知できるか"""
    assert notification_util.notify_to_slack('test') is True
    assert notification_util.notify_to_slack('test') is True


def test_notify_to_slack_error():
    """Slackに通知できないときはFalseを返すか"""
    assert notification_util.notify_to_slack('test') is False
    # AssertionErrorが出る
    with pytest.raises(AssertionError):
        notification_util.notify_to_slack('test')
