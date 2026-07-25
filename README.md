# InTRACt: Interplay of Text, Reader And Context in children’s digital reading

*Work in progress. This repository contains an ongoing literature review and a preregistration document, both under active development.*

---

## About the project

The project asks how the language in a story shapes how quickly a child reads it, and whether children read faster as reading experience accumulates, story after story.

InTRACt is a preregistered study that analyses large-scale behavioural data from children aged 7 and older who read AI-generated storybooks through *Let's Story*, a feature of the *Applaydu* edutainment app (Gameloft / Ferrero International). By combining computational psycholinguistics with Bayesian statistical modelling, the study investigates how measurable properties of text (word frequency, syntactic complexity, semantic coherence) and children's growing reading experience predict reading behaviour in the wild, across the 19 languages of the corpus.

The project is hosted at the **[Department of Education, University of Oxford](https://www.education.ox.ac.uk/)**, and is embedded within the **[Learning in Families through Technology (LIFT)](https://www.education.ox.ac.uk/project/lift-learning-in-families-through-technology/)** project, which investigates how digital technologies shape learning within families. It is funded by **Kinder** and the **John Fell Fund** (University of Oxford).

---

## Background

Reading comprehension depends on both the reader and the text. Laboratory research has established that measurable features of written text reliably predict how long readers take and how much they understand. At the word level, less frequent and more abstract words slow readers down and are harder to retain. At the sentence level, longer and more structurally complex sentences impose greater demands on working memory. At the level of the whole passage, texts high in discourse coherence, in which sentences connect logically and explicitly, are generally easier to follow than those that leave more to inference.

These effects are well established in adults, but children's reading is distinct. Younger readers have smaller vocabularies, less automatised decoding and more limited working memory, all of which are still developing through the primary-school years, and their fluency grows with every story they read. At the same time, the rise of AI-generated text and edutainment apps has opened new windows onto children's naturalistic reading at a scale that laboratory studies cannot match. InTRACt bridges these two traditions.

---

## Conceptual framework

The diagram below sets out the study's theoretical scope. The top band lists the established findings the theory builds on. The middle band states the constructs and labelled propositions: three families of text difficulty (lexical-distributional, syntactic-structural and discourse-coherence), together with within-child reading experience and the language context, predict reading time per word. The bottom band states the four pre-registered predictions, each pointed at an alternative account that the same pre-registered analyses weigh against.

![Theoretical scope of the InTRACt study: the established findings the theory builds on; the constructs and labelled propositions, in which lexical-distributional, syntactic-structural and discourse-coherence text difficulty, together with within-child reading experience and the language context, predict reading time per word; and the four pre-registered predictions (H1a, H1b, H1c and H2), each weighed against an alternative account.](mindmap/mindmap.png)

---

## Hypotheses

The study tests two pre-registered, directional hypotheses. The first concerns the text: linguistically more demanding stories are expected to take children longer to read per word. It is evaluated as three independent sub-hypotheses, one per text dimension. Stories with more structurally complex sentences (Hypothesis 1a) and more difficult vocabulary (Hypothesis 1b) should be read more slowly, and more coherent stories, which guide the reader from one idea to the next, should be read faster (Hypothesis 1c).

The second hypothesis concerns the reader. Reading practice builds fluency, so children are expected to read progressively faster as they accumulate reading experience across sessions in the app (Hypothesis 2). Because the data are observational, the hypotheses are tested alongside pre-registered checks that put rival explanations, chiefly skimming and selective retention, to the same tests. The app also allows stories to be read aloud, and narration is not logged, so pacing that the child does not set alone is treated as one source of the constant-rate pacing that the text-feature predictions are set against.

---

## Data

Data come from the *Let's Story* feature of *Applaydu*, which enables families to co-create AI-generated storybooks. In the first six months after launch in late 2024, over 2.4 million story sessions were recorded across 19 languages. The study sample includes children aged 7 and older who provided parental consent in-app, completed first-time readings of at least five distinct stories, and produced reading times within plausible bounds. All data are anonymised and collected passively, with no experimental manipulation. The outcome is how long children spend reading each word; because the platform records no cross-linguistically comparable comprehension measure, the study's inferences concern reading behaviour rather than comprehension itself.

For each story, the study computes a broad range of computational text indices covering word frequency, vocabulary diversity, sentence structure, semantic coherence between sentences, connective density, and affective properties such as sentiment and emotional arousal. Before modelling, these indices are reduced to a smaller number of interpretable composite scores, which then serve as predictors.

---

## Analytic approach

All confirmatory analyses use Bayesian hierarchical models, a framework suited to the present data because the scientific questions concern the size and direction of effects rather than their mere existence, and because the very large sample would render conventional significance tests uninformative. The models account for the fact that reading sessions are nested within children, who are in turn nested within languages. For each hypothesis, the study reports the estimated effect, its uncertainty, and whether the effect is large enough to be educationally meaningful, a distinction that matters when sample sizes are in the millions.

---

## Repository contents

The `preregistration/` folder contains the preregistration document in Quarto source format alongside rendered HTML and PDF drafts and the associated reference library. The `mindmap/` folder contains the theory-scope figure, its machine-readable theory specification (theoryforge), and the scripts that generate it. The `systematic_review/` folder contains the verified data table from the ongoing systematic literature review and the script that keeps it consistent with the reference library.

---

## Contact

Questions and comments are welcome via the [issue tracker](../../issues).

