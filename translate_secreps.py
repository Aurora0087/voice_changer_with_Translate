from googletrans import Translator


def translate_english_to_japanese(texts):
    try:
        translator = Translator()
        translate_channel = translator.translate(texts, dest='ja')
        return translate_channel
    except:
        return "ERROR...."


def translate_to_english(texts):
    try:
        translator = Translator()
        translate_channel = translator.translate(texts)
        return translate_channel
    except:
        return "ERROR....."
