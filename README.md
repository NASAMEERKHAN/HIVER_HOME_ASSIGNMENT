# AppleSupport AI Support Agent — Hiver SDE Intern Take-Home

A reproducible prototype that turns the Customer Support on Twitter dataset into an AppleSupport-focused support agent. The system classifies intent, retrieves historically similar AppleSupport interactions, drafts an evidence-grounded response, and decides whether to handle automatically or escalate.

## Why AppleSupport?

AppleSupport has enough historical volume to support meaningful retrieval while keeping the domain coherent: device performance, iOS updates, battery/charging, apps, connectivity, accounts/security, payments, media services, notifications, hardware, backup/sync, how-to questions, and unknown/insufficient-context requests.

## Architecture

`customer message -> intent classifier -> historical retrieval -> escalation gate -> grounded reply`

- **Intent:** TF-IDF (1–2 grams) + class-balanced logistic regression trained on the 200-example golden set.
- **Retrieval:** TF-IDF cosine similarity over historical customer messages paired with AppleSupport responses.
- **Grounding:** the non-escalated reply is selected from a historically observed AppleSupport response rather than inventing troubleshooting facts.
- **Escalation:** explicit safety/security/financial/severe-device triggers plus a low-evidence threshold.
- **LLM judge:** included as a provider-agnostic harness; no fabricated judge or human-agreement scores are reported.

## Reproduce in under 15 minutes

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python evaluation/evaluate_baselines.py
python demo.py
```

The repository contains the reduced AppleSupport evidence corpus and 200-example golden set, not the original 500+ MB raw dataset.

## Headline development results

5-fold stratified cross-validation on the 200-example golden set:

| Model | Accuracy | Macro-F1 |
|---|---:|---:|
| Majority baseline | **26.5% ± 1.2%** | **0.034 ± 0.002** |
| TF-IDF + Logistic Regression | **32.0% ± 6.8%** | **0.219 ± 0.069** |

These are **development-set classifier results**, not an end-to-end agent score. Several intents have very few examples, so macro-F1 is unstable.

## Golden set

`data/apple_golden_set.csv` contains 200 manually reviewed examples with:
- intent label
- handle/escalate decision
- escalation reason
- annotator notes

Intent labels are intentionally small and Apple-specific rather than copied from a generic banking taxonomy.

## What is misleading about my headline number?

The 35.0% classifier accuracy can look like a weak complete-agent score, but it is only one component of the system. More importantly, the golden set was created as a compact development/evaluation artifact and contains rare classes with 2–4 examples. A future final evaluation should hold out entire conversation threads and freeze the taxonomy before measuring the production candidate. Therefore this submission does **not** claim that 35% is the expected production accuracy.

## Top failure modes

1. **Short context / follow-ups:** messages such as “11.0.3” or “OK” contain too little information to infer intent safely.
2. **Overlapping device symptoms:** battery drain, overheating, freezing, and slow performance can describe the same underlying incident.
3. **Update vs app problems:** customers often mention an iOS update while the actual intent is an app crash.
4. **Rare intents:** account/security, backup/sync, and how-to categories have few labeled examples.
5. **Historical replies often route to DM:** the dataset contains many support responses that move the case to private support rather than publicly documenting a resolution.

## What I did not build

- No autonomous execution of account/device changes.
- No claim that a historical tweet is a universally correct troubleshooting procedure.
- No fine-tuning on the full corpus.
- No fabricated LLM-judge agreement score.
- No production authentication, PII store, ticketing integration, or live Apple API access.

## One more week

1. Expand the golden set to 500–1,000 examples and double-annotate it.
2. Split by conversation/thread and time to prevent retrieval leakage.
3. Add embedding retrieval and a cross-encoder reranker.
4. Use an LLM to synthesize replies while forcing citation of retrieved evidence.
5. Calibrate escalation thresholds against human reviewer decisions.
6. Run the judge on 50–100 examples and compare it against human scores before using it as a headline metric.

## Data attribution

The underlying dataset is **Customer Support on Twitter** by Thought Vector and collaborators, distributed through Kaggle. It contains anonymized tweets/replies and response IDs that allow conversation reconstruction. The Kaggle page describes it as a corpus of over 3 million tweets/replies and lists a CC BY-NC-SA 4.0 license; it also asks users to contact Thought Vector for commercial applications/full-dataset use. See the official dataset page: https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter

This repository intentionally ships a reduced AppleSupport-derived corpus rather than redistributing the full raw dataset.
