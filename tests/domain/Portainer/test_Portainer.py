from domain.Portainer.Portainer import Portainer
import datetime
import settings
from domain.Portainer.Stack import Stack


def test_creation():
    portainer: Portainer = Portainer("prod", "https://portainer.com:5000")

    assert portainer.name == "prod"
    assert portainer.endpoint == "https://portainer.com:5000"
    assert portainer.next_check <= datetime.datetime.now().timestamp()


def test_invalid_endpoint():
    try:
        Portainer("prod", "https://portainer:5000")
        assert False
    except AssertionError:
        assert True


def test_name_immutable():
    portainer: Portainer = Portainer("prod", "https://portainer.com:5000")

    try:
        portainer.name = "preprod"
        assert False
    except Exception:
        assert True


def test_endpoint_immutable():
    portainer: Portainer = Portainer("prod", "https://portainer.com:5000")

    try:
        portainer.endpoint = "https://portainer.com:6000"
        assert False
    except Exception:
        assert True


def test_next_check_property_immutable():
    portainer: Portainer = Portainer("prod", "https://portainer.com:5000")

    try:
        portainer.next_check = 3
        assert False
    except Exception:
        assert True


def test_prepare_check():
    portainer: Portainer = Portainer("prod", "https://portainer.com:5000")
    before = datetime.datetime.now().timestamp()
    portainer.prepare_check()

    assert (
        before
        <= portainer.next_check
        <= datetime.datetime.now().timestamp() + settings.NEXT_CHECK_INTERVAL
    )


def test_add_stack():
    portainer: Portainer = Portainer("prod", "https://portainer.com:5000")
    portainer.add_stack("nginx")

    assert len(portainer.stacks) == 1
    assert all(isinstance(s, Stack) for s in portainer.stacks)
    assert [s.name for s in portainer.stacks] == ["nginx"]


def test_add_stack_duplicate():
    portainer: Portainer = Portainer("prod", "https://portainer.com:5000")
    portainer.add_stack("nginx")

    try:
        portainer.add_stack("nginx")
        assert False
    except AssertionError:
        assert True


def test_remove_stack():
    portainer: Portainer = Portainer("prod", "https://portainer.com:5000")
    portainer.add_stack("nginx")
    portainer.remove_stack("nginx")

    assert len(portainer.stacks) == 0


def test_remove_stack_not_exists():
    portainer: Portainer = Portainer("prod", "https://portainer.com:5000")

    try:
        portainer.remove_stack("nginx")
        assert False
    except AssertionError:
        assert True
