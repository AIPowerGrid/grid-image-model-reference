# Model Reference Scripts

## Purpose

Validation, comparison, and controlled maintenance utilities for the image
model reference catalog consumed by the media worker.

## Ownership

- `validate_stable_diffusion.py` - schema/content validation.
- `compare_pr_to_main.py` - catalog change review helper.
- `no_extra_fields.py` - strict field check.
- `modify.py` - bulk catalog maintenance.
- `requirements*.txt` - task-specific script dependencies.

## Local Contracts

- Preserve deterministic ordering and schema-valid output; avoid broad
  mechanical churn unrelated to the intended model update.
- Treat upstream URLs, hashes, filenames, model families, and capabilities as
  supply-chain data. Verify them from authoritative sources before merging.
- Maintenance scripts must not silently rewrite the catalog by default; make
  write mode explicit and review the diff.

## Work Guidance

- Prefer validation from parsed JSON/schema over text replacement.
- Update catalog documentation and media-worker assumptions when fields or
  semantics change.

## Verification

- Install the narrow relevant `requirements*.txt` set.
- Run strict field and stable-diffusion validation over the complete catalog.
- Compare the final catalog against main and run `git diff --check`.

## Child DOX Index

No child guides are currently required; this file owns `scripts/`.
