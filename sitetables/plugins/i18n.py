from django.utils.translation import get_language

from .base import TablePlugin


LANGS = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijan',
    'bn': 'Bangla',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'zh-hant': 'Chinese-traditional',
    'zh-hans': 'Chinese',
    'zh': 'Chinese',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    # 'en': 'English',  # this on is built-in
    'et': 'Estonian',
    'fil': 'Filipino',  # no two-letter code
    'fi': 'Finnish',
    'fr': 'French',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ida': 'Indonesian-Alternative',  # pseudo code
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'kk': 'Kazakh',
    'ko': 'Korean',
    'ky': 'Kyrgyz',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'mk': 'Macedonian',
    'ml': 'Malay',
    'mn': 'Mongolian',
    'ne': 'Nepali',
    'nb': 'Norwegian-Bokmal',
    'nn': 'Norwegian-Nynorsk',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt-br': 'Portuguese-Brasil',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sr': 'Serbian',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'ta': 'Tamil',
    'te': 'telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
}


class I18nPlugin(TablePlugin):
    """Internationalization plugin."""

    def __init__(self, lang_code=None):
        """
        :param str lang_code: Language code (usually two-letter). E.g.: ru, de
        """
        self.lang = lang_code

    def contribute_to_config(self, config, table):
        super().contribute_to_config(config, table)

        code = self.lang

        if code is None:
            # Try auto.
            code = get_language()

        name = LANGS.get(code)

        if name:
            config['language'] = {'url': table.url_plugins + 'i18n/' + name + '.json'}
