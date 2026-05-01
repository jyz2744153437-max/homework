# Trae rules for bibliometrics-mini

You are pair-programming a minimal Python bibliometrics project for a course.

Hard rules:
1. Do not change formulas without explicitly explaining the change.
2. Co-citation matrix: C = A.T @ A, where A is paper-reference incidence.
3. Bibliographic coupling matrix: B = A @ A.T.
4. For NetworkX betweenness on similarity-weighted networks, create a distance attribute as 1 / weight and use weight='distance'.
5. Never hard-code API keys. Read OPENALEX_API_KEY from environment variables.
6. Output paths must stay fixed: outputs/tables, outputs/figures, reports.
7. Every function must have a docstring and must be testable on the sample data.
8. Prefer small, reviewable changes over rewriting the whole project.
