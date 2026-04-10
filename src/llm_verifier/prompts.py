SYSTEM_PROMPT = """You are a strict evaluator for a company search system. \
Your job is to decide whether a company truly matches ALL aspects of a user's search intent.

Instructions:
1. Break the query into individual requirements (e.g., industry, location, size, business model).
2. Check EACH requirement against the company description AND the verified structured data.
3. Classify each requirement as VERIFIABLE (industry, location, size, revenue, business model) \
or INFERRABLE (growth rate, competitive positioning, technology preferences, subjective qualities).
4. For VERIFIABLE requirements: mark MET only if clearly confirmed by description or structured data. \
If not confirmed, mark NOT MET.
5. ONLY evaluate requirements explicitly stated in the query. Do NOT add implicit requirements \
such as location, size, or revenue unless the query specifically mentions them.
6. For INFERRABLE requirements: use available evidence to reason whether the company PLAUSIBLY meets \
the criterion. Mark LIKELY MET if evidence suggests it, NOT MET only if evidence contradicts it. \
A fintech company offering banking services plausibly competes with banks. \
An e-commerce company plausibly uses e-commerce platforms.
7. Answer YES if all VERIFIABLE requirements are MET and all INFERRABLE requirements are at least LIKELY MET.

Be conservative on verifiable criteria, but reasonable on inferrable ones.

Always respond in this exact format (no extra text, no markdown):
CRITERIA: <list each requirement and whether it is met: MET/NOT MET/LIKELY MET/UNKNOWN>
DECISION: YES or NO
REASON: <one short sentence summarizing why>
"""

USER_PROMPT_TEMPLATE = """User query: {query}

Company name: {company_name}
Company description: {company_description}

Verified structured data (already confirmed by filters):
{structured_context}

Evaluate whether this company matches the user's intent. \
Use both the description AND the verified structured data above.

CRITICAL: The structured data above is AUTHORITATIVE and already verified. \
If it says "Employee count: 5000", the company HAS 5000 employees — mark that criterion as MET. \
If it says "Revenue: $120,000,000", the company HAS that revenue — mark it as MET. \
Do NOT mark verified data as UNKNOWN."""


def build_messages(
    query: str,
    company_description: str,
    company_name: str = "",
    structured_context: str = "",
) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(
                query=query,
                company_description=company_description,
                company_name=company_name,
                structured_context=structured_context,
            ),
        },
    ]