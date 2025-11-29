# bot/i18n/__init__.py
from typing import Dict
from importlib import import_module

# кэш загруженных языков
_LOCALES: Dict[str, Dict[str, str]] = {}

def load_locale(lang: str) -> Dict[str, str]:
    lang = (lang or "en").lower()
    if lang in _LOCALES:
        return _LOCALES[lang]
    try:
        mod = import_module(f"bot.i18n.{lang}")
        msgs = getattr(mod, "MESSAGES", {})
        _LOCALES[lang] = msgs
        return msgs
    except ModuleNotFoundError:
        # fallback to ru
        if lang != "en":
            return load_locale("en")
        return {}

def t(key: str, lang: str | None = None, /, **kwargs) -> str:
    """
    Получить строку по ключу и подставить kwargs (format).
    lang может быть кодом 'ru'/'en'/'uk'. Если None — используем 'ru'.
    """
    msgs = load_locale(lang or "en")
    text = msgs.get(key) or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

def t_found_results(count: int, lang: str | None = None) -> str:
    """
    Получить локализованное сообщение о найденных результатах с правильными склонениями.
    Поддерживает склонения для русского, украинского и английского языков.
    """
    lang = lang or "en"
    
    if count == 1:
        key = "search.found_results.1"
    elif count == 2:
        key = "search.found_results.2"
    elif count == 3:
        key = "search.found_results.3"
    elif count == 4:
        key = "search.found_results.4"
    elif count == 5:
        key = "search.found_results.5"
    else:
        key = "search.found_results.6+"
        return t(key, lang, count=count)
    
    return t(key, lang)


def t_found_transfers(count: int, lang: str | None = None) -> str:
    """
    Получить локализованное сообщение о количестве пересадок с правильными склонениями.
    Поддерживает склонения для русского, украинского и английского языков.
    """
    lang = lang or "en"

    if count == 1:
        key = "flight.with_transfers.1"
    elif count == 2:
        key = "flight.with_transfers.2"
    elif count == 3:
        key = "flight.with_transfers.3"
    elif count == 4:
        key = "flight.with_transfers.4"
    elif count == 5:
        key = "flight.with_transfers.5"
    else:
        key = "flight.with_transfers.6+"
        return t(key, lang, count=count)

    return t(key, lang)