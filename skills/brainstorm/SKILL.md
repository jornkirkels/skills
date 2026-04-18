---
name: brainstorm
description: "Use when a skill needs to clarify intent with the user, or when starting a conversation where the user's goal is unclear. Also use when the user says 'brainstorm,' 'think this through,' 'let's figure out,' or 'what should we do about.' Do NOT use for simple, direct requests with clear intent."
---

# Brainstorm

Reach shared understanding with the user through structured interview. Resolve every decision, then return a confirmed summary.

## Process

1. Extract decisions, constraints, and preferences already stated. Skip what is clear.
2. Map the decisions needed. Start from the stated goal. Order by dependency - decisions that constrain others come first.
3. Ask one question at a time. Provide multiple choice options where possible. Lead with your recommended answer and explain why. When only one sensible path exists, say so and move on.
4. When the answer is likely in the codebase, read files instead of asking. Only ask about preferences.
5. When a decision needs facts you lack, delegate research rather than guessing or asking the user to look it up.
6. Surface things the user likely has not considered that would meaningfully improve the outcome. Be a thinking partner, not a question-asker. Stay silent only when there is nothing worth adding.
7. When the user changes a decision, accept it and flag if it affects earlier decisions.
8. When all decisions from the initial map are resolved, stop. Fold in new relevant topics the user raises. Keep the conversation bounded.
9. Draft a structured summary. Group decisions logically. Preserve all decisions with their reasoning. Preserve nuances. Apply writing-clearly-and-concisely to the summary.
10. Present the summary for confirmation or changes.
11. Return the confirmed summary to the calling skill.

## Rules

- One question per message.
- Never narrate the process. The user sees questions and the summary.
- The calling skill determines what areas to cover. Brainstorm owns the interview method.
- Propose alternatives only when there is a genuine trade-off.
- Return the summary and stop. No file writes, no commits, no handoffs.
- State assumptions and move on when the answer is clear from context.
