"""
Usage: python manage.py seed_data

Creates sample IELTS test data for all four skills plus community rooms.
Safe to run multiple times — skips existing records.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Seed sample IELTS test data'

    def handle(self, *args, **options):
        self.seed_community()
        self.seed_reading()
        self.seed_listening()
        self.seed_writing()
        self.seed_speaking()
        self.stdout.write(self.style.SUCCESS('✓ Sample data seeded successfully.'))

    # ─── Community rooms ────────────────────────────────────────────────────
    def seed_community(self):
        from apps.community.models import Room
        rooms = [
            {'name': 'General Discussion', 'slug': 'general', 'description': 'Talk about anything IELTS related.', 'icon': 'chat'},
            {'name': 'IELTS Tips & Tricks', 'slug': 'tips', 'description': 'Share strategies that worked for you.', 'icon': 'bulb'},
            {'name': 'Band 7+ Lounge', 'slug': 'band7', 'description': 'For high achievers and those aiming for band 7+.', 'icon': 'star'},
            {'name': 'Writing Feedback', 'slug': 'writing-feedback', 'description': 'Post your writing and get peer feedback.', 'icon': 'pen'},
            {'name': 'Speaking Practice', 'slug': 'speaking-practice', 'description': 'Find speaking partners and share recordings.', 'icon': 'mic'},
            {'name': 'Study Groups', 'slug': 'study-groups', 'description': 'Organise study sessions with other learners.', 'icon': 'users'},
        ]
        created = 0
        for r in rooms:
            _, c = Room.objects.get_or_create(slug=r['slug'], defaults=r)
            if c:
                created += 1
        self.stdout.write(f'  Community rooms: {created} created')

    # ─── Reading ────────────────────────────────────────────────────────────
    def seed_reading(self):
        from apps.reading.models import ReadingTest, ReadingPassage, QuestionGroup, Question

        if ReadingTest.objects.filter(title='Academic Reading Test 1').exists():
            self.stdout.write('  Reading: already seeded, skipping')
            return

        test = ReadingTest.objects.create(
            title='Academic Reading Test 1',
            test_type='academic',
            duration_minutes=60,
            is_published=True,
        )

        # Passage 1
        p1 = ReadingPassage.objects.create(
            test=test, order=1, title='The Coral Triangle',
            content="""The Coral Triangle, a vast maritime region in the western Pacific Ocean, encompasses the waters of Indonesia, Malaysia, the Philippines, Papua New Guinea, the Solomon Islands and Timor-Leste. Spanning an area of 5.7 million square kilometres — roughly the size of the continental United States — it is the global epicentre of marine biodiversity, home to 76% of all known coral species, more than 3,000 species of fish, and six of the world's seven marine turtle species.

Scientists often refer to it as the "Amazon of the Seas" because, just as the Amazon rainforest sustains enormous terrestrial biodiversity, the Coral Triangle sustains an extraordinary variety of ocean life. The region supports the food security of 120 million people who rely directly on the sea for their livelihoods and daily sustenance.

Despite its ecological importance, the Coral Triangle faces relentless threats. Coral bleaching — triggered by rising sea temperatures associated with climate change — has damaged vast swathes of reef. Destructive fishing practices, including blast fishing and cyanide fishing, destroy reef structure, while overfishing depletes fish populations faster than they can recover. Coastal development has led to sedimentation that smothers coral, and plastic pollution has become ubiquitous throughout the region.

Governments of the six member countries established the Coral Triangle Initiative on Coral Reefs, Fisheries and Food Security (CTI-CFF) in 2009. The initiative aims to address these threats through coordinated marine resource management, the expansion of marine protected areas, and adaptation strategies for climate change. Progress has been mixed: marine protected areas have grown substantially, but enforcement remains inadequate in many zones, and illegal fishing continues largely unabated.

