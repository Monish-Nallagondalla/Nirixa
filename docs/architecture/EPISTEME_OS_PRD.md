# Nirixa Episteme OS
## Product Requirements Document
### Version: 1.0
### Status: Build Specification
### Product Type: Cognitive Operating System & Epistemic Research Workbench

---

# 1. Executive Summary

Nirixa is a local-first personal cognitive operating system designed to preserve, organize, interrogate, connect, and evolve a person's intellectual life over decades.

It is not primarily a notes application.

It is not a chatbot wrapper.

It is not a productivity dashboard.

It is not intended to replace human judgment.

Nirixa treats **questions, epistemic objects, beliefs, evidence, intellectual work, provenance, connections, outputs, and outcomes as persistent computational primitives**.

The system exists because conventional AI interfaces have a structural weakness:

> AI answers questions, but the intellectual context that produced those questions is usually temporary.

A conversation ends.

A useful connection disappears.

A belief changes without its history being preserved.

A paper is read but its implications are never connected to previous thinking.

A thought becomes a LinkedIn post but the ancestry of that thought is lost.

Nirixa reverses this model.

Its central proposition is:

> **Questions compound. Answers decay. Context accumulates.**

Nirixa therefore maintains a longitudinal representation of:

1. The external world.
2. The user's evolving intellectual state.
3. The AI system's evolving capabilities and understanding.
4. The interactions between them.

The core research spine is:

```text
Interaction
    ↓
Epistemic Work
    ↓
Change
    ↓
Adaptation
    ↓
Future Interaction
```

The product must therefore function simultaneously as:

- Personal intellectual memory
- Research workbench
- AI research agent
- Thought graph
- Writing/output system
- Self-inquiry system
- Human-AI coevolution laboratory
- Longitudinal research instrument

---

# 2. Product Thesis

Nirixa should be built around the following thesis:

> **Human intellectual development can be represented as a longitudinal system of questions, epistemic objects, evidence, beliefs, work, connections, outputs, and outcomes. Persistent AI interaction can then become observable as a process of human-AI coevolution rather than a sequence of isolated conversations.**

The system must not assume this thesis is correct.

A foundational design principle is:

> **Do not build Nirixa to prove that human-AI coevolution happens. Build Nirixa so that, if it happens, we can observe it, measure it, challenge it, and discover that we were wrong.**

This is a research instrument as much as it is a product.

---

# 3. Product Vision

By 2029, Nirixa should allow the user to look backward across years of intellectual activity and answer questions such as:

- What did I believe in 2026?
- Why did I believe it?
- What changed my mind?
- Which questions survived for years?
- Which questions generated the most valuable work?
- Which ideas did I abandon?
- Which ideas unexpectedly connected?
- Which discoveries were made by me?
- Which were discovered by AI?
- Which were co-created?
- Where did AI genuinely change my thinking?
- Where did I become dependent on AI?
- Where did AI misunderstand me?
- How has my reasoning changed?
- How has my questioning changed?
- How has Nirixa itself changed?
- Which ideas became papers?
- Which became products?
- Which became public writing?
- Which became book chapters?
- Which became real-world outcomes?

The product should preserve the **complete intellectual ancestry** of these changes.

---

# 4. Core Design Principles

## 4.1 Questions are first-class primitives

A question is not merely text inside a note.

A Question is a persistent unresolved inquiry.

It can:

- evolve
- remain unanswered
- generate subquestions
- connect to multiple EOs
- generate evidence
- generate experiments
- generate beliefs
- generate outputs
- survive for years

Example:

```text
Q-001
How does persistent AI interaction change human reasoning?
```

The question may remain active even after several partial answers.

---

# 4.2 Epistemic Objects are enduring subjects of inquiry

An Epistemic Object represents a persistent subject being understood, investigated, explained, challenged, evaluated, or developed.

An EO is not:

- a note
- a question
- a belief
- a topic
- a snapshot
- a document

Example:

```text
EO-004
Contextual Retrieval of Human Intentions
```

An EO may contain:

```text
Questions
Answers
Evidence
Counter-evidence
Beliefs
Work
Connections
Outputs
History
Uncertainty
```

The EO itself should remain relatively stable.

Intellectual evolution occurs around it.

---

# 4.3 No artificial EO versioning

Do not create:

```text
EO-004-v1
EO-004-v2
EO-004-v3
```

simply because understanding changed.

Instead, the intellectual history surrounding EO-004 evolves.

If intellectual work demonstrates that the EO contains two genuinely independent subjects, decomposition may occur:

```text
EO-004
   ↓ DECOMPOSES_INTO
EO-019
EO-020
```

If one EO is merely a more precise formulation of another:

```text
EO-A
   ↓ REFINED_BY
EO-B
```

If one EO is replaced:

```text
EO-A
   ↓ SUPERSEDED_BY
EO-B
```

The system must never split or merge objects merely because the database schema suggests doing so.

> **Work determines intellectual evolution. Ontology does not dictate it.**

---

# 4.4 Beliefs are independently addressable

A belief is a proposition currently held by a human or AI.

Beliefs must have:

- proposition
- holder
- epistemic status
- confidence
- evidence
- origin
- history
- challenges
- changes
- timestamp

Example:

```text
B-017

Proposition:
Persistent contextual interaction may improve human synthesis.

Holder:
Human

Status:
Working belief

Confidence:
0.62
```

Possible statuses:

```text
Hypothesis
Working Belief
Uncertain
Supported
Challenged
Rejected
Superseded
```

Belief history must never be overwritten.

---

# 4.5 Evidence must preserve provenance

Evidence is material that supports, weakens, contradicts, or contextualizes an epistemic claim.

Sources may include:

- academic papers
- books
- podcasts
- videos
- websites
- datasets
- documents
- conversations
- experiments
- personal observations
- workplace observations
- AI-generated arguments
- external events

The original source must remain distinguishable from AI interpretation.

Example:

```text
Source
  ↓
Extracted Claim
  ↓
User Interpretation
  ↓
Evidence
  ↓
EO / Question / Belief
```

Nirixa must never present an AI interpretation as though it were a source fact.

---

# 4.6 Activity is not automatically epistemic work

A user can read a paper without learning anything relevant.

A user can have a two-hour conversation without changing an epistemic state.

