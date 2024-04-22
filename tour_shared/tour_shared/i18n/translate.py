"""
i18n utitlies for Nameko

This module defines three main functions:
* gettext
* gettext_lazy
* activate
"""
import os
import re
import gettext as gettext_module
from functools import total_ordering, wraps, lru_cache

from nameko import config
from eventlet.corolocal import local

from tour_shared.utils import lazy

_thread_local = local()
_default = None
# Translations are cached in a dictionary for every language.
# The active translations are stored by thread ID to make them thread local.
_translations = {}

# Format of Accept-Language header values. From RFC 2616, section 14.4 and 3.9
# and RFC 3066, section 2.1
accept_language_re = re.compile(
    r'''
    ([A-Za-z]{1,8}(?:-[A-Za-z0-9]{1,8})*|\*)      # "en", "en-au", "x-y-z", "es-419", "*"
    (?:\s*;\s*q=(0(?:\.\d{,3})?|1(?:\.0{,3})?))?  # Optional "q=1.00", "q=0.8"
    (?:\s*,\s*|$)                                 # Multiple accepts per header.
    ''',
    re.VERBOSE
)

language_code_re = re.compile(
    r'^[a-z]{1,8}(?:-[a-z0-9]{1,8})*(?:@[a-z0-9]{1,20})?$',
    re.IGNORECASE
)


def get_language_attribute(key, default=None):
    language_config = config.get("LANGUAGE")
    return language_config.get(key, default)


def get_lang_config(key, default=None):
    language_config = config['LANGUAGE']
    return language_config.get(key, default)


def translation(language, domain='base'):
    # NOTE: Possible DoS attack via injecting a series of valid langs.
    # The _translations variable will grow unbounded.
    if language not in _translations:
        _translations[language] = gettext_module.translation(
            domain=domain,
            localedir=os.path.abspath(get_lang_config('local_path')),
            languages=[language],
            fallback=True
        )
    return _translations[language]


def activate(language):
    """
    Fetch the translation object for a given language and install it as the
    current translation object for the current thread.

    NOTE: It only understands locales in form of language[_teritory]
    """
    if not language:
        return

    _thread_local.translation = translation(language)


def deactivate():
    if hasattr(_thread_local, 'translation'):
        del _thread_local.translation


def gettext(message):
    """
    Translate the 'message' string. It uses the current thread to find the
    translation object to use. If no current translation is activated, the
    message will be run through the default translation object.
    """
    global _default
    eol_message = message.replace('\r\n', '\n').replace('\r', '\n')
    if eol_message:
        _default = _default or translation(get_lang_config('default'))
        translation_object = getattr(_thread_local, 'translation', _default)

        result = translation_object.gettext(eol_message)
    else:
        # Return an empty value of the corresponding type if an empty message
        # is given, instead of metadata, which is the default gettext behavior.
        result = type(message)('')

    return result


def to_locale(language):
    """Turn a language name (en-us) into a locale name (en_US)."""
    lang, _, country = language.lower().partition('-')
    if not country:
        return language[:3].lower() + language[3:]
    # A language with > 2 characters after the dash only has its first
    # character after the dash capitalized; e.g. sr-latn becomes sr_Latn.
    # A language with 2 characters after the dash has both characters
    # capitalized; e.g. en-us becomes en_US.
    country, _, tail = country.partition('-')
    country = country.title() if len(country) > 2 else country.upper()
    if tail:
        country += '-' + tail
    return lang + '_' + country


@lru_cache(maxsize=1000)
def check_for_language(lang_code, domain='base'):
    """
    Check whether there is a global language file for the given language
    code. This is used to decide whether a user-provided language is
    available.
    """
    # First, a quick check to make sure lang_code is well-formed
    if lang_code is None or not language_code_re.search(lang_code):
        return False
    path = os.path.abspath(get_lang_config('local_path'))
    return gettext_module.find(domain, path, [to_locale(lang_code)]) is not None


@lru_cache(maxsize=1000)
def get_supported_language_variant(lang_code):
    """
    Return the language code that's listed in supported languages, possibly
    selecting a more generic variant. Raise LookupError if nothing is found.
    """
    if lang_code:
        # If 'fr-ca' is not supported, try language-only 'fr'.
        possible_lang_codes = [lang_code]
        generic_lang_code = lang_code.split('-')[0]
        possible_lang_codes.append(generic_lang_code)
        supported_lang_codes = get_lang_config('supported', [])

        for code in possible_lang_codes:
            if code in supported_lang_codes and check_for_language(code):
                return code
    raise LookupError(lang_code)


def get_language_from_header(header):
    """
    Analyze the header to find what language the user wants the system to show.
    If the user requests a sublanguage where we have a main language, we send
    out the main language.
    """
    for accept_lang, unused in parse_accept_lang_header(header):
        if accept_lang == '*':
            break

        if not language_code_re.search(accept_lang):
            continue

        try:
            return get_supported_language_variant(accept_lang)
        except LookupError:
            continue

    try:
        return get_supported_language_variant(get_lang_config('default'))
    except LookupError:
        return get_lang_config('default')


def get_language_from_request(request):
    accept = request.headers.get('Accept-Language', '')
    for accept_lang, unused in parse_accept_lang_header(accept):
        if accept_lang == '*':
            break

        if not language_code_re.search(accept_lang):
            continue

        if accept_lang in get_language_attribute('supported', []):
            return accept_lang

    return get_language_attribute('default')


@lru_cache(maxsize=1000)
def parse_accept_lang_header(lang_string):
    """
    Parse the lang_string, which is the body of an HTTP Accept-Language
    header, and return a tuple of (lang, q-value), ordered by 'q' values.

    Return an empty tuple if there are any format errors in lang_string.
    """
    result = []
    pieces = accept_language_re.split(lang_string.lower())
    if pieces[-1]:
        return ()
    for i in range(0, len(pieces) - 1, 3):
        first, lang, priority = pieces[i:i + 3]
        if first:
            return ()
        if priority:
            priority = float(priority)
        else:
            priority = 1.0
        result.append((lang, priority))
    result.sort(key=lambda k: k[1], reverse=True)
    return tuple(result)


gettext_lazy = lazy(gettext, str)
