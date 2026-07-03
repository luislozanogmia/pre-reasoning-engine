# Changelog

## v3.1.0

CPU inference is 4-6x faster. No API changes, no new dependencies, identical
outputs (verified byte-identical on a 12-prompt reference suite). All
optimizations are pure PyTorch and process-safe: nothing global is modified,
so other models running in the same client process are unaffected.

- KV cache in `generate()`: the prompt is encoded once, then each new token
  runs a single incremental step instead of re-processing the full sequence.
  Long-sequence fallback to the original loop is automatic (> max_seq_len).
- Functional fast path for incremental steps (same tensor ops without
  nn.Module dispatch overhead) under `torch.inference_mode()`.
- Scoped thread pinning: single-token steps run at 4 threads during
  `generate()` only; the caller's `torch.get_num_threads()` setting is
  saved and restored, never changed globally.
- Engine singleton: `get_engine()`/`analyze()` reuse one engine per
  (checkpoint, device) instead of reloading the checkpoint each call.
- Persistent E4 closure-window cache: canonical 2-hop windows are
  deterministic (greedy decode, fixed weights), so results are memoized on
  the model instance across calls.
- Escape hatches (env vars, all default-off): `PRE_REASONING_DISABLE_KV=1`
  (original generate loop), `PRE_REASONING_NO_FASTSTEP=1` (module-based
  incremental steps), `PRE_REASONING_THREADS=N` (thread pin override, 0 =
  never touch threading), `PRE_REASONING_NO_ENGINE_CACHE=1` (rebuild engine
  per call), `PRE_REASONING_NO_F5_CACHE=1` (per-pass closure cache only).

## v3.0.0

- Upgraded to 13.7M trainable parameter MoE model (v4, 5 expert groups) as the standalone engine.
- Transitive closure is now computed by the built-in E4 expert. The external derive_expert package is no longer needed.
- Renamed internal modules: engine.py (was pre_reasoning_v2_5_2.py), engine_core.py (was pre_reasoning_v2_5.py).
- Checkpoint upgraded from 3M (11MB) to 13.7M trainable parameters (85MB file, 22.1M tensor values including fixed masks).
- Removed derive_expert sub-package from the distribution.
- Fixed broken imports caused by the module rename.

## v2.5.4

- Added derive-expert neural transitive-closure enrichment to the default engine.
- Bundled `derive_expert` and `thin_expert_d128L3.safetensors` with the package.
- CLI and package-level APIs now route through the enriched engine while preserving the legacy v2.5 engine alias.

## v2.5.3

- Documentation only: removed internal stage labels (V2 / V3) from the public docs (README, CHANGELOG, skill descriptor). The package is presented as a single v2.5 engine: neural perception plus graph reasoning. No code, API, or behavior changes.

## v2.5.2

- Fixed graph linking that flattened transitive impact scores to 1 on plain-English problems.
  - `entity_match` no longer links two entities on shared stopwords ("the", "a", "of", ...); only content words can form an edge. Previously, phrases like "the missing skill" and "the cheapest test" matched on "the", collapsing distinct nodes into a star and flattening impact.
  - `_build_entity_overlap_edges` now lets an already-parented node acquire children (only the child must be an orphan), so a node in the middle of a chain connects the nodes below it instead of fragmenting one long chain into disjoint pairs. The `j > i` rule is kept, so edges run low->high index and the graph stays acyclic.
- Net effect: a 4-node dependency chain now reports transitive impact 0/1/2/3 (was 1/1/1/1), and root blockers are identified correctly.

## v2.5.1

- torch and safetensors are now required dependencies -- the engine always runs in full mode (neural perception + graph reasoning).
- Removed `[neural]` optional extra and deterministic-only fallback.

## v2.5.0

- Neural perception engine: 3M-parameter model trained on reasoning graphs, bundled as weights-only safetensors.
- v2.5 engine: neural perception + graph reasoning.
- Package-level `analyze()` and `pulse()` API.
- CLI entry point: `pre-reasoning "your problem text"`.
- Pytest coverage for analysis, cycles, conflicts, and pulse checks.
- PyPI packaging with torch and safetensors bundled.
- Claude Code adoption docs and agent skill descriptor.
- MIT license.