Therefore:

```text
Activity
    ↓
Did it materially change epistemic state?
    ├── No → Activity/Event
    └── Yes → Epistemic Work
```

Epistemic Work is:

> **An activity that produces a meaningful change in the state, structure, evidence, relationships, or understanding of an Epistemic Object.**

---

# 4.7 AI proposes, human canonizes

AI can:

- discover
- interpret
- connect
- challenge
- research
- propose
- synthesize
- generate hypotheses

AI cannot independently:

- canonize a human belief
- declare an idea true
- permanently redefine the user's intellectual identity
- publish consequential work
- make major personal/career decisions
- erase intellectual history

Human confirmation is required where the action changes canonical human epistemic state.

---

# 4.8 Reversibility

Every important AI-generated interpretation should be reversible.

The system should retain:

```text
Candidate
    ↓
Investigating
    ↓
Supported
    ↓
Canonized
```

Alternative branches:

```text
Rejected
Challenged
Revised
Superseded
```

Being wrong is valuable data.

Nirixa should remember:

> What was believed, why it was believed, what challenged it, and why it was rejected.

---

# 4.9 Authenticity

Nirixa must never fabricate personal experience.

It must not invent:

- workplace situations
- conversations
- client interactions
- personal anecdotes
- emotional experiences
- achievements
- experiments
- decisions

Personal stories can only originate from:

1. Explicit user input.
2. Verified stored source material.
3. An explicitly identified inference.

Inference must never be presented as fact.

---

# 5. Core Ontology

The foundational objects are:

```text
Question
Epistemic Object
Belief
Evidence
Answer
Source
Event
Activity
Engagement
Epistemic Work
Connection
Goal
Output
Outcome
```

---

# 6. Object Definitions

## 6.1 Question

Persistent unresolved inquiry.

Attributes:

```text
id
text
created_at
updated_at
status
priority
parent_question
related_eos
related_beliefs
related_evidence
origin
provenance
history
```

Statuses:

```text
Open
Investigating
Partially Answered
Answered
Reopened
Dormant
Superseded
```

---

# 6.2 Epistemic Object

Persistent subject of inquiry.

Attributes:

```text
id
title
description
created_at
updated_at
status
topics
questions
answers
evidence
counter_evidence
beliefs
work
connections
outputs
history
uncertainty
provenance
```

Statuses:

```text
Active
Dormant
Decomposed
Superseded
Archived
```

---

# 6.3 Belief

A proposition currently held by a human or AI.

Attributes:

```text
id
proposition
holder
status
confidence
created_at
updated_at
supporting_evidence
contradicting_evidence
origin
history
```

---

# 6.4 Evidence

Provenance-preserving material relevant to an epistemic claim.

Attributes:

```text
id
source_id
content
type
timestamp
provenance
related_claims
related_beliefs
related_eos
strength
interpretation
```

Evidence types:

```text
Observation
Source Claim
Experimental Result
Data
Argument
Counterexample
Personal Experience
AI Argument
Conversation
Literature Finding
```

---

# 6.5 Answer

An Answer is a response to a Question at a specific point in time.

An answer is not necessarily truth.

It represents:

> What appears to be the best answer given the evidence and understanding available at that time.

Attributes:

```text
id
question_id
content
timestamp
author
evidence
confidence
status
supersedes
```

Multiple answers can exist for the same question.

---

# 6.6 Source

A provenance anchor.

Examples:

```text
Paper
Book
Podcast
Video
Website
Conversation
Dataset
Document
Experiment
Personal observation
```

---

# 6.7 Event

Something that happened.

Examples:

```text
User read paper.
User heard podcast.
User had conversation.
User experienced event.
User published post.
AI generated discovery.
```

Events do not automatically become epistemic work.

---

# 6.8 Activity

An action performed by a human, AI, or external system.

Examples:

```text
Read
Listen
Search
Compare
Write
Experiment
Ask
Challenge
Implement
Publish
```

---

# 6.9 Engagement

The bridge between an event/activity and an epistemic object.

Example:

```text
Read paper
      ↓
Engagement with EO-004
      ↓
Identified contradiction
      ↓
Epistemic Work
```

---

# 6.10 Epistemic Work

Types:

```text
Discovery
Inquiry
Synthesis
Validation
Challenge
Reflection
Revision
Experimentation
Externalization
```

Each Work record should capture:

```text
actor
timestamp
activity
target
before_state
action
change
after_state
evidence
confidence
```

---

# 6.11 Connection

Typed relationship between objects.

Supported relationships:

```text
SUPPORTS
CONTRADICTS
EXTENDS
REFINES
DERIVES_FROM
INSPIRED_BY
ANALOGOUS_TO
QUESTIONS
DEPENDS_ON
APPLIES_TO
GENERATES
SUPERSEDES
DECOMPOSES_INTO
RELATED_TO
```

Connections must include:

```text
source
target
relationship_type
reason
created_at
created_by
confidence
evidence
human_verified
```

---

# 6.12 Goal

A desired future state.

Goals form a hierarchy:

```text
Long-term direction
      ↓
2029
      ↓
2027
      ↓
2026
      ↓
Current objectives
```

Goals provide contextual relevance.

They must not dictate what the user thinks.

---

# 6.13 Output

Externalized result.

Examples:

```text
LinkedIn post
Paper
Book chapter
Talk
Product
Experiment
OSS contribution
Decision
Presentation
```

---

# 6.14 Outcome

Real-world consequence of an output.

Examples:

```text
New opportunity
Career progression
Research collaboration
Follower growth
Publication
Product adoption
Learning result
Change in behaviour
```

Outcome can generate future Events.

---

# 7. Epistemic State

Epistemic State is a derived state.

It must not be treated as a manually edited document.

It is reconstructed from:

```text
Questions
Answers
Evidence
Beliefs
Connections
Work
Outputs
History
Uncertainty
```

The UI may present:

> Current understanding

but the underlying system must retain the history that produced it.

---

# 8. Intellectual Change Model

Nirixa must measure intellectual change across multiple dimensions.

Do NOT create a single "intelligence score."

Instead maintain an **Intellectual Change Vector**.

Dimensions:

