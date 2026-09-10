# Hiver SDE Intern — AppleSupport AI Agent

## 1. Problem framing

Customer-support automation fails when it answers from generic knowledge rather than the brand's own support behavior. I therefore framed the task as a constrained pipeline: infer a small AppleSupport intent, retrieve similar historical customer/support interactions, produce a reply grounded in those interactions, and escalate when the evidence or risk profile is unsuitable for automation.

The dataset's response IDs make it possible to reconstruct conversations. I selected AppleSupport because it provides substantial historical volume while remaining a coherent technical-support domain.

### Intent taxonomy

`battery_charging`, `ios_update`, `app_problem`, `connectivity`, `account_access_security`, `store_payment`, `media_services`, `notifications_messaging`, `device_hardware_features`, `device_performance`, `data_backup_sync`, `how_to_information`, `other_unknown`.

`other_unknown` is deliberate: forcing ambiguous follow-ups into a specific intent creates false confidence.

## 2. System

1. **Intent classifier:** TF-IDF word/phrase features + class-balanced logistic regression.
2. **Historical retriever:** TF-IDF cosine similarity over 100k+ reconstructed AppleSupport customer→support pairs.
3. **Grounded response:** return a historically observed support response when evidence is sufficient; otherwise route to human support.
4. **Escalation gate:** catches safety/fraud/security/severe-device cases and weak retrieval evidence.
5. **LLM judge harness:** scores groundedness, relevance, helpfulness, safety, and style. Human-agreement collection is intentionally separated so no agreement is fabricated.

## 3. Evaluation

The 200-example golden set contains hand-reviewed intent and escalation labels.

| Baseline | Accuracy | Macro-F1 |
|---|---:|---:|
| Majority | 26.5% ± 1.2% | 0.034 ± 0.002 |
| TF-IDF + Logistic Regression | **32.0% ± 6.8%** | **0.219 ± 0.069** |

Evaluation uses 5-fold stratified cross-validation. The baseline is intentionally simple and reproducible.

### Important limitation

This is not a final unbiased end-to-end score. The golden set is small and class-imbalanced; rare intents make macro-F1 unstable. The retrieval corpus must also be evaluated with conversation/thread-level exclusion to avoid leakage. These constraints are explicitly called out rather than hidden behind a single headline number.

## 4. Escalation policy

Auto-handle is permitted only when there is sufficient historical evidence and no high-risk trigger. Human escalation is preferred for account/security issues, suspected fraud, safety symptoms, severe/persistent device failures, and weak retrieval evidence.

This is a conservative design choice: a wrong support instruction has higher cost than asking a specialist to take over.

## 5. Top failure modes

### 1. Context-poor follow-ups

Examples such as version numbers or “OK” cannot reliably establish an intent. Hypothesis: a conversation-aware model with previous turns would outperform single-message classification.

### 2. Overlapping symptoms

Battery drain, overheating, freezing, and slow performance overlap. Hypothesis: hierarchical classification (problem family → specific intent) would reduce confusion.

### 3. Update/app ambiguity

Customers frequently mention an OS update while the actionable problem is an app crash. Hypothesis: classify the customer's requested outcome rather than keyword presence.

### 4. Rare classes

Account/security, backup/sync, and how-to examples are sparse. Hypothesis: active sampling and second-pass annotation should focus on minority intents.

### 5. DM-routing responses

Historical AppleSupport replies often request a DM. These are useful evidence of escalation behavior but weak evidence for a public technical resolution. Hypothesis: evidence should be tagged as `resolution`, `troubleshooting`, or `handoff` rather than treated uniformly.

## 6. What is misleading about my headline number?

The 32% accuracy number is easy to misread as “the agent is only 32% useful.” It is actually a development score for one component: intent classification. It does not measure retrieval quality, response groundedness, or escalation safety. Conversely, it should not be interpreted as a production-quality benchmark because the 200-example set is small and not yet a frozen, thread-level held-out test set.

The honest conclusion is: **the pipeline is runnable and the evaluation scaffolding is in place, but the next measurement step is a larger, conversation-separated test set plus human-validated reply scoring.**

## 7. One-more-week plan

- 500–1,000 examples with two annotators.
- Conversation/time-based train/test split.
- Dense embeddings + reranker.
- LLM response synthesis constrained to retrieved evidence.
- Human-calibrated escalation threshold.
- 50–100 human-scored replies and LLM-vs-human agreement analysis.

## 8. Decision log summary

See `DECISION_LOG.md` for the non-obvious design choices and rationale.
