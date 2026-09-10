# Decision Log

1. **AppleSupport as the brand** — enough historical volume with a coherent technical-support domain.
2. **Small custom intent taxonomy** — keeps labels actionable and avoids importing an unrelated taxonomy.
3. **`other_unknown` class** — prevents forced classification of context-poor messages.
4. **TF-IDF baseline first** — fast, transparent, reproducible, and strong enough to expose data/label issues.
5. **Class-balanced logistic regression** — compensates for minority intents during development.
6. **Historical retrieval before generation** — the assignment values brand-grounded responses over generic chatbot behavior.
7. **Customer-message retrieval** — similarity is based on the problem the customer described, not on support boilerplate.
8. **Pair retrieval with support response** — lets retrieved examples serve as both precedent and response evidence.
9. **Conservative escalation** — unsafe/unsupported automation is worse than a human handoff.
10. **Low-similarity escalation** — the system should not invent a resolution when precedent is weak.
11. **No autonomous account/device actions** — the dataset cannot safely justify operational access.
12. **No fabricated LLM judge score** — evaluation credibility matters more than filling every metric cell.
13. **No full raw dataset in repository** — reduces repository size and avoids redistributing the complete source dataset.
14. **Headline number labeled as development-only** — the 200-example set is too small for a production claim.
15. **Separate handoff from resolution evidence** — many historical replies route customers to DM and should not be mistaken for complete public fixes.