```text
Question Quality
Synthesis
Connection Quality
Evidence Quality
Epistemic Calibration
Contradiction Handling
Belief Evolution
Falsification Behaviour
Novelty
Exploration Breadth
Depth
Problem Framing
Experimentation
Externalization
Intellectual Independence
```

These are observational metrics.

They are not optimization targets.

The system should avoid statements such as:

> "Your intelligence increased by 12%."

Instead:

> "Your questions have become more specific and falsifiable over the last six months."

---

# 9. Human-AI Contribution Model

Every meaningful intellectual contribution must have attribution.

Actors:

```text
Human
AI
Human + AI
External Source
Unknown
```

Contribution lineage:

```text
Origin
   ↓
Contribution
   ↓
Discovery
   ↓
Interpretation
   ↓
Acceptance
   ↓
Canonization
```

Contribution is not ownership.

Example:

```text
Human:
Original question

AI:
Unexpected connection

Human:
Reframed question

AI:
Research synthesis

Human:
Accepted hypothesis

Human:
Published output
```

Nirixa must preserve this lineage.

---

# 10. AI Autonomy Model

## Level 0 — Observe

AI may:

- ingest
- index
- transcribe
- extract
- classify
- preserve provenance
- detect entities

## Level 1 — Propose

AI may:

- propose questions
- propose EOs
- propose connections
- identify contradictions
- suggest research
- challenge beliefs
- suggest outputs

## Level 2 — Investigate

AI may autonomously:

- search literature
- gather evidence
- find counterarguments
- compare sources
- test candidate explanations
- generate candidate conclusions

Results remain candidate state.

## Level 3 — Canonicalize

Human approval required.

AI cannot independently:

- change canonical human beliefs
- declare an idea established
- canonize important intellectual relationships
- publish consequential work
- redefine the user's identity
- make major decisions

---

# 11. AI Research Agent

Nirixa should behave as an autonomous intellectual research partner.

When new material enters the system, Nirixa should ask internally:

```text
What is this?
Why might it matter?
What existing questions does it relate to?
What EOs does it affect?
What beliefs does it support?
What beliefs does it challenge?
What contradictions does it reveal?
What new questions does it generate?
What unexpected connections exist?
What should the user investigate?
```

The system must not stop at summarization.

---

# 12. Example: Podcast Ingestion

User sends:

```text
Podcast URL
```

Nirixa should:

1. Retrieve/transcribe if possible.
2. Preserve source.
3. Extract meaningful claims.
4. Identify concepts.
5. Identify arguments.
6. Identify evidence.
7. Identify disagreements.
8. Compare with existing EOs.
9. Compare with existing questions.
10. Compare with beliefs.
11. Search for contradictions.
12. Search for unexpected connections.
13. Generate new questions.
14. Generate candidate epistemic work.
15. Present discoveries.
16. Ask for human confirmation where canonicalization is required.

The output should NOT simply be:

> "Here is a summary of the podcast."

Instead:

> "This podcast contains three ideas relevant to EO-004. One appears to contradict a belief you formed in July. I also found an unexpected connection to a paper you read four months ago."

---

# 13. Discovery Engine

Discovery is a core product capability.

Nirixa must proactively identify:

### Unexpected connections

Connections that the user did not explicitly request.

### Contradictions

Where two beliefs, sources, observations, or EOs conflict.

### Forgotten ideas

Important historical questions or ideas that have not been revisited.

### Neglected objects

E.g.:

> "You have accumulated evidence around this question but have not attempted an experiment."

### Research opportunities

Questions with:

- high relevance
- high novelty
- unresolved contradiction
- available evidence
- potential research value

### Intellectual patterns

Examples:

> "You repeatedly connect memory to intelligence."

> "You frequently explore questions about context but rarely test them empirically."

> "Your last 12 research sessions reinforced existing beliefs rather than challenged them."

These should be evidence-backed observations.

---

# 14. Challenge Engine

Nirixa must actively disagree when appropriate.

Challenge UI:

```text
I think one of your current beliefs may be wrong.

BELIEF

Evidence supporting it

Evidence against it

Counter-thesis

Potential falsifier

Related research

Your historical reasoning

Options:
[Defend]
[Investigate]
[Revise]
[Reject]
[Defer]
```

The goal is not argument for its own sake.

The goal is epistemic improvement.

---

# 15. Exploration Engine

Nirixa must avoid overfitting to the user's existing interests.

It should occasionally introduce:

- adjacent disciplines
- unrelated research
- opposing schools
- alternative frameworks
- unexpected analogies
- difficult counterexamples

The system should distinguish:

```text
Personal relevance
vs
Intellectual exploration
```

Exploration is necessary because otherwise the system may become an echo chamber.

---

# 16. Self Model

Nirixa maintains a dynamic model of the user.

Potential dimensions:

```text
Goals
Questions
Beliefs
Interests
Knowledge
Capabilities
Experiences
Preferences
Decision patterns
Behaviour patterns
Career trajectory
Research trajectory
Intellectual trajectory
Writing patterns
```

The model must be evidence-backed.

AI inference should be labelled as inference.

Example:

```text
Observed:
User has created 17 questions around AI memory.

Possible pattern:
Memory appears to be a recurring intellectual interest.

Confidence:
0.84
```

---

# 17. Ask Nirixa

Ask Nirixa is not a generic chatbot.

It is a longitudinal self-inquiry interface.

Examples:

```text
Why am I interested in memory?

What changed my mind recently?

What am I avoiding?

What are my strongest ideas?

Which of my beliefs are weakly supported?

Where am I inconsistent?

What questions have survived the longest?

What ideas have I abandoned?

What should I research next?

How have I changed since I started using Nirixa?

Where is AI influencing my thinking most?

Am I becoming better at thinking or merely better at using AI?
```

Answers must cite underlying evidence and lineage where possible.

---

# 18. Human-AI Coevolution Model

Nirixa tracks:

```text
Human state
AI state
Interaction
Human contribution
AI contribution
Epistemic work
Change
Adaptation
Downstream effect
```

Conceptual structure:

```text
Human v1
     ↕
Nirixa v1
     ↓
Interaction
     ↓
Human v2
     ↕
Nirixa v2
     ↓
Interaction
     ↓
Human v3
```

A Coevolution Event occurs when:

