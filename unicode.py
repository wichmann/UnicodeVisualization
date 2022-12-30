# info: https://realpython.com/pyscript-python-in-browser/#disclaimer-pyscript-is-an-experimental-project

import unicodedata

from js import document, console, window
from pyodide.ffi import create_proxy
from pyscript import Element


# global flag for choosing binary or hex representation
show_binary = True


# categories and their abbreviation come directly from the Unicode standard
categories = {'Lu': 'Letter, uppercase',
              'Ll': 'Letter, lowercase',
              'Lt': 'Letter, titlecase',
              'Lm': 'Letter, modifier',
              'Lo': 'Letter, other',
              'Mn': 'Mark, nonspacing',
              'Mc': 'Mark, spacing combining',
              'Me': 'Mark, enclosing',
              'Nd': 'Number, decimal digit',
              'Nl': 'Number, letter',
              'No': 'Number, other',
              'Pc': 'Punctuation, connector',
              'Pd': 'Punctuation, dash',
              'Ps': 'Punctuation, open',
              'Pe': 'Punctuation, close',
              'Pi': 'Punctuation, initial quote (may behave like Ps or Pe depending on usage)',
              'Pf': 'Punctuation, final quote (may behave like Ps or Pe depending on usage)',
              'Po': 'Punctuation, other',
              'Sm': 'Symbol, math',
              'Sc': 'Symbol, currency',
              'Sk': 'Symbol, modifier',
              'So': 'Symbol, other',
              'Zs': 'Separator, space',
              'Zl': 'Separator, line',
              'Zp': 'Separator, paragraph',
              'Cc': 'Other, control',
              'Cf': 'Other, format',
              'Cs': 'Other, surrogate',
              'Co': 'Other, private use',
              'Cn': 'Other, not assigned (including noncharacters)'}


def getCharacterInformation(c):
    return f'<p class="display-3">{c}</p>'


def getCharacterCodePoints(c):
    link = f'https://www.fileformat.info/info/unicode/char/{ord(c):06x}/index.htm'
    cp = f'<p>Code point: {ord(c):x}<sub>16</sub> = {ord(c)}<sub>10</sub> = <a target="_blank" href="{link}">U+{ord(c):06x}</a></p>'
    if ord(c) <= 0xffff:
        bmp = '<p>Code Point belongs to the <a target="_blank" href="https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane">Basic Multilingual Plane</a></p>'
    elif ord(c) <= 0x1ffff:
        bmp = '<p>Code Point belongs to the <a target="_blank" href="https://en.wikipedia.org/wiki/Plane_(Unicode)#Supplementary_Multilingual_Plane">Supplementary Multilingual Plane</a></p>'
    elif ord(c) <= 0x2ffff:
        bmp = '<p>Code Point belongs to the <a target="_blank" href="https://en.wikipedia.org/wiki/Plane_(Unicode)#Supplementary_Ideographic_Plane">Supplementary Ideographic Plane</a></p>'
    elif ord(c) <= 0x3ffff:
        bmp = '<p>Code Point belongs to the <a target="_blank" href="https://en.wikipedia.org/wiki/Plane_(Unicode)#Tertiary_Ideographic_Plane">Tertiary Ideographic Plane</a></p>'
    else:
        bmp = ''
    info = f'<p>Name: {unicodedata.name(c)}</p><p><a href="https://www.unicode.org/versions/Unicode15.0.0/ch04.pdf#G134153" target="_blank">Category</a>: {categories[unicodedata.category(c)]}</p>'
    norm = '<p>Code Point is normalized according to the <a href="https://en.wikipedia.org/wiki/Unicode_equivalence#Normalization" target="_blank">Normalization Form Canonical Decomposition (NFD)</a>.</p>' if unicodedata.is_normalized('NFD', c) else ''
    return cp + info + bmp + norm


def getCharacterEncodingUtf8(c):
    codeunit_list = list(c.encode(encoding='utf_8'))
    utf8_binary = ''
    for x in codeunit_list:
        utf8_bits = f'{x:08b}'
        if utf8_bits.startswith('0'):
            title = 'ASCII code points start with a zero'
        elif utf8_bits.startswith('110'):
            title = 'First byte of two byte code point starts with 110xxxxx'
        elif utf8_bits.startswith('1110'):
            title = 'First byte of three byte code point starts with 1110xxxx'
        elif utf8_bits.startswith('11110'):
            title = 'First byte of four byte code point starts with 11110xxx'
        elif utf8_bits.startswith('10'):
            title = 'Non-starting bytes of multi-byte code points begin with 10xxxxxx'
        else:
            title = ''
        utf8_codeunit = f'{x:08b}' if show_binary else f'0x{x:02x}'
        utf8_binary += f'<span id="{ord(c):06x}-utf8" class="codeunit border mx-1 font-monospace fw-bold" title="{title}">{utf8_codeunit}</span>'
    return utf8_binary


