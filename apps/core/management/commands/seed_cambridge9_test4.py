"""
python manage.py seed_cambridge9_test4

Adds a Reading test (3 passages, 40 questions) and a Listening test
(4 sections, 40 questions) that mirror the structure of Cambridge IELTS 9 Test 4.
The passage text and audio scripts are original IELTS-style content —
replace them through the teacher interface with actual Cambridge material.

Safe to run multiple times: skips if the test title already exists.
"""
from django.core.management.base import BaseCommand


READING_PASSAGE_1 = """\
The Remarkable Abilities of Savants

In 1887, physician J. Langdon Down gave a name to a syndrome he had observed
throughout his career: individuals with serious developmental or mental
disabilities who nonetheless possessed extraordinary abilities in a specific
field. He called them "idiot savants", a term that has since been replaced by
the more respectful "savant syndrome". Today, researchers estimate that savant
syndrome occurs in roughly one in a million people, though milder forms may be
considerably more common.

The abilities displayed by savants are strikingly consistent across cases.
Musical genius is perhaps the most frequently documented — many savants can
play a complex piece of music after hearing it only once, despite having no
formal training and limited ability to communicate. The British pianist Derek
Paravicini, born blind and with severe learning difficulties, can reproduce
virtually any piece of music after a single hearing and has performed at
Carnegie Hall. Calendar calculation is another common savant skill: given any
date, past or future, a calendar savant can immediately identify the day of the
week, often calculating thousands of years into the future without apparent
effort or understanding of how they do it.

Visual art provides further examples. Kim Peek, the man who inspired the film
Rain Man, could read two pages of a book simultaneously — one with each eye —
and had memorised the contents of over 12,000 books. Stephen Wiltshire, an
autistic British artist, can draw entire cityscapes in intricate detail after
a single helicopter flight over a city. His panoramic drawings of Tokyo, Rome,
Hong Kong and New York have been exhibited internationally and praised for
their architectural precision.

Researchers have proposed several competing theories to explain savant syndrome.
One prominent hypothesis centres on the concept of "cortical release". According
to this view, all human brains possess latent abilities that are ordinarily
suppressed by higher cortical functioning. When certain regions of the left
hemisphere are damaged — through injury, disease or developmental anomaly —
right-hemisphere functions are paradoxically enhanced. Patients who acquire
savant-like skills following a stroke or brain injury appear to support this
model. Bruce Miller at the University of California documented patients with
frontotemporal dementia who suddenly developed remarkable artistic abilities as
their left hemisphere deteriorated.

A second theory focuses on abnormal connectivity. Brain imaging studies suggest
that savants show unusual patterns of neural wiring, with weaker connections
between frontal control regions and stronger connections between lower-level
perceptual and memory systems. This may allow savants to access raw perceptual
data that most people's brains automatically filter and discard — enabling
calendar savants, for instance, to perform what appears to be unconscious
pattern-matching across vast datasets of dates.

Allan Snyder of the University of Sydney has pursued a more controversial line
of enquiry. He has used transcranial magnetic stimulation (TMS) to temporarily
suppress left-hemisphere activity in neurotypical subjects, claiming that
some subjects temporarily display savant-like enhancements in drawing ability
or calendar calculation. His work suggests that savant abilities may lie dormant
in all humans, accessible in principle if the right inhibitory circuits can be
switched off. Critics, however, point out that the effect sizes in such studies
are small and difficult to replicate.

Whether or not savant abilities are truly universal in potential, they raise
profound questions about how the brain stores and processes information. Standard
models of memory emphasise the reconstructive nature of recall — we do not
replay memories like video recordings, but rebuild them from fragments,
influenced by emotion, expectation and subsequent experience. Savants, with their
near-perfect retention of specific categories of information, appear to operate
according to a different model — one that is, paradoxically, both more powerful
and more limited than ordinary memory.

The paradox of savant syndrome — extraordinary ability coexisting with
significant disability — challenges simplistic notions of intelligence as a
single, unified capacity. It supports instead a modular view of cognition in
which the brain comprises many semi-independent systems, each capable, in
principle, of functioning at an exceptional level. What savants demonstrate,
above all, is that the boundaries of human cognitive possibility are far wider
than everyday experience suggests.
"""