1. Human and/or AI state changes.
2. The change affects subsequent interaction.
3. The interaction produces meaningful downstream consequences.

---

# 19. Research Instrumentation

Every meaningful interaction should be instrumented where privacy allows.

Conceptual record:

```yaml
coevolution_event:
  timestamp:
  human_state_before:
  ai_state_before:
  interaction:
  human_contribution:
  ai_contribution:
  epistemic_work:
  epistemic_change:
  human_state_after:
  ai_state_after:
  downstream_effect:
  evidence:
  confidence:
```

Research instrumentation must be passive wherever possible.

Do not force the user to fill forms after every interaction.

---

# 20. Human-AI Metrics

## Human Evolution

Measure:

- question quality
- synthesis
- connection-making
- evidence usage
- calibration
- falsification
- belief revision
- exploration
- depth
- experimentation
- externalization
- intellectual independence

## AI Evolution

Measure:

- retrieval relevance
- context accuracy
- personalization
- discovery precision
- challenge relevance
- user-model accuracy
- goal understanding
- forgotten-idea retrieval
- research assistance
- false-positive discoveries
- false-negative discoveries

## Mutual Adaptation

Measure:

- AI → Human influence
- Human → AI adaptation
- shared vocabulary
- increasing contextual fit
- reciprocal strategy adaptation
- persistent behavioural effects

## Joint Performance

Measure:

- time-to-insight
- novel connections
- contradictions found
- breadth
- depth
- idea-to-experiment conversion
- idea-to-output conversion
- research productivity
- long-term retrieval quality

Do not compress these into a single Coevolution Score.

Use a **Coevolution Profile**.

---

# 21. UI/UX Philosophy

The UI must combine two seemingly different ideas:

### Jarvis

Fast.

Ambient.

Intelligent.

Responsive.

Proactive.

Command-oriented.

Aware of system state.

### Research laboratory

Precise.

Evidence-based.

Historical.

Inspectable.

Traceable.

Calm.

Dense with meaning.

The desired principle is:

> **Make Nirixa feel like what Jarvis would look like if Tony Stark were a serious researcher.**

The UI must therefore feel futuristic without becoming generic cyberpunk.

---

# 22. Visual Identity

Primary aesthetic:

**Research Observatory + Jarvis Intelligence Layer**

Base:

```text
#0B0D13
#12151E
```

Primary text:

```text
#EDEAE3
```

Secondary:

```text
#9FA4B2
```

Accent:

```text
#C89B53
#E5A93C
```

Secondary semantic accent:

```text
#2E7D5B
```

Borders:

```text
rgba(255,255,255,0.07)
```

Typography:

### Newsreader

Use for:

- major intellectual questions
- research titles
- manuscript text
- formal headings

### Geist Sans

Use for:

- interface
- navigation
- controls
- metadata

### JetBrains Mono

Use for:

- EO IDs
- telemetry
- timestamps
- technical data
- system state
- agent status

---

# 23. Visual Rules

Avoid:

- generic SaaS dashboard
- Notion clone
- Obsidian clone
- neon cyberpunk
- excessive glassmorphism
- excessive gradients
- gamification
- childish icons
- excessive cards
- excessive rounded rectangles
- decorative graphs without meaning

Use:

- restrained HUD elements
- thin luminous lines
- subtle grids
- intelligent motion
- dark surfaces
- amber/white primary highlights
- restrained spectral colours for semantic categories
- dense but readable information
- cinematic spatial hierarchy

---

# 24. Information Architecture

Primary navigation:

```text
COCKPIT

Questions
Epistemic Objects
Discoveries
Challenges

Research
Writing

Evolution
Ask Nirixa

World Model
System

Settings
```

The navigation should remain compact.

Do not expose every database object as a top-level menu.

---

# 25. Cockpit

The Cockpit is the main screen.

Its question is:

> **What is intellectually alive right now?**

Not:

> What tasks do I have?

Not:

> What notes did I create?

Not:

> How many items are in the database?

The Cockpit should contain:

### Current Intellectual Focus

The EOs/questions currently receiving meaningful activity.

### Active Discoveries

Unexpected connections discovered by Nirixa.

### Active Challenges

Beliefs or assumptions currently being challenged.

### Compounding Radar

Longitudinal view of intellectual activity.

### Evolution

Recent human and AI changes.

### Research Horizon

Important unanswered questions.

### Output Pipeline

Potential outputs:

```text
Idea
→ Draft
→ Research
→ Manuscript
→ Published
```

### Capture Stream

Recent Telegram/raw captures requiring processing.

---

# 26. Jarvis Command Layer

A persistent command/search bar should be available globally.

Placeholder:

```text
Ask Nirixa about your thinking, graph, research, or anything...
```

It should accept:

- natural language
- questions
- commands
- references
- URLs
- pasted text
- research instructions

Examples:

```text
Why did I stop researching this?

Connect this to my previous work.

Find contradictions in my current beliefs.

Show everything related to contextual memory.

What should I investigate next?

Turn this into a research question.

Challenge this idea.

Find evidence against this.

Show me how this idea evolved.
```

---

# 27. Epistemic Object Screen

The EO screen is the primary research workspace.

Example:

```text
EO-004
Contextual Retrieval of Human Intentions
```

Header:

```text
Status
Maturity
Last meaningful work
Confidence
Research relevance
```

Sections:

```text
Overview

Questions

Current Understanding

Evidence

Counter-evidence

Beliefs

Answers

Connections

Work

Outputs

History
```

The UI must make intellectual lineage visible.

---

# 28. EO Connection Graph

The connection graph is one of Nirixa's signature interfaces.

It should not be a decorative "galaxy."

It should represent actual epistemic relationships.

Example:

```text
              Memory
                 │
                 │
          Contextual Retrieval
            /         \
           /           \
      Human Intent    AI Agents
          │              │
          │              │
       Cognition      Product Design
           \             /
            \           /
             Human-AI
             Coevolution
```

Nodes represent:

- EOs
- Questions
- Beliefs
- Evidence
- Outputs

Edges represent:

- supports
- contradicts
- extends
- derives
- refines
- inspired-by
- analogous-to
- generates

---

# 29. Graph Interaction

User must be able to:

