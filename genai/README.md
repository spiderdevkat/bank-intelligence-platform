# GenAI — Phase 6 & 7 Notes

## Text-to-SQL (raw API vs LangChain)
Built the same schema-aware text-to-SQL twice — once with raw Gemini API
calls, once with LangChain's PromptTemplate + pipe syntax. Both produced
nearly identical, correct SQL. LangChain didn't add safety or correctness
on its own — our hand-written `validate_sql()` guardrail (block non-SELECT,
block dangerous keywords) had to run regardless of which approach generated
the query. LangChain's real value shows up in agent/tool orchestration
(checkpoint 7.4), not in this simple single-call case.

## Notable setup issues hit along the way
- `google-generativeai` is fully deprecated — migrated to `google-genai`.
- `gemini-2.0-flash` returned `limit: 0` (free tier moved to newer models) —
  switched to `gemini-3.1-flash-lite`.
- `greenlet` (a LangChain/SQLAlchemy dependency) failed to compile from
  source on Windows + old Python 3.9 + old MSVC Build Tools — fixed with
  `pip install --only-binary :all: greenlet` to force a pre-built wheel.
- Gemini embedding free tier is rate-limited to 100 requests/minute —
  built automatic retry-with-backoff into the embedding pipeline rather
  than manually re-running on failure.

## Agent (checkpoint 7.4)
The LangChain `AgentExecutor` + `create_tool_calling_agent` pattern failed
against Gemini 3.x models with a `thought_signature` error — a known,
current compatibility gap between LangChain's legacy agent executor and
Gemini 3's mandatory reasoning-signature requirement, not fixable by
upgrading within this project's Python 3.9 constraint. Rebuilt the agent
using the raw `google-genai` SDK directly with a manual tool-calling loop
instead — same three tools (query_database, search_news,
score_account_fraud_risk), full control over conversation history, no
framework-version fighting. Verified against a real flagged account:
correctly identified both structuring and velocity fraud patterns from
raw transaction data, cited a real 71% ML-model risk score, and produced
a genuine investigation memo with actionable recommendations.