def getCharacterEncodingUtf16be(c):
    codeunit_list = list(c.encode(encoding='utf_16be'))
    utf16be_binary = ''
    for x in codeunit_list:
        utf16be_codeunit = f'{x:08b}' if show_binary else f'0x{x:02x}'
        utf16be_binary += f'<span id="{ord(c):06x}-utf16be" class="codeunit border mx-1 font-monospace fw-bold">{utf16be_codeunit}</span>'
    return utf16be_binary


def getCharacterEncodingUtf16le(c):
    codeunit_list = list(c.encode(encoding='utf_16'))
    utf16le_binary = ''
    for i, x in enumerate(codeunit_list):
        utf16be_codeunit = f'{x:08b}' if show_binary else f'0x{x:02x}'
        if i < 2:
            utf16le_binary += f'<span id="{ord(c):06x}-utf16lebom" class="codeunit border mx-1 font-monospace fw-bold" title="Byte Order Mark">{utf16be_codeunit}</span>'
        else:
            utf16le_binary += f'<span id="{ord(c):06x}-utf16le" class="codeunit border mx-1 font-monospace fw-bold">{utf16be_codeunit}</span>'
    return utf16le_binary


def getCharacterEncodingUtf32(c):
    codeunit_list = list(c.encode(encoding='utf_32be'))
    utf32_binary = ''
    for x in codeunit_list:
        utf32_codeunit = f'{x:08b}' if show_binary else f'0x{x:02x}'
        utf32_binary += f'<span id="{ord(c):06x}-utf32" class="codeunit border mx-1 font-monospace fw-bold">{utf32_codeunit}</span>'
    return utf32_binary


def getCharacterEncoding(c):
    s = f"""<p>UTF-8 (8-bit code units):<br/>{getCharacterEncodingUtf8(c)}</p>
            <p>UTF-16BE (16-bit code units, <a target="_blank" href="https://en.wikipedia.org/wiki/UTF-16#Byte-order_encoding_schemes">default if BOM is missing</a>):<br/>{getCharacterEncodingUtf16be(c)}</p>
            <p>UTF-16LE (16-bit code units, with <a target="_blank" href="https://en.wikipedia.org/wiki/Byte_order_mark">Byte Order Mark</a>):<br/>{getCharacterEncodingUtf16le(c)}</p>
            <p>UTF-32BE (32-bit code units):<br/>{getCharacterEncodingUtf32(c)}</p>
        """
    return s


def handle_glyph(event):
    clearCharacters()
    glyph = Element('glyph').element.value
    character_list = Element('character-list')
    character_template = Element('character-template').select('.character', from_content=True)
    for c in glyph:
        console.log(f"Character: {unicodedata.name(c)}")
        new_character = character_template.clone(f'character-{ord(c):06}')
        new_character.select('.character-info').element.innerHTML = getCharacterInformation(c)
        new_character.select('.codepoint-info').element.innerHTML = getCharacterCodePoints(c)
        new_character.select('.encoding-info').element.innerHTML = getCharacterEncoding(c)
        character_list.element.appendChild(new_character.element)


def fillTextField(glyph):
    console.log(glyph)
    input_field = Element('glyph')
    input_field.element.value = glyph
    handle_glyph(None)


def clearCharacters(event=None):
    if event:
        input_field = Element('glyph')
        input_field.element.value = ''
    character_list = Element('character-list')
    character_list.clear()
    character_list.element.innerHTML = ''


def switchNumberSystem(event):
    global show_binary
    show_binary = not show_binary
    if show_binary:
        window.localStorage.setItem('NumberSystem', 'bin')
    else:
        window.localStorage.setItem('NumberSystem', 'hex')
    handle_glyph(None)
    setNumberSystemButton()


def setNumberSystemButton():
    document.getElementById('switch-binary-button').innerHTML = '<div class="font-monospace lh-1">c7</div><div class="font-monospace lh-1">1e</div>' if show_binary else '<div class="font-monospace lh-1">10</div><div class="font-monospace lh-1">01</div>'


def setDefaultNumberSystem():
    global show_binary
    ns = window.localStorage.getItem('NumberSystem')
    console.log(f'Saved number system: {ns}')
    if not ns:
        show_binary = True
    else:
        if ns == 'bin':
            show_binary = True
        elif ns == 'hex':
            show_binary = False
    setNumberSystemButton()


document.getElementById('glyph').addEventListener('input', create_proxy(handle_glyph))
document.getElementById('clear-button').addEventListener('click', create_proxy(clearCharacters))
setDefaultNumberSystem()