- zoom
- pan
- search
- filter
- isolate an EO
- expand neighbours
- hide categories
- inspect relationship metadata
- inspect evidence
- inspect lineage
- jump to source
- jump to question
- jump to output
- view historical evolution

Time should be a graph dimension.

User should eventually be able to ask:

> Show how this thought evolved from 2026 to 2029.

The graph should animate or reconstruct lineage through time.

---

# 30. Discoveries Screen

Dedicated AI discovery inbox.

Headline:

> **I found something you didn't ask me to look for.**

Discovery types:

```text
Unexpected Connection
Contradiction
Forgotten Idea
Neglected Question
Research Opportunity
Pattern
Potential Experiment
Potential Output
```

Each discovery must explain:

```text
What I found
Why it matters
Objects involved
Evidence
Reasoning
Confidence
Potential consequence
```

Actions:

```text
Accept
Investigate
Dismiss
Save for later
Challenge
```

Acceptance does not automatically mean truth.

---

# 31. Challenges Screen

The Challenges screen contains active epistemic disagreements.

Each challenge should show:

```text
Claim
Why Nirixa is challenging it
Supporting evidence
Counter-evidence
Alternative explanation
Potential falsifier
Historical context
```

Actions:

```text
Defend
Investigate
Revise
Reject
Defer
```

---

# 32. Research Lab

Research should feel like a laboratory rather than a document library.

The PDF reader should support:

- PDF rendering
- search
- highlights
- annotations
- citation metadata
- page references
- source provenance
- linking highlighted material to EOs
- linking to Questions
- linking to Beliefs
- marking counter-evidence
- extracting claims
- comparing papers

Interaction:

```text
Highlight
    ↓
Classify
    ↓
Attach to EO
    ↓
Connect to Question/Belief
    ↓
Evaluate
```

Classification:

```text
Claim
Evidence
Method
Result
Counterargument
Definition
Observation
Limitation
```

---

# 33. Writing Studio

Writing must preserve intellectual lineage.

Supported output types:

```text
LinkedIn Post
Research Essay
Academic Paper
Book Chapter
Talk
Keynote
Product Concept
OSS Contribution
```

Writing Studio layout:

```text
LEFT
Draft

CENTER
Editor

RIGHT
Epistemic Lineage
```

The user should see:

```text
This paragraph
   ↓
EO-004
   ↓
Question Q-017
   ↓
Paper P-004
   ↓
Evidence E-032
   ↓
Belief B-019
```

This protects against unsupported writing.

---

# 34. Evolution Screen

Evolution is a longitudinal timeline.

It should show:

```text
Human Evolution
AI Evolution
Epistemic Evolution
Product Evolution
```

Example:

```text
2026
Question emerges

2026
Paper discovered

2027
Belief changes

2027
New experiment

2028
New EO decomposed

2028
Research paper

2029
Book chapter

2029
Keynote
```

A second track shows Nirixa:

```text
Nirixa v0.1
Capture

v0.3
Graph

v0.6
Discovery

v0.9
Research Agent

v1.2
Self Model
```

The goal is to make visible:

> **The product evolved with the person.**

---

# 35. Ask Nirixa Interface

This should feel like an AI command centre rather than a normal chat window.

The system should support question categories:

```text
ABOUT ME
ABOUT MY THINKING
ABOUT MY BELIEFS
ABOUT MY RESEARCH
ABOUT MY HISTORY
ABOUT MY EVOLUTION
ABOUT NIRIXA
ABOUT THE WORLD
```

Answers should preferentially include evidence and links into the graph.

---

# 36. World Model

World Model stores external reality.

Examples:

```text
People
Companies
Technologies
Papers
Books
Research
Events
Concepts
Datasets
Organizations
```

It must remain distinct from the user's beliefs.

For example:

```text
WORLD:
A paper claims X.

USER:
Believes X is plausible.

NIRIXA:
Confidence 0.63 that X explains Y.
```

Never collapse these three.

---

# 37. System Model

System Model represents Nirixa itself.

Track:

```text
Capabilities
Agents
Architecture
Models
Tools
Policies
Failures
Discoveries
Design Decisions
Experiments
Versions
Behaviour
```

Nirixa must be able to answer:

```text
Why did you make this discovery?

When did you gain this capability?

Which version introduced this behaviour?

What has changed in your reasoning?

Where do you still fail?
```

---

# 38. Telegram Capture Layer

Telegram is the primary mobile sensory interface.

Input types:

```text
Text
Voice
Image
Video
PDF
URL
Forwarded message
Document
```

Telegram should optimize for:

> **Minimum capture friction.**

The user should not have to categorize content manually.

Example:

```text
User:
"I just realized the way I remembered the heater reminds me of contextual retrieval."

Nirixa:
Captured.

Potential links:
EO-004
Question Q-017

Would you like me to investigate the connection?
```

The raw capture must remain intact.

---

# 39. Raw Capture Architecture

Capture should follow:

```text
Raw
 ↓
Normalize
 ↓
Interpret
 ↓
Candidate Objects
 ↓
Human Confirmation
 ↓
Canonical Knowledge
```

Never destroy raw material during processing.

---

# 40. Capture Provenance

Every capture must retain:

```text
source
timestamp
original content
sender
media type
processing history
AI interpretation
human modifications
final canonical objects
```

The system should be able to reconstruct:

> Where did this idea come from?

---

# 41. Local-First Architecture

Primary data substrate:

```text
SQLite
```

Database location:

```text
system/data/nirixa.db
```

Target implementation:

```text
better-sqlite3
```

Target:

```text
sub-30ms
```

for normal local queries.

The architecture should be local-first.

Cloud services should be optional.

The user's intellectual history must remain usable even if:

- an AI provider disappears
- an API changes
- the internet is unavailable
- a model changes
- a vendor shuts down

---

# 42. Source of Truth

Markdown + Git remains the human-readable archival layer.

SQLite is the operational index/query layer.

Conceptually:

```text
Markdown/Git
     +
SQLite
     +
AI Context Engine
```

Git provides:

- history
- diff
- rollback
- portability
- human-readable archive

SQLite provides:

- fast querying
- indexing
- graph traversal
- operational state

AI provides:

- interpretation
- discovery
- reasoning
- research
- interaction

No layer should become the sole representation of intellectual truth.

---

# 43. Model Agnosticism