READING_PASSAGE_2 = """\
The Urban Farming Revolution

Across the rooftops of Singapore, in converted warehouses in Detroit, on
vertical towers in Tokyo shopping malls and in hydroponic tunnels beneath the
streets of London, a quiet agricultural revolution is under way. Urban farming —
the cultivation of food within city boundaries — has moved from the fringes of
alternative lifestyles to a subject of serious interest for city planners,
venture capitalists and food security researchers. The global urban farming
market was valued at approximately $170 billion in 2022 and is projected to
exceed $280 billion by 2030, driven by growing urban populations, climate
anxiety and technological advances in controlled-environment agriculture.

Advocates argue that urban farming addresses multiple challenges simultaneously.
By shortening supply chains, it reduces the carbon emissions associated with
long-distance food transport — an important consideration given that the average
food item in a Western supermarket travels more than 1,500 kilometres before
reaching a plate. Urban farms also recapture land from impermeable surfaces,
potentially reducing urban heat-island effects and stormwater runoff. In cities
where fresh produce is expensive and difficult to obtain — so-called "food
deserts" — rooftop gardens and community plots can improve local food access for
low-income residents.

Perhaps the most dramatic development in urban agriculture is the rise of
vertical farming, in which crops are grown in stacked layers inside
climate-controlled warehouses, illuminated by LED lights calibrated to maximise
plant growth. Vertical farms use up to 95% less water than conventional
agriculture through closed-loop hydroponic systems. Since they are entirely
enclosed, they require no pesticides and are unaffected by extreme weather
events or seasonal variation. A vertical farm in New Jersey, operated by AeroFarms
before its bankruptcy in 2023, produced 2 million pounds of leafy greens
annually in a former steel mill covering roughly 7,000 square metres.

Critics of urban farming, however, point to significant limitations. The energy
consumption of indoor vertical farms is substantial: LED lighting, climate
control and water circulation systems can make the carbon footprint per kilogram
of produce significantly higher than conventional field agriculture, depending
on the electricity grid in use. A 2019 study published in Nature Plants
calculated that lettuce grown in a vertical farm in the UK produced up to 50
times more carbon per kilogram than field-grown lettuce, once the electricity
used was accounted for. This arithmetic improves as electricity grids
decarbonise, but currently represents a significant obstacle.

The economics present further challenges. Capital costs for vertical farms are
extremely high — building and equipping a commercial facility can cost tens of
millions of dollars — and operating costs, dominated by energy and labour,
make it difficult to achieve profitability. Most vertical farms focus on
high-value, short-cycle crops such as salad leaves, herbs and microgreens, which
can bear the high cost of production. Staple crops such as wheat, rice and
potatoes — which provide the bulk of human caloric intake — are generally
impractical to grow vertically. Urban farming, in this sense, can at best
supplement rather than replace conventional agriculture for the foreseeable
future.

Community and social dimensions of urban farming deserve consideration too.
In cities across Europe and North America, community gardens have served for
decades as spaces of social connection, mental health recovery and cultural
identity — particularly for immigrant communities who cultivate plants from
their home regions. Research from the Netherlands has found that people living
near urban green spaces, including community gardens, report significantly
higher levels of wellbeing and social cohesion. These benefits are difficult
to quantify economically but represent a compelling case for supporting urban
agriculture beyond its direct food production value.

The future of urban farming likely lies in integration: combining the
technological sophistication of controlled-environment agriculture with
thoughtful urban planning and community engagement. Cities including Amsterdam,
Singapore and Melbourne have begun incorporating urban food production into
building codes and planning frameworks, requiring new developments above a
certain size to include green space that can accommodate food growing. Whether
through high-tech vertical farms or low-tech community plots, urban agriculture
is increasingly recognised as an essential component of resilient, sustainable
cities.
"""

