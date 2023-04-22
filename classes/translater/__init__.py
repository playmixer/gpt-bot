from translate import Translator


def translate(text: str, from_lang="ru", to_lang="en"):
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translation = translator.translate(text)
    return translation