AI models must be replaceable.

Do not hard-code Nirixa's intellectual model to one provider.

Architecture:

```text
Nirixa
   ↓
Model Abstraction Layer
   ↓
Gemini / Claude / OpenAI / Local Model / Future Model
```

The user's knowledge and graph must survive model changes.

---

# 44. Agent Architecture

Recommended conceptual agents:

```text
Capture Agent
Ingestion Agent
Research Agent
Context Agent
Discovery Agent
Challenge Agent
Writing Agent
Self-Model Agent
Evaluation Agent
System Agent
```

Agents should not create competing sources of truth.

They operate on shared canonical state.

---

# 45. Context Engine

Context is not the same as memory.

Use:

```text
Data
Memory
Knowledge
Context
```

Definitions:

```text
Data:
What happened.

Memory:
What was retained.

Knowledge:
What has been learned.

Context:
What is relevant now.
```

The Context Engine selects relevant information for a given task.

It should consider:

```text
Current question
EO
Goal
Recent activity
Historical context
Relevant beliefs
Contradictions
Evidence
User state
World state
```

---

# 46. Relevance Model

Relevance should not simply mean semantic similarity.

Candidate factors:

```text
Semantic relevance
Conceptual relevance
Temporal relevance
Goal relevance
Epistemic relevance
Contradiction relevance
User relevance
Novelty
Evidence strength
Recency
```

The system should favour information that changes reasoning, not merely information that sounds similar.

---

# 47. Search

Search must support:

### Semantic search

Find conceptually related material.

### Exact search

Find exact words/phrases.

### Graph search

Find connected objects.

### Temporal search

Find what was believed or known at a point in time.

Example:

> What did I think about AI memory before I read paper X?

### Provenance search

> Where did this belief originate?

### Counterfactual search

> What evidence have I encountered that should have made me reconsider this?

---

# 48. Knowledge Evolution

The system must preserve state changes.

Example:

```text
Belief:
AI memory is mostly retrieval.

↓ Paper

Belief challenged.

↓ Discussion

New hypothesis:
AI memory may involve active reconstruction.

↓ Experiment

Belief revised.
```

Never overwrite the original belief.

---

# 49. Conversation Memory

The ChatGPT conversation history must not be considered the project's permanent source of truth.

Important project conversations must eventually be captured into the project repository.

Recommended:

```text
project-memory/
    conversations/
        YYYY/
            YYYY-MM-DD-topic.md
```

Each conversation record should preserve:

```text
Raw conversation
Key decisions
New concepts
Rejected concepts
Open questions
Changed assumptions
Implementation consequences
```

Do not store only summaries.

The raw intellectual history matters.

---

# 50. Decision Register

Every meaningful product/architecture decision should be recorded.

Schema:

```text
Decision
Why
Alternatives
Rejected Alternatives
Consequences
Date
Status
```

Implementation agents should consult the decision register before asking questions.

---

# 51. Agent Decision Policy

The implementation agent must classify uncertainty.

## Blocking Question

Ask the user only when:

- conceptual behaviour is genuinely ambiguous
- two choices materially change the product
- privacy/security consequences are significant
- human authority is affected
- ontology semantics are uncertain

## Implementation Decision

Agent decides.

Examples:

- library choice
- component structure
- CSS implementation
- API shape
- caching
- test framework

Record decision.

## Technical Detail

Agent decides using standard engineering practice.

Do not interrupt user.

---

# 52. Personal vs Open Source Architecture

Two layers must remain separate.

## Personal Nirixa

Contains:

- personal history
- private thoughts
- career
- private conversations
- personal goals
- private documents
- personal graph

## Nirixa Open Source

Contains:

- generalized architecture
- ontology
- schemas
- workflows
- agents
- UI
- methodology
- documentation
- examples using synthetic/public data

Never commit private personal data to the public repository.

---

# 53. Open Source Objective

Nirixa should eventually be useful to people other than the original user.

A new user should be able to clone the project and establish:

```text
Their Questions
Their EOs
Their Beliefs
Their Evidence
Their Goals
Their Outputs
Their Evolution
```

The methodology should generalize.

The user's personal data must not be required for the architecture to function.

---

# 54. Security & Privacy

Default:

```text
Local-first
Private-by-default
Explicit external transmission
```

Sensitive data should not automatically leave the machine.

For external AI providers:

- show provider where appropriate
- minimize data
- preserve provenance
- allow configuration
- maintain local records of AI interactions

No silent transmission of the user's private intellectual archive.

---

# 55. Performance

Primary UX requirements:

```text
Local navigation: near-instant
Normal database queries: <30ms target
Graph interactions: smooth
Search: responsive
Capture: immediate acknowledgement
AI operations: asynchronous
```

Long-running operations should never block the interface.

Use background jobs.

---

# 56. Progressive Processing

A Telegram capture should not wait for every AI process to complete.

Example:

```text
0 sec
Capture confirmed

1–2 sec
Raw record stored

Background
Transcription

Background
Extraction

Background
EO matching

Background
Discovery

Background
Research

Background
User notification
```

---

# 57. Notifications

Nirixa should be proactive but not noisy.

Notification priority:

### High

Potential major contradiction.

### Medium

Unexpected high-value connection.

### Low

Potentially interesting pattern.

Avoid notifications for:

- routine classifications
- minor metadata
- low-confidence semantic similarity

The system must protect attention.

---

# 58. Quiet Mode

User investigates.

Nirixa stays mostly passive.

It supports retrieval and commands without interruption.

---

# 59. Active Mode

Nirixa may proactively surface:

```text
Discoveries
Challenges
Patterns
Research opportunities
Forgotten ideas
Neglected questions
```

The system must justify why the interruption matters.

---

# 60. Attention Budget

Nirixa must treat user attention as a constrained resource.

Every proactive intervention should have:

```text
importance
confidence
novelty
relevance
expected value
```

Low-value discoveries should be batched.

---

# 61. Outputs

Nirixa should allow epistemic work to become externalized.

Pipeline:

```text
Question
 ↓
EO
 ↓
Evidence
 ↓
Belief
 ↓
Work
 ↓
Synthesis
 ↓
Draft
 ↓
Output
 ↓
Outcome
```

Outputs must preserve lineage.

---

