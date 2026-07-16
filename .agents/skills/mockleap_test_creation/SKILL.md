---
name: MockLeap Test Creation
description: Guidelines and HTML structures for adding new Reading and Listening tests to the MockLeap database. Use this when the user asks to add or create a new test, populate test data, or integrate exam materials.
---
# MockLeap Test Creation Guide

MockLeap uses a hybrid-static approach for exam questions. 
Instead of complex relational models for Questions and Options, we store:
1. `questions_html` (TextField): The styled raw HTML for the questions section.
2. `answer_key` (JSONField): A simple JSON dictionary mapping question numbers to answers.

## General Rules
- Do NOT create `Question` or `QuestionGroup` models. They were deleted.
- Use `data-qhl="q{id}"` on question text elements (`.q-text`) to enable the user highlighting feature. For Listening tests, ensure the parent wrapper `.ml-freeform-questions` has `data-qhl="ls-sec-{index}"` so highlighting works anywhere in the section.
- Use `.q-block` for question wrappers (it uses CSS Grid: 1st col for `.q-num`, 2nd col for the rest).
- Use `.q-num` for the IELTS-style black circle numbers. It supports wide text (like "18-20") automatically via `min-width`.
- Use `.ml-input-inline` for fill-in-the-blank text inputs. We recommend adding `style="width:110px;"` for standard blanks, and `style="width:50px; text-transform:uppercase;"` for multiple-choice-multiple-answer letters.
- For Notes completion in tables, use standard HTML `<table>`, `<tr>`, and `<td>` for perfect vertical alignment rather than using `<br>` or Tailwind grids.
- All inputs MUST have a `name` attribute matching the question number, e.g., `name="q1"`.
- Provide an `answer_key` dict where keys are strings of the question number, e.g., `{"1": "TRUE", "2": "apple"}`.

## Example: HTML Construction
```html
<div class="q-group-header">
  <div class="q-group-type">Note Completion</div>
</div>
<!-- Question Text with Highlighting Support -->
<div class="q-block">
  <div class="q-num">1</div>
  <div class="q-text" data-qhl="q1">
    Early uses of silk included <input type="text" name="q1" class="ml-input-inline" style="width:110px;">
  </div>
</div>

<!-- TFNG Options -->
<div class="q-block">
  <div class="q-num">2</div>
  <div class="q-text" data-qhl="q2">The text agrees with this statement.</div>
  <div class="tfng-options">
    <label class="tfng-label"><input type="radio" name="q2" value="TRUE"> <span>TRUE</span></label>
    <label class="tfng-label"><input type="radio" name="q2" value="FALSE"> <span>FALSE</span></label>
    <label class="tfng-label"><input type="radio" name="q2" value="NOT GIVEN"> <span>NOT GIVEN</span></label>
  </div>
</div>
```

## Data Population
```python
from apps.reading.models import ReadingTest, ReadingPassage

test = ReadingTest.objects.create(
    title="Volume X Test Y",
    test_type='academic',
    duration_minutes=60,
    is_published=True,
    created_by=admin_user
)

p1_content = "Passage text here..."
p1_questions = \"\"\"(Use beautiful HTML format shown above)\"\"\"
p1_answers = {"1": "clothing", "2": "TRUE"}

ReadingPassage.objects.create(
    test=test, order=1, title="The Silk Industry",
    content=p1_content, source="Volume X",
    questions_html=p1_questions, answer_key=p1_answers
)
```
