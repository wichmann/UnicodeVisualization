"""
Evaluate Unicode characters and output its data on PWA.

Info:
* https://realpython.com/pyscript-python-in-browser/#disclaimer-pyscript-is-an-experimental-project
"""

import unicodedata

from js import document, console, window, tooltipList
from pyodide.code import run_js
from pyscript.ffi import create_proxy, is_none
from pyscript import document
from pyscript.web import page, when

# global flag for choosing binary or hex representation
show_binary = True


# entered code point in modal dialog
entered_unicode_codepoint = ''


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
    norm = '<p>Code Point is normalized according to the <a href="https://en.wikipedia.org/wiki/Unicode_equivalence#Normalization" target="_blank">Normalization Form Canonical Decomposition (NFD)</a>.</p>' if unicodedata.is_normalized(
        'NFD', c) else ''
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


def handleGlyph(_):
    """
    Show all information about the current glyphs in the input text field.
    """
    clearCharacters()
    glyph = page["#glyph"][0]
    console.log(f'Processing glyph: {glyph.value}')
    # character_list = Element('character-list')
    character_list = page["#character-list"][0]
    # character_template = Element('character-template').select('.character', from_content=True)
    #character_template = page['#character-template']['.character']
    character_template = page['#character-template'][0].content.querySelector('.character')
    for c in glyph.value:
        console.log(f'Processing next character...')
        try:
            console.log(f'Character: {unicodedata.name(c)}')
            new_character = character_template.cloneNode(True) # .clone(f'character-{ord(c):06}')
            new_character.querySelector('.character-info').innerHTML = getCharacterInformation(c)
            new_character.querySelector('.codepoint-info').innerHTML = getCharacterCodePoints(c)
            new_character.querySelector('.encoding-info').innerHTML = getCharacterEncoding(c)
            character_list.appendChild(new_character)
        except ValueError as e:
            console.log('Not existing character chosen.')
            console.log(e)
            # TODO: Handle this directly in Python!
            #run_js("""
            #const toastLiveExample = document.getElementById('showErrorToast')
            #const toast = new bootstrap.Toast(toastLiveExample)
            #toast.show()
            #""")
            # toastLiveExample = page['#liveToast']
            # toast = js.bootstrap.Toast(toastLiveExample)
            # toast.show()
            clearCharacters(True)


def fillTextField(glyph):
    # get a glyph (grapheme cluster) and put it in the input text field
    console.log(glyph)
    # input_field = Element('glyph')
    input_field = page["#glyph"][0]
    input_field.value = glyph
    handleGlyph(None)


def clearCharacters(event=None):
    if event:
        # clear the input text field if call came from clear button
        # input_field = Element('glyph')
        input_field = page["#glyph"][0]
        input_field.value = ''
    # clear all HTML elements showing information about previous characters
    # character_list = Element('character-list')
    character_list = page["#character-list"][0]
    character_list.innerHTML = ''
    # character_list.html = ''
    # hide all previously shown tooltips to prevent one being still open after
    # clicking an example button
    for t in tooltipList:
        t.hide()


def switchNumberSystem(_):
    global show_binary
    show_binary = not show_binary
    if show_binary:
        window.localStorage.setItem('NumberSystem', 'bin')
    else:
        window.localStorage.setItem('NumberSystem', 'hex')
    handleGlyph(None)
    setNumberSystemButton()


def setNumberSystemButton():
    """
    Set button text depending on the global variable 'show_binary'.
    """
    hexadecimal_button_text = '<div class="font-monospace lh-1">c7</div><div class="font-monospace lh-1">1e</div>'
    binary_button_text = '<div class="font-monospace lh-1">10</div><div class="font-monospace lh-1">01</div>'
    document.getElementById('switch-binary-button').innerHTML = hexadecimal_button_text if show_binary else binary_button_text


def setDefaultNumberSystem():
    # evaluate parameter 'NumberSystem' from local storage in the browser and
    # set global variable 'show_binary' accordingly
    global show_binary
    ns = window.localStorage.getItem('NumberSystem')
    console.log(f'Saved number system: {ns}')
    if is_none(ns):
        show_binary = True
    else:
        if ns == 'bin':
            show_binary = True
        elif ns == 'hex':
            show_binary = False
    setNumberSystemButton()


def handleCodepoints(event):
    global entered_unicode_codepoint
    # codepoint = Element('unicode-codepoint').value
    codepoint = page["#unicode-codepoint"][0].value
    try:
        if codepoint.startswith('U+') or codepoint.startswith('u+'):
            entered_unicode_codepoint = chr(int(codepoint[2:], 16))
        else:
            entered_unicode_codepoint = chr(int(codepoint, 16))
    except ValueError as e:
        console.log(e)
        entered_unicode_codepoint = ''
    document.getElementById('found-code-point').innerText = entered_unicode_codepoint


def handleEnter(event):
    """
    Prevent the page from reloading when pressing enter in the modal dialog.
    """
    if event.key == 'Enter':
        event.preventDefault()
        document.getElementById('copy-character-button').click()


def clearCodepoint():
    global entered_unicode_codepoint
    entered_unicode_codepoint = ''
    codepoint = page["#unicode-codepoint"][0]
    codepoint.value = 'U+'
    document.getElementById('found-code-point').innerText = ''


# handle events for main input text field
document.getElementById('glyph').addEventListener('input', create_proxy(handleGlyph))
document.getElementById('clear-button').addEventListener('click', create_proxy(clearCharacters))

# handle events for modal dialog
document.getElementById('unicode-codepoint').addEventListener('input', create_proxy(handleCodepoints))
document.getElementById('unicode-codepoint').addEventListener('keypress', create_proxy(handleEnter))

# handle example buttons
@when("click", "#example-button-1")
def insert_example_char_1(e):
    fillTextField('a')

@when("click", "#example-button-2")
def insert_example_char_2(e):
    fillTextField('ä')

@when("click", "#example-button-3")
def insert_example_char_3(e):
    fillTextField('ä')

@when("click", "#example-button-4")
def insert_example_char_4(e):
    fillTextField('참')

@when("click", "#example-button-5")
def insert_example_char_5(e):
    fillTextField('참')

@when("click", "#example-button-6")
def insert_example_char_6(e):
    fillTextField('❦')

@when("click", "#example-button-7")
def insert_example_char_7(e):
    fillTextField('𐃅')

@when("click", "#example-button-8")
def insert_example_char_8(e):
    fillTextField('🤓')

@when("click", "#example-button-9")
def insert_example_char_9(e):
    fillTextField('👩🏾‍🎤')

@when("click", "#example-button-10")
def insert_example_char_10(e):
    fillTextField('द्ध्र्य')

@when("click", "#example-button-11")
def insert_example_char_11(e):
    fillTextField('ﷺ')

@when("click", "#example-button-12")
def insert_example_char_12(e):
    fillTextField('שָׁלוֹם')

@when("click", "#switch-binary-button")
def switch_button_handler(e):
    switchNumberSystem(None)

@when("click", "#close-modal-button")
def close_modal_handler(e):
    clearCodepoint()

@when("click", "#remove-codepoint-button")
def remove_codepoint_handler(e):
    clearCodepoint()

@when("click", "#copy-character-button")
def copy_character_handler(e):
    fillTextField(entered_unicode_codepoint)
    clearCodepoint()

# load chosen number system from local storage and set button text
setDefaultNumberSystem()