# 62. LinkedIn Workflow

A mature thought may become a LinkedIn post.

The system should show:

```text
Post
 ↓
EOs
 ↓
Questions
 ↓
Evidence
 ↓
Sources
 ↓
Beliefs
```

This prevents content from becoming detached from intellectual development.

The user should be able to see:

> Which intellectual work produced this post?

---

# 63. Research Workflow

Research flow:

```text
Capture
 ↓
Question
 ↓
Research
 ↓
Evidence
 ↓
Counter-evidence
 ↓
Belief
 ↓
Experiment
 ↓
Revision
 ↓
Paper
```

The system should support citation provenance throughout.

---

# 64. Book Workflow

Book chapters should emerge from mature epistemic objects.

Example:

```text
EO
 ↓
Questions
 ↓
Research
 ↓
Connections
 ↓
Synthesis
 ↓
Chapter
```

The system should warn if a chapter contains claims without supporting evidence.

---

# 65. Product Workflow

An EO can generate a product idea.

Example:

```text
Research
 ↓
Unmet problem
 ↓
Product hypothesis
 ↓
Prototype
 ↓
Experiment
 ↓
Outcome
```

Product outputs can subsequently generate new evidence.

---

# 66. Feedback Loop

The full system loop is:

```text
WORLD
  ↓
EVENT
  ↓
CAPTURE
  ↓
ENGAGEMENT
  ↓
EPISTEMIC WORK
  ↓
EPISTEMIC STATE
  ↓
OUTPUT
  ↓
OUTCOME
  ↓
NEW EVENT
  ↓
HUMAN EVOLUTION
  ↕
NIRIXA EVOLUTION
```

This is the central architecture.

---

# 67. Data Model Principles

Every important record should include:

```text
ID
Timestamp
Provenance
Actor
Relationships
Confidence
History
```

Where relevant.

The system must favour append/history-preserving structures over destructive updates.

---

# 68. Immutable History

Do not delete meaningful intellectual history.

Instead use:

```text
Superseded
Rejected
Archived
Invalidated
```

with explanation.

The user must be able to inspect historical state.

---

# 69. Uncertainty

Nirixa must represent uncertainty explicitly.

Examples:

```text
Confidence: 0.42
Evidence strength: Weak
Source quality: Moderate
Interpretation: AI-generated
Human verified: No
```

Avoid false precision.

Scores should explain what they measure.

---

# 70. No Fake Intelligence

Nirixa must not generate activity merely to make the system appear alive.

Examples of bad behaviour:

```text
Generating meaningless connections
Creating low-value questions
Writing generic summaries
Inventing discoveries
Producing excessive notifications
```

The product must optimize for meaningful epistemic progress, not database growth.

---

# 71. Acceptance Criteria

Nirixa is successful when the following scenarios work.

## Scenario 1 — Raw Thought

User sends a random thought through Telegram.

System:

- stores raw capture
- preserves timestamp
- identifies possible context
- proposes relevant EO/question
- preserves user confirmation boundary

---

## Scenario 2 — Podcast

User sends podcast.

System:

- ingests source
- extracts meaningful claims
- compares against graph
- discovers connections
- identifies contradictions
- generates questions
- preserves provenance

---

## Scenario 3 — Paper

User reads paper.

System:

- captures annotations
- connects claims to EOs
- records evidence
- identifies counter-evidence
- updates candidate understanding

---

## Scenario 4 — Belief Change

User changes mind.

System:

- preserves previous belief
- records new belief
- records reason
- identifies evidence
- records work responsible for change
- updates epistemic state

---

## Scenario 5 — Unexpected Discovery

Nirixa finds a connection the user never requested.

System:

- explains connection
- shows evidence
- identifies relationship
- provides confidence
- asks whether to investigate/canonize

---

## Scenario 6 — Challenge

Nirixa finds contradictory evidence.

System:

- surfaces contradiction
- presents counter-thesis
- shows supporting evidence
- proposes falsifier
- lets user respond

---

## Scenario 7 — Ask Nirixa

User asks:

> How have I changed since I started using Nirixa?

System reconstructs:

- questions
- beliefs
- work
- outputs
- outcomes
- intellectual metrics
- AI influence
- important turning points

---

## Scenario 8 — Thought Lineage

User selects an EO.

System shows:

```text
Origin
→ Questions
→ Evidence
→ Work
→ Beliefs
→ Connections
→ Outputs
→ Outcomes
```

---

## Scenario 9 — 2026 → 2029

User asks:

> Show how this idea evolved.

System reconstructs the thought across time.

---

## Scenario 10 — AI Influence

User asks:

> Which of my ideas were primarily discovered by AI?

System returns contribution lineage rather than a simplistic percentage.

---

# 72. Definition of Done

A feature is not complete merely because it renders.

It must satisfy:

```text
Functional
+
Epistemically correct
+
Historically traceable
+
Provenance preserving
+
Human authority preserved
+
Tested
+
Documented
```

---

# 73. Testing Strategy

Tests should cover:

### Ontology

Can objects be correctly distinguished?

### Provenance

Can every claim trace to its source?

### History

Can previous states be reconstructed?

### Attribution

Can human and AI contribution be separated?

### Autonomy

Can AI actions exceed their permitted authority?

### Discovery

Are meaningful connections distinguished from semantic noise?

### Retrieval

Does context retrieval surface useful information?

### Reversibility

Can wrong AI interpretations be rejected without losing history?

### Privacy

Does personal data remain isolated?

---

# 74. Research Validity

Nirixa must avoid designing its instrumentation to prove its desired thesis.

Research data should support:

```text
Positive findings
Negative findings
Null results
Contradictions
Unexpected effects
AI failure
Human failure
Dependency
Improvement
Regression
```

The system must be capable of showing:

> Persistent AI interaction did not improve this aspect of human reasoning.

That is a valid result.

---

# 75. Research Spine

The primary research structure is:

```text
Interaction
     ↓
Work
     ↓
Change
     ↓
Adaptation
     ↓
Future Interaction
```

Research questions:

### RQ-A — Human Evolution

How does persistent AI interaction change human reasoning, knowledge formation, questioning, and behaviour over time?

### RQ-B — AI Adaptation

How does persistent contextual interaction cause an AI system to adapt to an individual?

