from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Max
from django.utils import timezone

import base64, tempfile, os
from django.core.files.base import ContentFile

from apps.writing.models import WritingSubmission
from apps.speaking.models import SpeakingSubmission
from apps.reading.models import ReadingTest, ReadingPassage, QuestionGroup, Question
from apps.listening.models import ListeningTest, ListeningSection, ListeningQuestion

from .forms import (
    ReadingTestForm, ReadingPassageForm, QuestionGroupForm, ReadingQuestionForm,
    ListeningTestForm, ListeningSectionForm, ListeningQuestionForm,
)
from .html_import import parse_reading_html, parse_listening_html


def teacher_required(view_func):
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return redirect('core:landing')
        return view_func(request, *args, **kwargs)
    return wrapper


# ── Review queue ──────────────────────────────────────────────────────────────

@login_required
@teacher_required
def dashboard(request):
    writing_queue = WritingSubmission.objects.filter(
        status=WritingSubmission.STATUS_SUBMITTED
    ).select_related('user', 'task').order_by('submitted_at')
    speaking_queue = SpeakingSubmission.objects.filter(
        status=SpeakingSubmission.STATUS_SUBMITTED
    ).select_related('user', 'part').order_by('submitted_at')
    context = {
        'writing_queue':  writing_queue[:10],
        'speaking_queue': speaking_queue[:10],
        'writing_count':  writing_queue.count(),
        'speaking_count': speaking_queue.count(),
    }
    return render(request, 'teachers/dashboard.html', context)


@login_required
@teacher_required
def review_writing(request, submission_pk):
    submission = get_object_or_404(WritingSubmission, pk=submission_pk)
    if request.method == 'POST':
        submission.band_task_response = request.POST.get('band_task_response')
        submission.band_coherence     = request.POST.get('band_coherence')
        submission.band_lexical       = request.POST.get('band_lexical')
        submission.band_grammar       = request.POST.get('band_grammar')
        submission.teacher_comment    = request.POST.get('teacher_comment', '')
        submission.corrected_text     = request.POST.get('corrected_text', '')
        submission.teacher            = request.user
        submission.status             = WritingSubmission.STATUS_REVIEWED
        submission.compute_overall()
        submission.reviewed_at = timezone.now()
        submission.save()
        return redirect('teachers:dashboard')
    return render(request, 'teachers/review_writing.html', {'submission': submission})


@login_required
@teacher_required
def review_speaking(request, submission_pk):
    submission = get_object_or_404(SpeakingSubmission, pk=submission_pk)
    if request.method == 'POST':
        submission.band_fluency      = request.POST.get('band_fluency')
        submission.band_lexical      = request.POST.get('band_lexical')
        submission.band_grammar      = request.POST.get('band_grammar')
        submission.band_pronunciation = request.POST.get('band_pronunciation')
        submission.teacher_comment   = request.POST.get('teacher_comment', '')
        submission.teacher           = request.user
        submission.status            = SpeakingSubmission.STATUS_REVIEWED
        scores = [submission.band_fluency, submission.band_lexical,
                  submission.band_grammar, submission.band_pronunciation]
        valid = [float(s) for s in scores if s]
        if valid:
            submission.overall_band = round(sum(valid) / len(valid) * 2) / 2
        submission.reviewed_at = timezone.now()
        submission.save()
        return redirect('teachers:dashboard')
    return render(request, 'teachers/review_speaking.html', {'submission': submission})


# ── Reading content management ────────────────────────────────────────────────

@login_required
@teacher_required
def reading_tests(request):
    if request.method == 'POST':
        form = ReadingTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()
            return redirect('teachers:reading_test_edit', pk=test.pk)
    else:
        form = ReadingTestForm()
    tests = ReadingTest.objects.order_by('-created_at')
    return render(request, 'teachers/reading_tests.html', {'tests': tests, 'form': form})


