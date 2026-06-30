"""
MockLeap HTML import utilities.

Expected HTML format for reading:

  <div class="ml-passage" data-title="..." data-source="...">
    <p>Paragraph 1</p>
    <p>Paragraph 2</p>
  </div>
  <div class="ml-question-group" data-type="mcq|tfng|fill|table|note|summary|match|short"
       data-instructions="...">
    <div class="ml-question" data-number="1" data-answer="B">
      <p class="ml-text">Question stem</p>
      <p class="ml-option-a">Option A</p>  <!-- only for mcq -->
      <p class="ml-option-b">Option B</p>
      <p class="ml-option-c">Option C</p>
      <p class="ml-option-d">Option D</p>
    </div>
  </div>

Expected HTML format for listening:

  <audio class="ml-audio" src="data:audio/mpeg;base64,..." controls></audio>
  <div class="ml-section" data-title="Section 1 — ..." data-description="...">
    <div class="ml-question" data-number="1" data-type="fill" data-answer="London">
      <p class="ml-text">The city is ______</p>
    </div>
    <div class="ml-question" data-number="2" data-type="mcq" data-answer="B">
      <p class="ml-text">What does he prefer?</p>
      <p class="ml-option-a">A</p>
      <p class="ml-option-b">B</p>
      <p class="ml-option-c">C</p>
    </div>
  </div>
"""

from html.parser import HTMLParser


class _StackParser(HTMLParser):
    """Build a simple element tree from HTML."""

    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__()
        self._root = _El('#root', {})
        self._stack = [self._root]

    def handle_starttag(self, tag, attrs):
        el = _El(tag, dict(attrs))
        self._stack[-1].children.append(el)
        if tag not in self.VOID:
            self._stack.append(el)

    def handle_endtag(self, tag):
        for i in range(len(self._stack) - 1, 0, -1):
            if self._stack[i].tag == tag:
                self._stack = self._stack[:i]
                return

    def handle_data(self, data):
        self._stack[-1].text += data

    @property
    def root(self):
        return self._root


class _El:
    __slots__ = ('tag', 'attrs', 'text', 'children')

    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs
        self.text = ''
        self.children = []

    def cls(self):
        return self.attrs.get('class', '').split()

    def get(self, key, default=''):
        return self.attrs.get(key, default)

    def all_text(self):
        parts = [self.text]
        for ch in self.children:
            parts.append(ch.all_text())
        return ' '.join(p.strip() for p in parts if p.strip())

    def find_all_cls(self, cls_name):
        results = []
        for ch in self.children:
            if cls_name in ch.cls():
                results.append(ch)
            results.extend(ch.find_all_cls(cls_name))
        return results

    def find_cls(self, cls_name):
        for ch in self.children:
            if cls_name in ch.cls():
                return ch
            found = ch.find_cls(cls_name)
            if found:
                return found
        return None

    def find_tag(self, tag_name):
        for ch in self.children:
            if ch.tag == tag_name:
                return ch
            found = ch.find_tag(tag_name)
            if found:
                return found
        return None


def _parse_html(html_content):
    p = _StackParser()
    p.feed(html_content)
    return p.root


import re as _re

_OPT_PREFIX = _re.compile(r'^[A-Da-d][.)]\s*')


def _clean_option(text):
    """Strip leading letter prefix like 'A.' 'B)' 'C. ' from MCQ option text."""
    return _OPT_PREFIX.sub('', text).strip()


def _parse_question(q_el):
    q = {
        'number': int(q_el.get('data-number', 0) or 0),
        'answer': q_el.get('data-answer', '').strip(),
        'text': '',
        'option_a': '',
        'option_b': '',
        'option_c': '',
        'option_d': '',
    }
    for ch in q_el.children:
        cls = ch.cls()
        txt = ch.all_text().strip()
        if 'ml-text' in cls:
            q['text'] = txt
        elif 'ml-option-a' in cls:
            q['option_a'] = _clean_option(txt)
        elif 'ml-option-b' in cls:
            q['option_b'] = _clean_option(txt)
        elif 'ml-option-c' in cls:
            q['option_c'] = _clean_option(txt)
        elif 'ml-option-d' in cls:
            q['option_d'] = _clean_option(txt)
    return q


def parse_reading_html(html_content):
    """
    Parse a reading import HTML.
    Returns list of passage dicts:
      [{'title', 'source', 'content', 'groups': [{'type', 'instructions', 'questions': [...]}]}]
    """
    root = _parse_html(html_content)
    passages = []

    for passage_el in root.find_all_cls('ml-passage'):
        title = passage_el.get('data-title') or 'Passage'
        source = passage_el.get('data-source', '')
        paras = [ch.all_text() for ch in passage_el.children
                 if ch.tag == 'p' and ch.all_text()]
        content = '\n\n'.join(paras)
        passages.append({
            'title': title,
            'source': source,
            'content': content,
            'groups': [],
        })

    for grp_el in root.find_all_cls('ml-question-group'):
        qtype = grp_el.get('data-type', 'fill')
        instructions = grp_el.get('data-instructions', '')
        questions = [_parse_question(q) for q in grp_el.find_all_cls('ml-question')]

        # If no passages yet (malformed), create one
        if not passages:
            passages.append({'title': 'Passage', 'source': '', 'content': '', 'groups': []})

        passages[-1]['groups'].append({
            'type': qtype,
            'instructions': instructions,
            'questions': questions,
        })

    return passages


def parse_listening_html(html_content):
    """
    Parse a listening import HTML.
    Returns:
      {
        'audio_src': str or None,   # data URI or empty
        'sections': [{'title', 'description', 'questions': [...]}]
      }
    """
    root = _parse_html(html_content)
    audio_src = None

    audio_el = root.find_cls('ml-audio')
    if audio_el:
        src = audio_el.get('src', '')
        if src.startswith('data:audio'):
            audio_src = src

    sections = []
    for sec_el in root.find_all_cls('ml-section'):
        title = sec_el.get('data-title') or 'Section'
        description = sec_el.get('data-description', '')
        questions = []
        for q_el in sec_el.find_all_cls('ml-question'):
            q = _parse_question(q_el)
            q['type'] = q_el.get('data-type', 'fill')
            questions.append(q)
        sections.append({
            'title': title,
            'description': description,
            'questions': questions,
        })

    return {'audio_src': audio_src, 'sections': sections}