### RQ-C — Coevolution

What happens when both human and AI continuously adapt to one another over an extended period?

Nirixa is an experimental platform through which these questions can be observed.

Nirixa is not itself the PhD.

---

# 76. Product Evolution

Nirixa itself must have a history.

Track:

```text
Version
Capability
Architecture
Design
Agent behaviour
Research instrumentation
Failures
Discoveries
Decisions
```

The system should eventually allow:

> How did Nirixa become different because of me?

and:

> How did I become different because of Nirixa?

---

# 77. Intellectual Evolution

The ultimate longitudinal model is:

```text
Human
 ↓
Experience
 ↓
Question
 ↓
Epistemic Work
 ↓
Belief
 ↓
Knowledge
 ↓
Output
 ↓
Outcome
 ↓
Human'
```

Parallel:

```text
Nirixa
 ↓
Interaction
 ↓
Observation
 ↓
Adaptation
 ↓
Capability
 ↓
Behaviour
 ↓
Nirixa'
```

Together:

```text
Human₀ ↔ Nirixa₀
       ↓
Human₁ ↔ Nirixa₁
       ↓
Human₂ ↔ Nirixa₂
       ↓
Human₃ ↔ Nirixa₃
```

---

# 78. Implementation Priorities

Build in this order.

## Phase 1 — Foundation

- SQLite
- ontology
- provenance
- Markdown/Git integration
- raw capture
- event model
- basic graph

## Phase 2 — Epistemic Core

- Questions
- EOs
- Beliefs
- Evidence
- Answers
- Connections
- Epistemic Work
- History

## Phase 3 — AI Layer

- context engine
- discovery
- challenge
- research
- attribution
- autonomy controls

## Phase 4 — Interfaces

- Cockpit
- EO workspace
- Graph
- Discoveries
- Challenges
- Ask Nirixa
- Research Lab
- Writing Studio
- Evolution

## Phase 5 — Mobile

- Telegram
- voice
- image
- video
- PDF
- URL ingestion

## Phase 6 — Research Instrumentation

- human change metrics
- AI adaptation
- coevolution events
- evaluation
- longitudinal analysis

## Phase 7 — Open Source

- sanitize architecture
- documentation
- setup
- example dataset
- privacy boundary
- contribution workflow

---

# 79. UI Priority Order

Do not build every screen equally.

The first polished vertical slice should be:

```text
Telegram Capture
      ↓
Epistemic Object
      ↓
Connection Graph
      ↓
AI Discovery
      ↓
Ask Nirixa
```

This demonstrates the core product.

The second vertical slice:

```text
PDF
 ↓
Evidence
 ↓
EO
 ↓
Belief
 ↓
Challenge
```

The third:

```text
EO
 ↓
Writing Studio
 ↓
Output
 ↓
Outcome
```

The fourth:

```text
Human evolution
↕
AI evolution
↕
Nirixa evolution
```

---

# 80. UI State Requirements

Every major screen should support:

```text
Loading
Empty
Active
Error
Partial
Processing
AI Working
Needs Human Decision
Completed
Historical
```

Never display a blank screen while background intelligence is running.

Use meaningful system-state indicators.

---

# 81. AI Activity Visualization

AI processing should feel like an intelligent system operating in the background.

For example:

```text
NIRIXA

Reading source...
     ↓
Extracting claims...
     ↓
Comparing with 42 epistemic objects...
     ↓
Found 3 potential connections...
     ↓
Found 1 contradiction...
     ↓
Preparing discovery...
```

This should not become fake theatrical animation.

It must reflect real processing state.

---

# 82. Graph Visual Language

Graph semantics should be visible without overwhelming the user.

Possible encoding:

```text
Node size
= epistemic relevance

Edge thickness
= relationship strength

Edge style
= relationship type

Opacity
= confidence

Glow
= recent activity

Animation
= active change
```

Do not use visual effects merely for decoration.

---

# 83. Empty States

Empty states should teach the system.

Example:

```text
No Epistemic Objects yet.

Start with a question.

"What are you trying to understand?"
```

Discoveries:

```text
No discoveries yet.

Keep thinking.

Nirixa will look for connections you didn't ask for.
```

Challenges:

```text
Nothing is currently being challenged.

That may mean you're stable.
Or it may mean Nirixa isn't challenging you enough.
```

---

# 84. Error Philosophy

Errors should preserve intellectual continuity.

If AI processing fails:

```text
Raw capture preserved.
AI interpretation unavailable.
Retry when ready.
```

Never lose the user's original thought because an AI service failed.

---

# 85. Offline Behaviour

When offline:

- capture must work
- local search must work
- graph must work
- existing knowledge must remain accessible
- AI tasks can queue

Once online:

```text
Queued work
 ↓
Process
 ↓
Attach results
 ↓
Notify
```

---

# 86. Import / Export

Nirixa must remain portable.

Support eventually:

```text
Markdown
JSON
CSV
SQLite
Git repository
```

The user should never feel locked into Nirixa.

---

# 87. Long-Term Architecture Principle

Nirixa must survive:

```text
Model changes
Vendor changes
UI redesigns
Database migrations
AI capability jumps
Different devices
Different agents
Different research directions
```

The durable asset is:

> **The user's epistemic history.**

Not the model.

Not the interface.

Not the current agent.

---

# 88. Product North Star

The product's deepest question is:

> **Can we build a system that remembers not only what a person knows, but how that person came to know it, how their understanding changed, what challenged it, and how persistent interaction with AI changes both sides over time?**

---

# 89. Final Product Principle

Nirixa must not become a machine that tells the user what to think.

It should become a system that makes the user's thinking increasingly visible.

It should:

```text
Remember
Connect
Question
Challenge
Research
Reflect
Measure
Externalize
Learn
Adapt
```

But the final intellectual authority remains human.

The intended relationship is:

```text
Human asks.
Nirixa remembers.

Human investigates.
Nirixa connects.

Human believes.
Nirixa challenges.

Human changes.
Nirixa records.

Nirixa discovers.
Human evaluates.

Human creates.
Nirixa preserves the lineage.

Both adapt.
The system observes what happens.
```

The ultimate objective is not to create an AI that thinks for the user.

It is to create an environment in which **human thinking can compound instead of disappearing.**