READING_PASSAGE_3 = """\
How We Decide: The Neuroscience of Choice

Every waking moment, the human brain makes decisions. Most are trivial — which
shoe to put on first, which route to take to work — and are made largely
automatically, below the threshold of conscious awareness. Others are
consequential and demand deliberate reasoning. Understanding the neural
mechanisms that underpin decision-making has become one of the most active areas
in cognitive neuroscience, with implications ranging from economics and public
policy to clinical treatment of addiction and depression.

Early theories of decision-making, influenced by classical economics, assumed
that humans are rational agents who evaluate options systematically and choose
the one that maximises expected utility. This view was challenged decisively by
the work of psychologists Daniel Kahneman and Amos Tversky in the 1970s and
1980s. Their research revealed systematic, predictable biases in human judgment
that deviate markedly from the rational-agent model. People, they showed, are
disproportionately averse to losses relative to equivalent gains — a
phenomenon they termed "loss aversion". They also demonstrated that the framing
of options — how choices are presented — strongly influences decisions, even
when the underlying information is identical.

Neuroscientific research has since provided a biological basis for these
observations. Brain imaging studies consistently identify the prefrontal cortex
as a central hub for deliberate, goal-directed decision-making. This region,
particularly the ventromedial prefrontal cortex, integrates information from
memory, perception and emotional systems to produce value signals that guide
choice. Crucially, the prefrontal cortex interacts constantly with the amygdala
— a structure associated with emotional processing and threat detection — and
with dopaminergic circuits originating in the midbrain. This interaction
reflects the emotional dimension of decision-making that classical economics
overlooked.

The role of dopamine in decision-making has been studied extensively. This
neurotransmitter is not simply a "pleasure chemical", as popular accounts
sometimes suggest, but is more accurately described as a signal of prediction
error — the gap between expected and actual outcomes. When outcomes are better
than anticipated, dopamine neurons fire, reinforcing the behaviour that led to
the positive result. When outcomes are worse than expected, dopamine activity
decreases, making similar choices less likely in future. This system underlies
the capacity to learn from experience, but it also makes humans vulnerable to
addiction: substances that artificially stimulate dopamine release can hijack
the learning system, creating powerful urges that override deliberate reasoning.

Dual-process theory, popularised by Kahneman's book Thinking, Fast and Slow,
proposes that human cognition operates through two distinct systems. System 1
is fast, automatic and largely unconscious, drawing on heuristics and emotional
responses to generate rapid judgments. System 2 is slow, effortful and
deliberate, capable of logical reasoning but requiring significant cognitive
resources to engage. Most everyday decisions are handled by System 1, with
System 2 engaged only when System 1 signals uncertainty or when a problem is
explicitly flagged as requiring careful analysis. Research has shown that
cognitive load — tasks that occupy System 2 resources — leads people to rely
more heavily on System 1 heuristics, increasing susceptibility to biases.

The influence of social context on decision-making represents another major
research theme. Humans are profoundly social creatures, and choices are rarely
made in isolation. Studies using economic games such as the Ultimatum Game —
in which one player offers a division of a sum of money and the other must
accept or reject it — have demonstrated that people routinely sacrifice
financial gain to punish partners who make what they perceive as unfair offers.
Brain imaging during these games reveals activity in the anterior insula, a
region associated with disgust and moral emotion, as well as in the prefrontal
cortex. The balance between these systems determines whether an individual
accepts an unfair but financially rational offer or rejects it on principle.

Understanding the neural underpinnings of decision-making has practical
implications. In medicine, patients with damage to the ventromedial prefrontal
cortex show intact logical reasoning but severely impaired real-world
decision-making, suggesting that emotional signals are essential inputs to good
judgment rather than obstacles to it — a finding that overturns long-standing
cultural assumptions about the primacy of reason. In economics and public
policy, "nudge theory" — derived from behavioural insights — exploits
predictable decision-making biases to steer behaviour in beneficial directions,
for instance by making healthy food options more visually prominent or enrolment
in pension plans the default choice. The study of how we decide has, in short,
become indispensable to understanding how we live.
"""


