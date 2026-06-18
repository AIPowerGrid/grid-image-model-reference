# DOX framework

- DOX is a hierarchy of AGENTS.md files that carry the durable contracts for this repo.
- Agents must follow the DOX chain on every edit.

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees.
- Any work product must stay understandable from the nearest AGENTS.md plus every parent above it.

## Read Before Editing

1. Read this root AGENTS.md.
2. Identify every path you expect to touch.
3. Walk from repo root to each target, reading every AGENTS.md on the way.
4. The nearest AGENTS.md is the local contract; parents hold repo-wide rules.
5. If docs conflict, the closer doc controls local detail, but no child may weaken DOX.

Do not rely on memory — re-read the applicable chain in-session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done. Update the closest
owning AGENTS.md when a change affects: purpose/scope/ownership; durable structure,
contracts, or workflows; inputs/outputs/permissions/side-effects; or the Child DOX Index.
Remove stale text immediately. Refresh affected parent and child indexes.

## Style

Concise, current, operational. Stable contracts, not diary entries. Broad rules in parents,
concrete detail in children. Delete stale notes instead of explaining history.

---

# grid-image-model-reference — image model definitions for the grid

## Purpose

A DATA repo: curated JSON definitions of the image models, ControlNets, LoRAs, embeddings,
and dependencies the grid knows about. It is the translation layer between **ComfyUI**
naming and **AI Power Grid** model names, consumed by
[grid-comfy-bridge](https://github.com/AIPowerGrid/grid-comfy-bridge) to resolve, validate, and
download models. There is almost no runtime code here — the deliverables are the JSON files.

## Ownership

- **`stable_diffusion.json`** — primary checkpoint reference (~26 entries). Each key is a
  grid model name; value carries `baseline`, `type`, `config.files[]` (path + sha256/md5),
  and `config.download[]` (file_name/file_path/file_url). This is the canonical file the
  validation CI and `scripts/` operate on.
- **`stable_diffusion.schema.json`** — JSON Schema for the checkpoint records. The contract
  the validator enforces against `stable_diffusion.json`.
- **`stable_diffusion_old.json`** — legacy/archived checkpoint set (large). Not validated by
  CI; retained for reference, not the live source.
- **`controlnet.json`** — ControlNet model definitions (files + download records, per baseline).
- **`lora.json`** — flat JSON array of CivitAI LoRA numeric IDs the grid allows.
- **`db_embeds.json`** — textual-inversion / embedding definitions (`EmbedName`, `EmbedType`,
  `DownloadPath`, `baseline`).
- **`db_dep.json`** — shared model dependencies (CLIP, GFPGAN, etc.) with download + unzip rules.
- **`miscellaneous.json`** — auxiliary models (e.g. layer-diffuse) not fitting the above.
- **`diffusers.json`** — diffusers-format models; currently empty (`{}`).
- **`validate_urls.py`** — standalone helper to HEAD/GET every download URL (`--validate`) and
  optionally standardize entries to the `config.download[]` format (`--standardize`; writes only
  with `--apply`, otherwise dry-run).
- **`scripts/`** — validation + authoring helpers (schema validation via
  `horde_model_reference`, the interactive `modify.py` add/update CLI, PR-diff tooling). Thin
  tooling, not a durable boundary; documented here.
- **`.github/workflows/`** — CI: validate the reference on PR/main, diff PR vs main, release.

## Local Contracts

- **Inherit org engineering standards:** /Users/j/fix-axios-vuln/aipg-documentation/engineering-standards/
  (core + git + the matching language file).
- **JSON is the product.** Edits are data edits. Keep keys = grid model names; preserve the
  existing record shape so grid-comfy-bridge's resolver does not break.
- **`stable_diffusion.json` must validate** against `stable_diffusion.schema.json` and the
  `horde_model_reference` legacy validator — no extra fields (CI runs with `fail_on_extra`).
- **Checksums are load-bearing.** When adding/updating a checkpoint, set the real
  `sha256sum` for each downloadable file; bridge integrity checks depend on it.
- **Multiple ComfyUI names per model** is intentional (aliases/file names/community names) —
  do not collapse them.
- Do not edit `stable_diffusion_old.json` for live changes; it is archival.

## Work Guidance

- Add/update/remove checkpoints with `scripts/modify.py` (computes sha256, fills `config`),
  or hand-edit JSON keeping the schema shape.
- After URL or download changes, run `validate_urls.py --validate` to confirm reachability.
- Match existing indentation/formatting per file (tabs vs 4-space spaces vary across files;
  follow the file you are editing). `black`/`ruff`/`pre-commit` govern the Python helpers.

## Verification

- `tox` runs the full gate: `pre-commit`, `validate-sd`
  (`scripts/validate_stable_diffusion.py`), and `no-extra-fields`
  (`scripts/no_extra_fields.py`).
- `python scripts/validate_stable_diffusion.py` — schema-validate `stable_diffusion.json`.
- `python validate_urls.py --validate` — check download URL reachability.

## Child DOX Index

- (none) — single-file DOX; `scripts/` and the JSON files are documented above.
