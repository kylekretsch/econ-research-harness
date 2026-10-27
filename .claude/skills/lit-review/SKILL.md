---
name: lit-review
description: Find and summarize related economics literature with verified citations (NBER, SSRN, RePEc/IDEAS, journal sites, Google Scholar, OpenAlex). Use when the user asks for related work, a literature review, or citations.
---

# Literature review

1. Search with WebSearch / WebFetch; prefer OpenAlex API (`https://api.openalex.org/works?search=...`) and
   journal/NBER/RePEc pages for metadata.
2. **Verify every paper exists**: open its DOI or landing page. If you cannot verify it, do not cite it.
3. For each paper record in `notes/literature.md`:
   `### Author (Year) — Title` · DOI/URL · question · data · identification · main finding (with magnitude) · relevance to us.
4. Add a BibTeX entry to `paper/refs.bib` (key `AuthorYear`) including `doi` or `url`. Prefer the DOI's official BibTeX
   (`curl -LH "Accept: application/x-bibtex" https://doi.org/<doi>`).
5. Synthesize: what's settled, what's contested, where our contribution fits. Distinguish what papers *show* from what you infer.