class Command(BaseCommand):
    help = 'Seed Cambridge IELTS 9 Test 4 — Reading and Listening (original IELTS-style content)'

    def handle(self, *args, **options):
        self.seed_reading()
        self.seed_listening()
        self.stdout.write(self.style.SUCCESS(
            '✓ Cambridge 9 Test 4 (Reading + Listening) seeded successfully.'
        ))

    # ─────────────────────────────────────────────────────────────────────────
    # READING
    # ─────────────────────────────────────────────────────────────────────────

    def seed_reading(self):
        from apps.reading.models import ReadingTest, ReadingPassage, QuestionGroup, Question

        title = 'Cambridge IELTS 9 — Academic Reading Test 4'
        if ReadingTest.objects.filter(title=title).exists():
            self.stdout.write(f'  skip (exists): {title}')
            return

        test = ReadingTest.objects.create(
            title=title,
            test_type='academic',
            duration_minutes=60,
            is_published=True,
        )

        # ── Passage 1 ────────────────────────────────────────────────────────
        p1 = ReadingPassage.objects.create(
            test=test, order=1,
            title='The Remarkable Abilities of Savants',
            content=READING_PASSAGE_1,
            source='Adapted from academic sources',
        )

        # Group 1: TFNG (Q1-6)
        g1 = QuestionGroup.objects.create(
            passage=p1, order=1, question_type='tfng',
            instructions='Do the following statements agree with the information in the passage? '
                         'In boxes 1–6 on your answer sheet, write TRUE if the statement agrees with '
                         'the information, FALSE if the statement contradicts the information, or '
                         'NOT GIVEN if there is no information on this.',
        )
        for num, text, ans in [
            (1,  'J. Langdon Down first used the term "savant syndrome" in 1887.', 'False'),
            (2,  'Derek Paravicini received formal piano training before his abilities were discovered.', 'False'),
            (3,  'Kim Peek could simultaneously read two pages, one with each eye.', 'True'),
            (4,  'Bruce Miller studied patients whose artistic skills improved as their left hemisphere deteriorated.', 'True'),
            (5,  'Allan Snyder\'s TMS experiments have been widely replicated by other researchers.', 'False'),
            (6,  'Savants tend to perform better than neurotypical people in all areas of memory.', 'Not Given'),
        ]:
            Question.objects.create(group=g1, number=num, text=text, correct_answer=ans)

        # Group 2: Fill (Q7-10) — note completion
        g2 = QuestionGroup.objects.create(
            passage=p1, order=2, question_type='note',
            instructions='Complete the notes below. Choose NO MORE THAN TWO WORDS from the passage '
                         'for each answer. Write your answers in boxes 7–10 on your answer sheet.',
        )
        for num, text, ans in [
            (7,  'Savant syndrome is estimated to occur in roughly one in a ___ people.', 'million'),
            (8,  'Cortical release theory holds that savant skills emerge when certain regions of the ___ hemisphere are damaged.', 'left'),
            (9,  'Brain imaging shows savants have weaker connections between frontal ___ regions.', 'control'),
            (10, 'Standard memory models emphasise the ___ nature of recall.', 'reconstructive'),
        ]:
            Question.objects.create(group=g2, number=num, text=text, correct_answer=ans)

        # Group 3: MCQ (Q11-13)
        g3 = QuestionGroup.objects.create(
            passage=p1, order=3, question_type='mcq',
            instructions='Choose the correct letter, A, B, C or D. '
                         'Write the correct letter in boxes 11–13 on your answer sheet.',
        )
        for num, text, oa, ob, oc, od, ans in [
            (11, 'The cortical release theory suggests that savant abilities appear when',
             'the right hemisphere is directly stimulated',
             'left-hemisphere damage disinhibits right-hemisphere functions',
             'neural connections between hemispheres are strengthened',
             'the prefrontal cortex becomes overactive',
             'B'),
            (12, 'What does Snyder\'s research primarily aim to demonstrate?',
             'That savant abilities exist only in people with disabilities',
             'That TMS can permanently enhance human memory',
             'That latent savant-like abilities may exist in all humans',
             'That calendar calculation is the most common savant skill',
             'C'),
            (13, 'The author\'s main point in the final paragraph is that savant syndrome',
             'proves intelligence is a single unified capacity',
             'shows that human cognitive limits are broader than commonly assumed',
             'demonstrates that disability always accompanies extraordinary ability',
             'supports the idea that memory is purely reconstructive',
             'B'),
        ]:
            Question.objects.create(
                group=g3, number=num, text=text,
                option_a=oa, option_b=ob, option_c=oc, option_d=od,
                correct_answer=ans,
            )

        # ── Passage 2 ────────────────────────────────────────────────────────
        p2 = ReadingPassage.objects.create(
            test=test, order=2,
            title='The Urban Farming Revolution',
            content=READING_PASSAGE_2,
            source='Adapted from academic sources',
        )

        # Group 4: Matching headings (Q14-19)
        g4 = QuestionGroup.objects.create(
            passage=p2, order=1, question_type='match',
            instructions='The passage has seven paragraphs, A–G. '
                         'Choose the correct heading for paragraphs B–G from the list of headings below. '
                         'Write the correct number, i–viii, in boxes 14–19 on your answer sheet. '
                         'List of Headings: i) The hidden benefits of community growing spaces  '
                         'ii) Why certain crops cannot be grown commercially in cities  '
                         'iii) A technology that eliminates outdoor farming constraints  '
                         'iv) The global growth and commercial value of city-based food production  '
                         'v) The carbon accounting problem with indoor agriculture  '
                         'vi) Efforts to integrate food growing into city planning  '
                         'vii) The multiple advantages claimed for growing food in cities  '
                         'viii) Financial barriers facing the urban farming industry',
        )
        for num, text, ans in [
            (14, 'Paragraph B', 'vii'),
            (15, 'Paragraph C', 'iii'),
            (16, 'Paragraph D', 'v'),
            (17, 'Paragraph E', 'viii'),
            (18, 'Paragraph F', 'i'),
            (19, 'Paragraph G', 'vi'),
        ]:
            Question.objects.create(group=g4, number=num, text=text, correct_answer=ans)

        # Group 5: Summary completion (Q20-26)
        g5 = QuestionGroup.objects.create(
            passage=p2, order=2, question_type='summary',
            instructions='Complete the summary below. Choose NO MORE THAN TWO WORDS AND/OR A NUMBER '
                         'from the passage for each answer. '
                         'Write your answers in boxes 20–26 on your answer sheet.',
        )
        for num, text, ans in [
            (20, 'Vertical farms use up to ___ percent less water than conventional agriculture.', '95'),
            (21, 'Because vertical farms are fully enclosed, they require no ___.', 'pesticides'),
            (22, 'A 2019 study found that lettuce from a vertical farm could produce up to ___ times more carbon per kilogram than field-grown lettuce.', '50'),
            (23, 'Most vertical farms focus on high-value, short-___ crops such as salad leaves.', 'cycle'),
            (24, 'Staple crops such as wheat and rice are generally considered ___ to grow vertically.', 'impractical'),
            (25, 'Research from the Netherlands found that people near urban green spaces reported higher levels of ___.', 'wellbeing'),
            (26, 'Amsterdam, Singapore and Melbourne have begun incorporating urban food production into building ___ and planning frameworks.', 'codes'),
        ]:
            Question.objects.create(group=g5, number=num, text=text, correct_answer=ans)

        # ── Passage 3 ────────────────────────────────────────────────────────
        p3 = ReadingPassage.objects.create(
            test=test, order=3,
            title='How We Decide: The Neuroscience of Choice',
            content=READING_PASSAGE_3,
            source='Adapted from academic sources',
        )

        # Group 6: MCQ (Q27-31)
        g6 = QuestionGroup.objects.create(
            passage=p3, order=1, question_type='mcq',
            instructions='Choose the correct letter, A, B, C or D. '
                         'Write the correct letter in boxes 27–31 on your answer sheet.',
        )
        for num, text, oa, ob, oc, od, ans in [
            (27, 'Kahneman and Tversky\'s research primarily showed that',
             'humans are rational agents who maximise expected utility',
             'human decision-making deviates from rational-agent models in predictable ways',
             'emotions play no significant role in human choices',
             'loss aversion is a culturally specific bias',
             'B'),
            (28, 'The ventromedial prefrontal cortex is described in the passage as',
             'a region associated with threat detection',
             'a source of dopamine signals in the midbrain',
             'a hub that integrates information to produce value signals',
             'a structure responsible for unconscious automatic decisions',
             'C'),
            (29, 'Dopamine is described more accurately as a signal of',
             'pleasure and reward',
             'emotional regulation',
             'prediction error',
             'threat avoidance',
             'C'),
            (30, 'According to dual-process theory, System 2 is engaged when',
             'a decision involves familiar situations',
             'cognitive resources are depleted',
             'System 1 signals uncertainty or a problem requires deliberate analysis',
             'emotional responses are strong',
             'C'),
            (31, 'Results from the Ultimatum Game suggest that people',
             'always maximise their financial gains',
             'use only their prefrontal cortex during economic decisions',
             'will sacrifice money to penalise partners they consider unfair',
             'show no emotional response to financial transactions',
             'C'),
        ]:
            Question.objects.create(
                group=g6, number=num, text=text,
                option_a=oa, option_b=ob, option_c=oc, option_d=od,
                correct_answer=ans,
            )

        # Group 7: TFNG (Q32-36)
        g7 = QuestionGroup.objects.create(
            passage=p3, order=2, question_type='tfng',
            instructions='Do the following statements agree with the claims of the writer in the passage? '
                         'In boxes 32–36 on your answer sheet, write YES if the statement agrees with '
                         'the claims of the writer, NO if the statement contradicts the claims of the '
                         'writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.',
        )
        for num, text, ans in [
            (32, 'Classical economics initially assumed that humans always make irrational decisions.', 'False'),
            (33, 'Loss aversion means people feel gains and losses of equal size equally strongly.', 'False'),
            (34, 'Dopamine neurons fire when outcomes exceed expectations.', 'True'),
            (35, 'Cognitive load causes people to use more System 2 reasoning.', 'False'),
            (36, 'Patients with ventromedial prefrontal cortex damage retain intact logical reasoning.', 'True'),
        ]:
            Question.objects.create(group=g7, number=num, text=text, correct_answer=ans)

        # Group 8: Short Answer (Q37-40)
        g8 = QuestionGroup.objects.create(
            passage=p3, order=3, question_type='short',
            instructions='Answer the questions below. Choose NO MORE THAN THREE WORDS from the passage '
                         'for each answer. Write your answers in boxes 37–40 on your answer sheet.',
        )
        for num, text, ans in [
            (37, 'What term did Kahneman and Tversky use to describe people\'s disproportionate reaction to losing compared to gaining?', 'loss aversion'),
            (38, 'Which brain structure is associated with disgust and moral emotion in economic game studies?', 'anterior insula'),
            (39, 'What name is given to the policy approach that exploits decision-making biases to improve behaviour?', 'nudge theory'),
            (40, 'What does the passage say making healthy food options more visually prominent is an example of?', 'nudge theory'),
        ]:
            Question.objects.create(group=g8, number=num, text=text, correct_answer=ans)

        self.stdout.write(f'  ✓ Reading test created: {title} (40 questions)')

    # ─────────────────────────────────────────────────────────────────────────
    # LISTENING
    # ─────────────────────────────────────────────────────────────────────────

    def seed_listening(self):
        from apps.listening.models import ListeningTest, ListeningSection, ListeningQuestion

        title = 'Cambridge IELTS 9 — Listening Test 4'
        if ListeningTest.objects.filter(title=title).exists():
            self.stdout.write(f'  skip (exists): {title}')
            return

        test = ListeningTest.objects.create(
            title=title,
            duration_minutes=40,
            is_published=True,
        )

        # ── Section 1: Conversation — booking a language course ───────────────
        s1 = ListeningSection.objects.create(
            test=test, order=1,
            title='Section 1 — Enquiry about a language course',
            description='A woman phones to enquire about an English language course at a college.',
        )
        for num, text, qtype, ans, oa, ob, oc, od in [
            (1,  'Name of caller: ___ Harrison',              'fill',  'Sarah',      '', '', '', ''),
            (2,  'Course level interested in: Upper ___',     'fill',  'Intermediate','', '', '', ''),
            (3,  'Number of hours per week: ___',             'fill',  '15',         '', '', '', ''),
            (4,  'Start date of next available course: ___',  'fill',  '14 March',   '', '', '', ''),
            (5,  'Course fee per month: £___',                'fill',  '320',        '', '', '', ''),
            (6,  'The caller\'s main reason for studying English is for ___ purposes.', 'fill', 'professional', '', '', '', ''),
            (7,  'The college is located near ___',           'fill',  'the park',   '', '', '', ''),
            (8,  'Which additional service does the college offer?',
                 'mcq', 'C',
                 'Free accommodation',
                 'Job placement support',
                 'Conversation exchange programme',
                 'Library membership'),
            (9,  'What documentation must the caller bring on the first day?',
                 'mcq', 'A',
                 'Passport and previous qualification certificates',
                 'Bank statement and employer reference',
                 'National ID and a recent photograph',
                 'Utility bill and passport'),
            (10, 'The caller will receive a confirmation by ___',
                 'fill', 'email', '', '', '', ''),
        ]:
            ListeningQuestion.objects.create(
                section=s1, number=num, text=text, question_type=qtype,
                correct_answer=ans, option_a=oa, option_b=ob, option_c=oc, option_d=od,
            )

        # ── Section 2: Monologue — tour of a science museum ──────────────────
        s2 = ListeningSection.objects.create(
            test=test, order=2,
            title='Section 2 — Welcome to the Discovery Science Museum',
            description='A museum guide gives a recorded introduction for visitors.',
        )
        # Table completion Q11-16, MCQ Q17-20
        table_qs = [
            (11, 'Ground floor: Interactive ___ Zone',         'table', 'Physics'),
            (12, 'First floor: ___ through the Ages exhibit',  'table', 'Medicine'),
            (13, 'Second floor: Space ___ Gallery',            'table', 'Exploration'),
            (14, 'Café closes at ___ on weekdays',             'table', '17:30'),
            (15, 'Gift shop discount for students: ___ %',     'table', '10'),
            (16, 'Maximum group size for guided tour: ___',    'table', '25'),
        ]
        for num, text, qtype, ans in table_qs:
            ListeningQuestion.objects.create(
                section=s2, number=num, text=text,
                question_type=qtype, correct_answer=ans,
            )
        for num, text, qtype, ans, oa, ob, oc, od in [
            (17, 'The museum is closed on',
                 'mcq', 'C',
                 'Saturdays',
                 'Sundays',
                 'Mondays',
                 'Fridays'),
            (18, 'Which facility has recently been refurbished?',
                 'mcq', 'B',
                 'The main entrance hall',
                 'The planetarium',
                 'The children\'s activity room',
                 'The outdoor garden'),
            (19, 'Photography is',
                 'mcq', 'A',
                 'permitted in all areas except the temporary exhibition',
                 'prohibited throughout the building',
                 'permitted only on the ground floor',
                 'permitted with a special pass'),
            (20, 'The museum recommends visitors allow at least ___ to see all the main exhibits.',
                 'mcq', 'B',
                 'one hour',
                 'three hours',
                 'five hours',
                 'half a day'),
        ]:
            ListeningQuestion.objects.create(
                section=s2, number=num, text=text, question_type=qtype,
                correct_answer=ans, option_a=oa, option_b=ob, option_c=oc, option_d=od,
            )

        # ── Section 3: Discussion — university research project ───────────────
        s3 = ListeningSection.objects.create(
            test=test, order=3,
            title='Section 3 — Student discussion with tutor',
            description='Two students discuss their research project on urban green spaces with their tutor.',
        )
        for num, text, qtype, ans, oa, ob, oc, od in [
            (21, 'The students chose their topic primarily because',
                 'mcq', 'B',
                 'their tutor suggested it',
                 'both had personal interest in environmental issues',
                 'it was the only topic available',
                 'the research data was easy to access'),
            (22, 'What problem did the students encounter with their survey data?',
                 'mcq', 'A',
                 'The sample size was too small',
                 'Participants did not answer all questions',
                 'The data could not be analysed statistically',
                 'Permission to publish was refused'),
            (23, 'The tutor suggests the students focus their conclusion on',
                 'mcq', 'C',
                 'practical policy recommendations',
                 'comparisons with international studies',
                 'the limitations of the research methodology',
                 'future data collection plans'),
            (24, 'What does the tutor say about the students\' literature review?',
                 'mcq', 'B',
                 'It covers too narrow a range of sources',
                 'It is thorough but needs a clearer structure',
                 'It relies too heavily on secondary sources',
                 'It contains factual errors that need correction'),
            (25, 'The students plan to submit their final report',
                 'mcq', 'A',
                 'one week before the official deadline',
                 'on the deadline date',
                 'two days after agreeing an extension',
                 'after receiving peer feedback'),
        ]:
            ListeningQuestion.objects.create(
                section=s3, number=num, text=text, question_type=qtype,
                correct_answer=ans, option_a=oa, option_b=ob, option_c=oc, option_d=od,
            )
        # Matching Q26-30
        match_g_items = [
            (26, 'Biodiversity survey', 'C'),
            (27, 'Air quality measurements', 'A'),
            (28, 'Resident wellbeing questionnaire', 'B'),
            (29, 'Carbon sequestration estimates', 'C'),
            (30, 'Economic valuation of green space', 'A'),
        ]
        for num, text, ans in match_g_items:
            ListeningQuestion.objects.create(
                section=s3, number=num, question_type='match',
                text=f'Which student was responsible for: {text}? '
                     f'(A = Priya  B = Marcus  C = Both students)',
                correct_answer=ans,
            )

        # ── Section 4: Lecture — history of cartography ───────────────────────
        s4 = ListeningSection.objects.create(
            test=test, order=4,
            title='Section 4 — Lecture: The History of Cartography',
            description='A university lecturer gives a talk on the development of map-making.',
        )
        note_qs = [
            (31, 'The earliest known maps were drawn on ___ tablets in Mesopotamia.', 'clay'),
            (32, 'Greek geographer Ptolemy compiled a ___ and mathematical guide to map-making around 150 CE.', 'geographical'),
            (33, 'Medieval European maps, called Mappa Mundi, were primarily ___ rather than geographical documents.', 'religious'),
            (34, 'The Mercator projection, developed in 1569, was designed specifically to assist ___ navigation.', 'marine'),
            (35, 'A key limitation of the Mercator projection is that it distorts the ___ of landmasses near the poles.', 'size'),
            (36, 'The Peters projection was proposed as an ___ alternative because it preserves relative area.', 'equal-area'),
            (37, 'Satellite remote sensing became commercially available in the ___ .', '1970s'),
            (38, 'GIS stands for Geographic ___ Systems.', 'Information'),
            (39, 'OpenStreetMap is described by the lecturer as a ___ mapping project.', 'crowdsourced'),
            (40, 'The lecturer argues that all maps reflect the ___ priorities of their makers.', 'cultural'),
        ]
        for num, text, ans in note_qs:
            ListeningQuestion.objects.create(
                section=s4, number=num, question_type='note',
                text=text, correct_answer=ans,
            )

        self.stdout.write(f'  ✓ Listening test created: {title} (40 questions)')