@login_required
@teacher_required
def reading_test_edit(request, pk):
    test = get_object_or_404(ReadingTest, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_test':
            # Only update editable fields — never touch is_published here
            test.title            = request.POST.get('title', test.title).strip()
            test.test_type        = request.POST.get('test_type', test.test_type)
            try:
                test.duration_minutes = int(request.POST.get('duration_minutes', test.duration_minutes))
            except (ValueError, TypeError):
                pass
            test.save(update_fields=['title', 'test_type', 'duration_minutes'])
            return redirect('teachers:reading_test_edit', pk=pk)

        elif action == 'add_passage':
            pform = ReadingPassageForm(request.POST)
            if pform.is_valid():
                passage = pform.save(commit=False)
                passage.test = test
                passage.save()
                return redirect('teachers:reading_passage_edit', pk=passage.pk)
            form = ReadingTestForm(instance=test)
            passages = test.passages.all()
            return render(request, 'teachers/reading_test_edit.html',
                          {'test': test, 'form': form, 'pform': pform, 'passages': passages})

        elif action == 'delete_passage':
            ReadingPassage.objects.filter(pk=request.POST.get('passage_pk'), test=test).delete()
            return redirect('teachers:reading_test_edit', pk=pk)

        elif action == 'toggle_publish':
            test.is_published = not test.is_published
            test.save()
            return redirect('teachers:reading_test_edit', pk=pk)

        elif action == 'import_html':
            html_file = request.FILES.get('html_file')
            part_mode = request.POST.get('part_mode', 'single')
            part_number = int(request.POST.get('part_number', 1))

            if html_file:
                html_content = html_file.read().decode('utf-8', errors='replace')
                passages_data = parse_reading_html(html_content)

                if part_mode == 'single':
                    # Only import the first passage, set order = part_number
                    if passages_data:
                        _create_reading_passage(test, passages_data[0], part_number)
                else:
                    # Full import: use order from parsed data (1-based index)
                    for idx, pdata in enumerate(passages_data, start=1):
                        _create_reading_passage(test, pdata, idx)

            return redirect('teachers:reading_test_edit', pk=pk)

    form  = ReadingTestForm(instance=test)
    pform = ReadingPassageForm(initial={'order': test.passages.count() + 1})
    passages = test.passages.prefetch_related('question_groups__questions').all()
    return render(request, 'teachers/reading_test_edit.html',
                  {'test': test, 'form': form, 'pform': pform, 'passages': passages})


@login_required
@teacher_required
def reading_passage_edit(request, pk):
    passage = get_object_or_404(ReadingPassage, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_passage':
            form = ReadingPassageForm(request.POST, instance=passage)
            if form.is_valid():
                form.save()
            return redirect('teachers:reading_passage_edit', pk=pk)

        elif action == 'add_group':
            gform = QuestionGroupForm(request.POST)
            if gform.is_valid():
                grp = gform.save(commit=False)
                grp.passage = passage
                grp.save()
            return redirect('teachers:reading_passage_edit', pk=pk)

        elif action == 'delete_group':
            QuestionGroup.objects.filter(pk=request.POST.get('group_pk'), passage=passage).delete()
            return redirect('teachers:reading_passage_edit', pk=pk)

        elif action == 'add_question':
            group = get_object_or_404(QuestionGroup, pk=request.POST.get('group_pk'), passage=passage)
            qform = ReadingQuestionForm(request.POST)
            if qform.is_valid():
                q = qform.save(commit=False)
                q.group = group
                q.save()
            return HttpResponseRedirect(
                reverse('teachers:reading_passage_edit', kwargs={'pk': pk}) + f'#group-{group.pk}'
            )

        elif action == 'edit_question':
            q = get_object_or_404(Question, pk=request.POST.get('q_pk'), group__passage=passage)
            group_pk = q.group_id
            try:
                q.number = int(request.POST.get('number', q.number))
            except (ValueError, TypeError):
                pass
            q.text           = request.POST.get('text', q.text).strip()
            q.correct_answer = request.POST.get('correct_answer', q.correct_answer).strip()
            if q.group.question_type == 'mcq':
                q.option_a = request.POST.get('option_a', '').strip()
                q.option_b = request.POST.get('option_b', '').strip()
                q.option_c = request.POST.get('option_c', '').strip()
                q.option_d = request.POST.get('option_d', '').strip()
            q.save()
            return HttpResponseRedirect(
                reverse('teachers:reading_passage_edit', kwargs={'pk': pk}) + f'#group-{group_pk}'
            )

        elif action == 'delete_question':
            q = Question.objects.filter(
                pk=request.POST.get('q_pk'), group__passage=passage
            ).select_related('group').first()
            group_pk = q.group_id if q else None
            if q:
                q.delete()
            anchor = f'#group-{group_pk}' if group_pk else ''
            return HttpResponseRedirect(
                reverse('teachers:reading_passage_edit', kwargs={'pk': pk}) + anchor
            )

    form   = ReadingPassageForm(instance=passage)
    gform  = QuestionGroupForm(initial={'order': passage.question_groups.count() + 1})
    groups = passage.question_groups.prefetch_related('questions').annotate(max_q_num=Max('questions__number')).all()
    tfng_choices     = [('True', 'True'), ('False', 'False'), ('Not Given', 'Not Given')]
    mcq_option_fields = [('A', 'option_a'), ('B', 'option_b'), ('C', 'option_c'), ('D', 'option_d')]
    return render(request, 'teachers/reading_passage_edit.html',
                  {'passage': passage, 'form': form, 'gform': gform,
                   'groups': groups, 'tfng_choices': tfng_choices,
                   'mcq_option_fields': mcq_option_fields})


# ── Listening content management ──────────────────────────────────────────────

@login_required
@teacher_required
def listening_tests(request):
    if request.method == 'POST':
        form = ListeningTestForm(request.POST)
        if form.is_valid():
            test = form.save()
            return redirect('teachers:listening_test_edit', pk=test.pk)
    else:
        form = ListeningTestForm()
    tests = ListeningTest.objects.order_by('-created_at')
    return render(request, 'teachers/listening_tests.html', {'tests': tests, 'form': form})


@login_required
@teacher_required
def listening_test_edit(request, pk):
    test = get_object_or_404(ListeningTest, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_test':
            test.title = request.POST.get('title', test.title).strip()
            try:
                test.duration_minutes = int(request.POST.get('duration_minutes', test.duration_minutes))
            except (ValueError, TypeError):
                pass
            if 'audio_file' in request.FILES:
                test.audio_file = request.FILES['audio_file']
            test.save()
            return redirect('teachers:listening_test_edit', pk=pk)

        elif action == 'add_section':
            sform = ListeningSectionForm(request.POST, request.FILES)
            if sform.is_valid():
                section = sform.save(commit=False)
                section.test = test
                section.save()
                return redirect('teachers:listening_section_edit', pk=section.pk)
            form = ListeningTestForm(instance=test)
            sections = test.sections.prefetch_related('questions').all()
            return render(request, 'teachers/listening_test_edit.html',
                          {'test': test, 'form': form, 'sform': sform, 'sections': sections})

        elif action == 'delete_section':
            ListeningSection.objects.filter(pk=request.POST.get('section_pk'), test=test).delete()
            return redirect('teachers:listening_test_edit', pk=pk)

        elif action == 'toggle_publish':
            test.is_published = not test.is_published
            test.save()
            return redirect('teachers:listening_test_edit', pk=pk)

        elif action == 'import_html':
            html_file = request.FILES.get('html_file')
            part_mode = request.POST.get('part_mode', 'single')
            part_number = int(request.POST.get('part_number', 1))

            if html_file:
                html_content = html_file.read().decode('utf-8', errors='replace')
                parsed = parse_listening_html(html_content)

                # Save embedded audio to the section or test
                audio_src = parsed.get('audio_src')

                if part_mode == 'single':
                    sections_data = parsed.get('sections', [])
                    if sections_data:
                        _create_listening_section(test, sections_data[0], part_number, audio_src)
                else:
                    for idx, sdata in enumerate(parsed.get('sections', []), start=1):
                        _create_listening_section(test, sdata, idx,
                                                  audio_src if idx == 1 else None)

            return redirect('teachers:listening_test_edit', pk=pk)

    form     = ListeningTestForm(instance=test)
    sform    = ListeningSectionForm(initial={'order': test.sections.count() + 1})
    sections = test.sections.prefetch_related('questions').all()
    return render(request, 'teachers/listening_test_edit.html',
                  {'test': test, 'form': form, 'sform': sform, 'sections': sections})


@login_required
@teacher_required
def listening_section_edit(request, pk):
    section = get_object_or_404(ListeningSection, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_section':
            form = ListeningSectionForm(request.POST, request.FILES, instance=section)
            if form.is_valid():
                form.save()
            return redirect('teachers:listening_section_edit', pk=pk)

        elif action == 'add_question':
            qform = ListeningQuestionForm(request.POST)
            if qform.is_valid():
                q = qform.save(commit=False)
                q.section = section
                q.save()
            return HttpResponseRedirect(
                reverse('teachers:listening_section_edit', kwargs={'pk': pk}) + '#questions'
            )

        elif action == 'edit_question':
            q = get_object_or_404(ListeningQuestion, pk=request.POST.get('q_pk'), section=section)
            try:
                q.number = int(request.POST.get('number', q.number))
            except (ValueError, TypeError):
                pass
            q.text           = request.POST.get('text', q.text).strip()
            q.correct_answer = request.POST.get('correct_answer', q.correct_answer).strip()
            if q.question_type == 'mcq':
                q.option_a = request.POST.get('option_a', '').strip()
                q.option_b = request.POST.get('option_b', '').strip()
                q.option_c = request.POST.get('option_c', '').strip()
                q.option_d = request.POST.get('option_d', '').strip()
            q.save()
            return HttpResponseRedirect(
                reverse('teachers:listening_section_edit', kwargs={'pk': pk}) + '#questions'
            )

        elif action == 'delete_question':
            ListeningQuestion.objects.filter(pk=request.POST.get('q_pk'), section=section).delete()
            return HttpResponseRedirect(
                reverse('teachers:listening_section_edit', kwargs={'pk': pk}) + '#questions'
            )

    form      = ListeningSectionForm(instance=section)
    questions = section.questions.all()
    next_q_num = (section.questions.aggregate(Max('number'))['number__max'] or 0) + 1
    mcq_option_fields = [('A', 'option_a'), ('B', 'option_b'), ('C', 'option_c'), ('D', 'option_d')]
    return render(request, 'teachers/listening_section_edit.html',
                  {'section': section, 'form': form, 'questions': questions,
                   'next_q_num': next_q_num, 'mcq_option_fields': mcq_option_fields})


# ── HTML import helpers ───────────────────────────────────────────────────────

def _create_reading_passage(test, pdata, order):
    passage = ReadingPassage.objects.create(
        test=test,
        order=order,
        title=pdata.get('title', 'Passage'),
        source=pdata.get('source', ''),
        content=pdata.get('content', ''),
    )
    for gdata in pdata.get('groups', []):
        grp = QuestionGroup.objects.create(
            passage=passage,
            question_type=gdata.get('type', 'fill'),
            instructions=gdata.get('instructions', ''),
            order=QuestionGroup.objects.filter(passage=passage).count() + 1,
        )
        for qdata in gdata.get('questions', []):
            Question.objects.create(
                group=grp,
                number=qdata.get('number', 0),
                text=qdata.get('text', ''),
                correct_answer=qdata.get('answer', ''),
                option_a=qdata.get('option_a', ''),
                option_b=qdata.get('option_b', ''),
                option_c=qdata.get('option_c', ''),
                option_d=qdata.get('option_d', ''),
            )
    return passage


def _create_listening_section(test, sdata, order, audio_src=None):
    section = ListeningSection.objects.create(
        test=test,
        order=order,
        title=sdata.get('title', f'Section {order}'),
        description=sdata.get('description', ''),
    )
    if audio_src and audio_src.startswith('data:audio'):
        try:
            header, b64data = audio_src.split(',', 1)
            ext = 'mp3'
            if 'ogg' in header:
                ext = 'ogg'
            elif 'wav' in header:
                ext = 'wav'
            audio_bytes = base64.b64decode(b64data)
            section.audio_file.save(
                f'section_{test.pk}_{order}.{ext}',
                ContentFile(audio_bytes),
                save=True,
            )
        except Exception:
            pass

    for qdata in sdata.get('questions', []):
        ListeningQuestion.objects.create(
            section=section,
            number=qdata.get('number', 0),
            text=qdata.get('text', ''),
            question_type=qdata.get('type', 'fill'),
            correct_answer=qdata.get('answer', ''),
            option_a=qdata.get('option_a', ''),
            option_b=qdata.get('option_b', ''),
            option_c=qdata.get('option_c', ''),
            option_d=qdata.get('option_d', ''),
        )
    return section
