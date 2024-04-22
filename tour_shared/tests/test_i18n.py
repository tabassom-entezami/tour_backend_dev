import pytest

import eventlet
from nameko import config

from tour_shared.i18n.translate import (
    activate, deactivate, gettext, gettext_lazy, get_language_from_header
)


hw_en = 'Hello, world!'
hw_fa = 'سلام، دنیا!'


@pytest.fixture
def lang_config():
    lang = {
        'LANGUAGE': {
            'local_path': 'tests/locales',
            'supported': ['fa'],
            'default': 'en'
        }
    }
    with config.patch(lang):
        yield


@pytest.fixture
def activate_fa(lang_config):
    activate('fa')
    yield
    deactivate()


@pytest.mark.parametrize('lang', [None, False, [], ''])
def test_activate_when_falsy_lang_value_passed(lang):
    assert activate(lang) is None


def test_activate_fails_with_no_config():
    with pytest.raises(KeyError, match='LANGUAGE'):
        activate('en')


def test_activate_when_localedir_does_not_exist():
    lang = {
        'LANGUAGE': {
            'local_path': 'nonexistent'
        }
    }
    with config.patch(lang):
        assert activate('en') is None


def test_gettext_with_no_explicit_activate_returns_default(lang_config):
    assert gettext('Hello, world!') == hw_en


def test_gettext_with_activate(activate_fa):
    assert gettext('Hello, world!') == hw_fa


def test_gettext_with_unavailable_lang_returns_default(lang_config):
    activate('foo')
    assert gettext('Hello, world!') == hw_en


@pytest.mark.parametrize('locale', ['fa', 'fa_IR'])
def test_gettext_with_standard_varations_of_same_locale(lang_config, locale):
    def activate_fa(lc):
        activate(lc)
        return gettext('Hello, world!')

    assert eventlet.spawn(activate_fa, locale).wait() == hw_fa


def test_gettext_with_untranslated_string(activate_fa):
    assert gettext('untranslated') == 'untranslated'


def test_activate_is_thread_local(lang_config):
    def activate_fa():
        activate('fa')
        return gettext('Hello, world!')

    assert eventlet.spawn(activate_fa).wait() == hw_fa

    def no_activate():
        return gettext('Hello, world!')

    assert eventlet.spawn(no_activate).wait() == hw_en


@pytest.mark.parametrize(
    'lang,expected',
    [
        ('foo', 'en'), ('de', 'en'), ('en', 'en'), ('en-US', 'en'),
        ('fa', 'fa'), ('fa-IR', 'fa'),
    ]
)
def test_get_lang_from_header(lang_config, lang, expected):
    assert get_language_from_header(lang) == expected
