# Fit Evidence into a Context Budget

A context budget turns retrieval ranking into a selection problem. Relevance order alone is insufficient because every selected passage consumes capacity.

This simple policy preserves relevance priority and skips oversized candidates. It is deterministic and easy to inspect, but can miss combinations with higher total relevance.

Construct two medium passages whose combined score exceeds one large passage. Explain when you might prefer a different selection policy, and where you would reserve tokens for the prompt and generated answer.

Concept reference: https://huggingface.co/learn/llm-course/chapter5/6