Conservation organisations argue that the long-term survival of the Coral Triangle depends not only on governmental action but on engaging local fishing communities as stewards of their own marine resources. Community-based marine management programmes — in which villages take direct responsibility for reef areas and fishery rules — have shown promising results in several locations, suggesting that locally driven solutions may prove more sustainable than top-down regulatory approaches.""",
        )
        g1 = QuestionGroup.objects.create(
            passage=p1, order=1, question_type='tfng',
            instructions='Do the following statements agree with the information in the passage? Write TRUE, FALSE or NOT GIVEN.',
        )
        tfng_qs = [
            (1, 'The Coral Triangle covers a larger area than the continental United States.', 'FALSE'),
            (2, 'More than three-quarters of all known coral species are found in the Coral Triangle.', 'TRUE'),
            (3, 'The number of fish species in the Coral Triangle exceeds 3,000.', 'TRUE'),
            (4, 'The CTI-CFF was established with financial support from the United Nations.', 'NOT GIVEN'),
            (5, 'Marine protected areas in the Coral Triangle have grown in number since 2009.', 'TRUE'),
        ]
        for num, text, ans in tfng_qs:
            Question.objects.create(group=g1, number=num, text=text, correct_answer=ans)

        g2 = QuestionGroup.objects.create(
            passage=p1, order=2, question_type='fill',
            instructions='Complete the sentences below. Choose NO MORE THAN TWO WORDS from the passage.',
        )
        fill_qs = [
            (6, 'The Coral Triangle supports the ________ of 120 million people who depend on the sea.', 'food security'),
            (7, 'Coral bleaching is mainly caused by rising ________ linked to climate change.', 'sea temperatures'),
            (8, 'The use of explosives in fishing is known as ________ fishing.', 'blast'),
        ]
        for num, text, ans in fill_qs:
            Question.objects.create(group=g2, number=num, text=text, correct_answer=ans)

        g3 = QuestionGroup.objects.create(
            passage=p1, order=3, question_type='mcq',
            instructions='Choose the correct letter, A, B, C or D.',
        )
        Question.objects.create(
            group=g3, number=9,
            text='According to the passage, what does the author suggest is a more sustainable approach to conservation?',
            option_a='Stronger international regulations imposed by the United Nations',
            option_b='Expanding the number of government-controlled marine reserves',
            option_c='Involving local fishing communities in managing their own reefs',
            option_d='Banning all commercial fishing in the Coral Triangle permanently',
            correct_answer='C',
        )
        Question.objects.create(
            group=g3, number=10,
            text='The phrase "largely unabated" (paragraph 4) most nearly means:',
            option_a='significantly reduced',
            option_b='continuing without much reduction',
            option_c='completely stopped by authorities',
            option_d='gradually increasing in frequency',
            correct_answer='B',
        )

        # Passage 2
        p2 = ReadingPassage.objects.create(
            test=test, order=2, title='The Science of Sleep',
            content="""Sleep is far from the passive, idle state it was once assumed to be. Research over the past four decades has revealed that sleep is an active biological process essential for physical health, cognitive function, emotional regulation and immune defence. Yet despite its importance, sleep deprivation has become epidemic in the modern world, with profound consequences for public health.

During a typical night, humans cycle through several distinct stages of sleep. Non-rapid eye movement (NREM) sleep comprises three stages: light sleep (N1), deeper sleep (N2) and slow-wave sleep (N3, also called deep sleep). These are followed by rapid eye movement (REM) sleep, during which most vivid dreaming occurs. A complete cycle takes approximately 90 minutes, and adults typically experience four to six cycles per night.

The function of sleep has been the subject of intense scientific debate. The synaptic homeostasis hypothesis, proposed by Giulio Tononi and Chiara Cirelli, suggests that the brain strengthens synaptic connections throughout waking hours, and sleep serves to downscale these connections to a sustainable baseline — a process of neural pruning that preserves the most important memories while discarding trivial ones. Other researchers emphasise sleep's role in waste clearance: during sleep, the glymphatic system — a network of channels surrounding brain blood vessels — flushes toxic proteins, including amyloid-beta, which accumulates in Alzheimer's disease.

Adults generally require seven to nine hours of sleep per night for optimal functioning, though individual variation is genuine and partly genetic. The idea that one can "train" oneself to need less sleep is largely a myth; studies consistently show that individuals who sleep fewer than six hours per night suffer measurable cognitive deficits, impaired reaction times and heightened emotional reactivity, even when they report feeling adequately rested.

Chronic sleep deprivation is associated with increased risk of obesity, type 2 diabetes, cardiovascular disease, depression and reduced life expectancy. Shift workers and those with irregular schedules face particular challenges, as disruption to the circadian rhythm — the internal 24-hour biological clock — compounds the effects of reduced sleep duration.""",
        )
        g4 = QuestionGroup.objects.create(
            passage=p2, order=1, question_type='mcq',
            instructions='Choose the correct letter, A, B, C or D.',
        )
        mcq_qs = [
            (11, 'According to the passage, what does the synaptic homeostasis hypothesis propose?', 'Sleep eliminates weak synaptic connections to optimise brain efficiency', 'Sleep creates entirely new neural pathways during dreaming', 'The brain ceases all electrical activity during NREM sleep', 'REM sleep is responsible for most memory formation', 'A'),
            (12, 'The glymphatic system is described as performing which function during sleep?', 'Regulating body temperature to support deep sleep', 'Removing harmful proteins that build up in the brain', 'Coordinating hormonal secretion across organs', 'Strengthening synaptic connections established during the day', 'B'),
        ]
        for num, text, oa, ob, oc, od, ans in mcq_qs:
            Question.objects.create(group=g4, number=num, text=text, option_a=oa, option_b=ob, option_c=oc, option_d=od, correct_answer=ans)

        g5 = QuestionGroup.objects.create(
            passage=p2, order=2, question_type='fill',
            instructions='Complete the summary using words from the box.',
        )
        fill2 = [
            (13, 'A full sleep cycle lasts approximately ________ minutes.', '90'),
            (14, 'Adults are generally advised to sleep ________ to nine hours per night.', 'seven'),
            (15, 'Disruption to the ________ rhythm can worsen the effects of sleep deprivation.', 'circadian'),
        ]
        for num, text, ans in fill2:
            Question.objects.create(group=g5, number=num, text=text, correct_answer=ans)

        self.stdout.write('  Reading: 1 test created (2 passages, 15 questions)')

    # ─── Listening ──────────────────────────────────────────────────────────
    def seed_listening(self):
        from apps.listening.models import ListeningTest, ListeningSection, ListeningQuestion

        if ListeningTest.objects.filter(title='IELTS Listening Practice Test 1').exists():
            self.stdout.write('  Listening: already seeded, skipping')
            return

        test = ListeningTest.objects.create(
            title='IELTS Listening Practice Test 1',
            duration_minutes=40,
            is_published=True,
        )

        # Section 1 — Social context conversation
        s1 = ListeningSection.objects.create(
            test=test, order=1,
            title='Section 1: Booking a Sports Facility',
            description='A conversation between a customer and a receptionist at a sports centre.',
        )
        s1_questions = [
            (1, 'fill', 'The customer wants to book a ________ court.', '', '', '', '', 'tennis'),
            (2, 'fill', 'The session will last ________ minutes.', '', '', '', '', '90'),
            (3, 'fill', 'The customer\'s surname is ________.', '', '', '', '', 'Henderson'),
            (4, 'mcq', 'What time does the customer prefer?', 'Morning', 'Afternoon', 'Evening', 'Lunchtime', 'C'),
            (5, 'fill', 'The total cost of the booking is £________.', '', '', '', '', '24'),
            (6, 'fill', 'The booking reference number is ________.', '', '', '', '', 'SC4471'),
            (7, 'mcq', 'What additional service does the customer request?', 'A locker', 'A racket hire', 'Coaching', 'Refreshments', 'B'),
            (8, 'fill', 'The sports centre closes at ________ on Sundays.', '', '', '', '', '6pm'),
            (9, 'fill', 'The customer is asked to arrive ________ minutes early.', '', '', '', '', '10'),
            (10, 'mcq', 'How will the customer pay?', 'Cash', 'Credit card', 'Online banking', 'Cheque', 'B'),
        ]
        for num, qtype, text, oa, ob, oc, od, ans in s1_questions:
            ListeningQuestion.objects.create(section=s1, number=num, text=text, question_type=qtype, option_a=oa, option_b=ob, option_c=oc, option_d=od, correct_answer=ans)

        # Section 2 — Monologue (public information)
        s2 = ListeningSection.objects.create(
            test=test, order=2,
            title='Section 2: City Museum Audio Guide',
            description='A guided audio tour of a city museum.',
        )
        s2_questions = [
            (11, 'fill', 'The museum was founded in ________.', '', '', '', '', '1887'),
            (12, 'fill', 'The permanent collection contains over ________ artefacts.', '', '', '', '', '40,000'),
            (13, 'mcq', 'The Egyptian gallery is located on which floor?', 'Ground floor', 'First floor', 'Second floor', 'Basement', 'B'),
            (14, 'fill', 'The museum café is open from 10am until ________.', '', '', '', '', '4:30pm'),
            (15, 'fill', 'Guided tours depart every ________ minutes.', '', '', '', '', '45'),
            (16, 'mcq', 'Children under what age are admitted free?', 'Under 5', 'Under 12', 'Under 16', 'Under 18', 'B'),
            (17, 'fill', 'The gift shop is located near the ________ entrance.', '', '', '', '', 'main'),
            (18, 'mcq', 'On which day is the museum closed?', 'Monday', 'Tuesday', 'Wednesday', 'Sunday', 'A'),
            (19, 'fill', 'Photography is not permitted in the ________ gallery.', '', '', '', '', 'contemporary art'),
            (20, 'fill', 'The museum\'s website address is www.________.org.', '', '', '', '', 'citymuseum'),
        ]
        for num, qtype, text, oa, ob, oc, od, ans in s2_questions:
            ListeningQuestion.objects.create(section=s2, number=num, text=text, question_type=qtype, option_a=oa, option_b=ob, option_c=oc, option_d=od, correct_answer=ans)

        # Section 3 — Academic discussion
        s3 = ListeningSection.objects.create(
            test=test, order=3,
            title='Section 3: University Tutorial — Research Methods',
            description='A discussion between two students and their tutor about research methodology.',
        )
        s3_questions = [
            (21, 'mcq', 'What is the main topic of the students\' research project?', 'Urban migration patterns', 'Online learning effectiveness', 'Consumer behaviour in retail', 'Climate change attitudes', 'B'),
            (22, 'fill', 'The tutor recommends a minimum sample size of ________ participants.', '', '', '', '', '50'),
            (23, 'mcq', 'Which data collection method does the tutor criticise?', 'Interviews', 'Surveys', 'Observation', 'Focus groups', 'B'),
            (24, 'fill', 'The students must submit their literature review by ________.', '', '', '', '', 'Friday'),
            (25, 'mcq', 'What does the tutor say about qualitative data?', 'It is more reliable than quantitative data', 'It should not be used for this topic', 'It can complement quantitative findings', 'It requires a larger sample', 'C'),
            (26, 'fill', 'The tutor suggests reading the paper by ________ on mixed methods.', '', '', '', '', 'Creswell'),
            (27, 'mcq', 'What problem do the students identify with their current design?', 'The questions are too difficult', 'The sample is too small', 'There is no control group', 'The timeline is too short', 'C'),
            (28, 'fill', 'The next tutorial meeting is scheduled for ________.', '', '', '', '', 'Thursday'),
            (29, 'mcq', 'The tutor recommends which type of sampling?', 'Random sampling', 'Purposive sampling', 'Convenience sampling', 'Stratified sampling', 'D'),
            (30, 'fill', 'The students need to include a ________ statement in their methodology section.', '', '', '', '', 'limitations'),
        ]
        for num, qtype, text, oa, ob, oc, od, ans in s3_questions:
            ListeningQuestion.objects.create(section=s3, number=num, text=text, question_type=qtype, option_a=oa, option_b=ob, option_c=oc, option_d=od, correct_answer=ans)

        # Section 4 — Academic monologue
        s4 = ListeningSection.objects.create(
            test=test, order=4,
            title='Section 4: Lecture — The History of Urban Planning',
            description='A university lecture on the development of modern urban planning.',
        )
        s4_questions = [
            (31, 'fill', 'The lecturer says modern urban planning began in the ________ century.', '', '', '', '', '19th'),
            (32, 'fill', 'The first public parks were created to address problems of ________.', '', '', '', '', 'overcrowding'),
            (33, 'mcq', 'What was the main principle of the Garden City movement?', 'Building upwards to save land', 'Combining urban and rural features', 'Restricting access to private vehicles', 'Separating residential and industrial zones', 'B'),
            (34, 'fill', 'Ebenezer Howard\'s book was published in ________.', '', '', '', '', '1898'),
            (35, 'mcq', 'Which city does the lecturer give as an example of a planned capital?', 'New York', 'Paris', 'Canberra', 'London', 'C'),
            (36, 'fill', 'The concept of ________ cities emerged in response to car-dependent suburbs.', '', '', '', '', 'walkable'),
            (37, 'mcq', 'What does the lecturer say is the biggest challenge facing cities today?', 'Air pollution', 'Housing affordability', 'Traffic congestion', 'Aging infrastructure', 'B'),
            (38, 'fill', 'Smart city technologies rely heavily on ________ and data analytics.', '', '', '', '', 'sensors'),
            (39, 'mcq', 'The lecturer\'s view on green roofs is that they:', 'are too expensive to be practical', 'reduce urban heat and manage rainwater', 'are mainly decorative features', 'require too much maintenance', 'B'),
            (40, 'fill', 'The lecturer recommends students read the report published by the ________ .', '', '', '', '', 'UN Habitat'),
        ]
        for num, qtype, text, oa, ob, oc, od, ans in s4_questions:
            ListeningQuestion.objects.create(section=s4, number=num, text=text, question_type=qtype, option_a=oa, option_b=ob, option_c=oc, option_d=od, correct_answer=ans)

        self.stdout.write('  Listening: 1 test created (4 sections, 40 questions)')

    # ─── Writing ────────────────────────────────────────────────────────────
    def seed_writing(self):
        from apps.writing.models import WritingTest, WritingTask

        if WritingTest.objects.filter(title='Academic Writing Test 1').exists():
            self.stdout.write('  Writing: already seeded, skipping')
            return

        test = WritingTest.objects.create(title='Academic Writing Test 1', is_published=True)

        WritingTask.objects.create(
            test=test,
            task_type='task1',
            order=1,
            prompt=(
                'The graph below shows the percentage of households in the United Kingdom '
                'that owned at least one car between 1970 and 2010.\n\n'
                'Summarise the information by selecting and reporting the main features, '
                'and make comparisons where relevant.'
            ),
            min_words=150,
            time_minutes=20,
        )

        WritingTask.objects.create(
            test=test,
            task_type='task2',
            order=2,
            prompt=(
                'In many countries, people are now living longer than ever before. Some people say '
                'an ageing population creates problems for governments. Others believe that older '
                'people make a valuable contribution to society.\n\n'
                'Discuss both views and give your own opinion.'
            ),
            min_words=250,
            time_minutes=40,
        )

        # Second writing test
        test2 = WritingTest.objects.create(title='Academic Writing Test 2', is_published=True)

        WritingTask.objects.create(
            test=test2,
            task_type='task1',
            order=1,
            prompt=(
                'The diagram below shows the process of recycling glass bottles.\n\n'
                'Summarise the information by selecting and reporting the main features.'
            ),
            min_words=150,
            time_minutes=20,
        )

        WritingTask.objects.create(
            test=test2,
            task_type='task2',
            order=2,
            prompt=(
                'Some people believe that the best way to improve public health is to increase '
                'the number of sports facilities. Others, however, believe that this would have '
                'little effect on public health and that other measures are required.\n\n'
                'Discuss both views and give your own opinion.'
            ),
            min_words=250,
            time_minutes=40,
        )

        self.stdout.write('  Writing: 2 tests created (4 tasks total)')

    # ─── Speaking ───────────────────────────────────────────────────────────
    def seed_speaking(self):
        from apps.speaking.models import SpeakingTest, SpeakingPart

        if SpeakingTest.objects.filter(title='IELTS Speaking Practice Test 1').exists():
            self.stdout.write('  Speaking: already seeded, skipping')
            return

        test = SpeakingTest.objects.create(title='IELTS Speaking Practice Test 1', is_published=True)

        SpeakingPart.objects.create(
            test=test, part_type='part1', order=1,
            prompt='Tell me about your home town or city. Where is it, and what do you like about it?',
            cue_card_points='',
            prep_time_seconds=0,
            speak_time_seconds=270,
        )

        SpeakingPart.objects.create(
            test=test, part_type='part2', order=2,
            prompt='Describe a book that you enjoyed reading.',
            cue_card_points='What the book was about\nWhen you read it\nWhy you chose to read it\nAnd explain why you enjoyed it',
            prep_time_seconds=60,
            speak_time_seconds=120,
        )

        SpeakingPart.objects.create(
            test=test, part_type='part3', order=3,
            prompt='Let\'s talk about reading habits in your country. Do you think people read less now than in the past? Why?',
            cue_card_points='',
            prep_time_seconds=0,
            speak_time_seconds=300,
        )

        # Second speaking test
        test2 = SpeakingTest.objects.create(title='IELTS Speaking Practice Test 2', is_published=True)

        SpeakingPart.objects.create(
            test=test2, part_type='part1', order=1,
            prompt='Let\'s talk about your daily routine. What time do you usually wake up, and how do you start your day?',
            cue_card_points='',
            prep_time_seconds=0,
            speak_time_seconds=270,
        )

        SpeakingPart.objects.create(
            test=test2, part_type='part2', order=2,
            prompt='Describe a time when you helped someone.',
            cue_card_points='Who you helped\nWhy they needed help\nHow you helped them\nAnd how you felt afterwards',
            prep_time_seconds=60,
            speak_time_seconds=120,
        )

        SpeakingPart.objects.create(
            test=test2, part_type='part3', order=3,
            prompt='Do you think people in modern society are more or less likely to help strangers compared to the past? What has changed?',
            cue_card_points='',
            prep_time_seconds=0,
            speak_time_seconds=300,
        )

        self.stdout.write('  Speaking: 2 tests created (6 parts total)')
