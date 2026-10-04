#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic release gate for the award-grade-design skill.

Usage:
    python scripts/run_evals.py [skill-dir]

Exit code 0 means every deterministic check passed. Exit code 1 means at least
one failed; each failure prints the file and the concrete problem.

Standard library only -- this must run anywhere, with no install step, because a
gate that needs setup is a gate that gets skipped.

What this does NOT cover: stage routing quality against real prompts, scope
discipline under ambiguity, and profile activation judgement. Those need a model
or a human, and belong to the qualitative track described in
`evals/evolution-policy.yaml`.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# --- configuration -----------------------------------------------------------

RESOURCE_DIRS = (
    "agents",
    "evals",
    "packs",
    "profiles",
    "references",
    "routing",
    "schemas",
    "scripts",
    "stages",
    "templates",
)

TEXT_SUFFIXES = (".md", ".yaml", ".yml", ".json", ".py", ".txt")

EXPECTED_STAGES = (
    "audit",
    "direction",
    "design-system",
    "page",
    "component",
    "implementation",
    "visual-qa",
    "optimization",
)

# The single implementation-strategy vocabulary. Every file that defines the set
# must define all of it -- a stage that silently drops one produces mappings the
# next stage cannot classify.
STRATEGY_TOKENS = ("REUSE", "CONFIGURE", "WRAP", "EXTEND", "REPLACE", "CREATE")
STRATEGY_UPPERCASE_SITES = (
    "references/design-to-code-protocol.md",
    "stages/component.md",
    "stages/implementation.md",
    "templates/implementation-plan-deep.md",
)
STRATEGY_KEY_SITES = (
    "schemas/design-spec.json",
    "templates/design-specification.yaml",
)
# The human-readable mirror of the spec template drifts more easily than the
# machine-checked yaml: nothing forces it to keep the full vocabulary, so a
# "Reuse / Extend / Replace / Create" shorthand can creep back in unnoticed.
STRATEGY_LOWERCASE_SITES = (
    "templates/design-specification.md",
)

# The high-density information flow. The reference, the profile, the stage file
# and the high-density pack each state it; if the segment sets diverge, a Page
# DSL author cannot tell which version is authoritative. v8.9 shipped
# "converged" while the pack still carried the old five-segment list -- a
# convergence claim only covers the files a check enumerates.
INFO_FLOW_FILES = (
    "references/page-archetype-contract.md",
    "profiles/vue3-antdv-tailwind/data-intensive-ui.md",
    "stages/page.md",
    "packs/high-density.md",
)
INFO_FLOW_ANCHOR = "Context"

# Numbers restated in more than one file must agree everywhere they appear --
# the v8.9 lesson generalizes beyond the info flow: drift survives wherever a
# check does not look. Dimension labels drift more easily than the numbers
# themselves ("perf" vs "Performance"), so the hard gates compare ordered
# threshold sequences, not labels.
AWARD_WEIGHT_FILES = ("SKILL.md", "references/award-benchmarks.md")
HARD_GATE_FILES = (
    ("SKILL.md", r"默认硬门槛：.*?才作为硬门槛。", r"≥\s*(\d+\.\d+)"),
    (
        "references/design-review-rubric.md",
        r"##\s*硬门槛.*?```text\s*\n(.*?)```",
        r"<\s*(\d+\.\d+)",
    ),
)
TOKEN_THRESHOLD_FILES = (
    "references/design-token-contract.md",
    "packs/design-system.md",
    "profiles/vue3-antdv-tailwind/tailwind-guidance.md",
    "profiles/vue3-antdv-tailwind/tailwind-implementation.md",
)

# Checks that only fire when their environment exists: readme-listing needs a
# parent README.md. The registry sync must not read their absence from RESULTS
# as drift when the policy explicitly allows the skip.
CONDITIONAL_CHECKS = {
    "package-hygiene.readme-listing": lambda root: (root.parent / "README.md").is_file(),
}

# Example scope contract's context.packs entries must resolve to real pack files.
SCOPE_CONTRACT_TEMPLATE = "templates/stage-scope-contract.yaml"

# Files that must all carry the same release version.
VERSION_PATTERNS = (
    ("SKILL.md", r"^#\s+.*?\bv(\d+(?:\.\d+)*)", "H1"),
    ("SKILL.md", r"^version:\s*(\S+)", "frontmatter"),
    ("profiles/vue3-antdv-tailwind/profile.yaml", r"^\s+version:\s*(\S+)", "profile"),
    ("routing/stage-router.yaml", r"^version:\s*(\S+)", "stage-router"),
    ("routing/scope-router.yaml", r"^version:\s*(\S+)", "scope-router"),
    ("routing/resource-map.yaml", r"^version:\s*(\S+)", "resource-map"),
    ("evals/evolution-policy.yaml", r"^version:\s*(\S+)", "evolution-policy"),
)

# A path-shaped reference to a bundled resource. `{}` is deliberately allowed
# inside the match so that an unresolved template placeholder is captured and
# then reported, instead of silently slipping through as "not a path".
PATH_REF_RE = re.compile(
    r"(?<![\w/.\-])"
    r"((?:agents|evals|packs|profiles|references|routing|schemas|scripts|stages|templates)"
    r"/[A-Za-z0-9_./\-{}]+\.(?:md|ya?ml|json|py))"
)

# The gate is tooling, not a resource consumer: it must not satisfy a reference
# requirement by mentioning a path inside its own source. SKILL.md is NOT
# excluded -- it is the main place resources are declared.
REFERENCE_SOURCE_EXCLUDE = {"scripts/run_evals.py"}

MAX_DESCRIPTION_CHARS = 500
MAX_SKILL_BODY_LINES = 300
MAX_SKILL_BODY_CHARS = 14000
# Per stage, counted separately: `resources` / `templates` / `profile_resources`
# are always loaded, while `optional` / `optional_profile_resources` are
# signal-gated. Either bucket growing past this means the Stage has stopped
# being a Stage and become a catch-all.
MAX_ALWAYS_LOADED_PER_STAGE = 12
MAX_CONDITIONAL_PER_STAGE = 12
MIN_TRIGGER_CASES_PER_CLASS = 8

RESULTS: list[tuple[str, str, bool, str]] = []


def record(check: str, level: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((check, level, ok, detail))


# --- helpers -----------------------------------------------------------------


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def text_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            out.append(path)
    return out


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def load_json(root: Path, relative: str):
    path = root / relative
    if not path.is_file():
        return None
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return None


def block_keys(text: str, top_key: str) -> list[str]:
    """Collect the 2-space-indented mapping keys under a top-level key."""
    keys: list[str] = []
    inside = False
    for line in text.splitlines():
        if re.match(rf"^{re.escape(top_key)}:\s*$", line):
            inside = True
            continue
        if inside:
            if line.strip() and not line.startswith(" "):
                break
            m = re.match(r"^  ([A-Za-z][\w.\-]*):", line)
            if m:
                keys.append(m.group(1))
    return keys


def stage_write_modes(text: str) -> dict[str, str]:
    """Map stage name -> write_mode from a router file."""
    out: dict[str, str] = {}
    current: str | None = None
    inside = False
    for line in text.splitlines():
        if re.match(r"^stages:\s*$", line):
            inside = True
            continue
        if inside:
            if line.strip() and not line.startswith(" "):
                break
            m = re.match(r"^  ([A-Za-z][\w.\-]*):\s*$", line)
            if m:
                current = m.group(1)
                continue
            m = re.match(r"^\s+write_mode:\s*(\S+)\s*$", line)
            if m and current:
                out[current] = m.group(1)
    return out


def stage_resource_paths(text: str) -> dict[str, dict[str, list[str]]]:
    """Map stage name -> {'always': [...], 'conditional': [...]}.

    Always-loaded means `resources` / `templates` / `profile_resources`.
    Signal-gated means `optional` / `optional_profile_resources`.
    """
    out: dict[str, dict[str, list[str]]] = {}
    current: str | None = None
    subkey: str | None = None
    inside = False
    for line in text.splitlines():
        if re.match(r"^stages:\s*$", line):
            inside = True
            continue
        if inside:
            if line.strip() and not line.startswith(" "):
                break
            m = re.match(r"^  ([A-Za-z][\w.\-]*):\s*$", line)
            if m:
                current = m.group(1)
                out[current] = {"always": [], "conditional": []}
                subkey = None
                continue
            m = re.match(r"^    ([a-z_]+):\s*(.*)$", line)
            if m and current:
                if m.group(1) == "stage":
                    # The `stage:` entry points at the stage file itself -- it
                    # is routed, not loaded as a resource. Counting it made
                    # every stage read one item heavier than the policy's
                    # definition of "always loaded" (resources / templates /
                    # profile_resources).
                    continue
                subkey = m.group(1)
                for found in PATH_REF_RE.finditer(m.group(2)):
                    out[current]["always"].append(found.group(1))
                continue
            if current and subkey:
                bucket = "conditional" if subkey.startswith("optional") else "always"
                stripped = line.strip()
                if (
                    stripped.startswith("- ")
                    and stripped[2:].strip()
                    and not PATH_REF_RE.search(stripped)
                ):
                    # A list entry that is not path-shaped skips the always /
                    # conditional count AND the reference resolver at once --
                    # a resource that is never loaded and never checked.
                    out[current].setdefault("malformed", []).append(stripped)
                for found in PATH_REF_RE.finditer(line):
                    out[current][bucket].append(found.group(1))
    return out


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    body = m.group(1)
    fields: dict[str, str] = {}
    for key in ("name", "description", "version"):
        km = re.search(rf"^{key}:\s*(.+?)(?=\n[A-Za-z_]+:|\Z)", body, re.S | re.M)
        if km:
            fields[key] = " ".join(km.group(1).split())
    return fields


def collect_references(root: Path) -> dict[str, set[str]]:
    """Map referenced path -> set of files that mention it."""
    refs: dict[str, set[str]] = {}
    for path in text_files(root):
        relative = rel(root, path)
        if relative in REFERENCE_SOURCE_EXCLUDE:
            continue
        for found in PATH_REF_RE.finditer(read_text(path)):
            refs.setdefault(found.group(1), set()).add(relative)
    return refs


def policy_allowlist(root: Path) -> set[str]:
    policy = root / "evals" / "evolution-policy.yaml"
    allowed: set[str] = set()
    if not policy.is_file():
        return allowed
    inside = False
    for line in read_text(policy).splitlines():
        if re.match(r"^orphan_allowlist:\s*$", line):
            inside = True
            continue
        if inside:
            if line.strip() and not line.startswith(" "):
                break
            m = re.match(r"^\s+-\s+(\S+)\s*$", line)
            if m:
                allowed.add(m.group(1))
    return allowed


def normalize_version(raw: str) -> str:
    m = re.match(r"(\d+)(?:\.(\d+))?", raw.strip())
    if not m:
        return raw.strip()
    return f"{m.group(1)}.{m.group(2) or '0'}"


def yaml_mapping_shape(text: str) -> dict[str, list[str] | None]:
    """Best-effort: top-level key -> list of 2-space-indented child keys.

    A value of None means the key holds a scalar or flow collection. This is a
    shallow reader, deliberately: it only needs to compare key names, and a real
    YAML parser would need a dependency this gate cannot assume.
    """
    shape: dict[str, list[str] | None] = {}
    current: str | None = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w.\-]*):\s*(.*)$", line)
        if m:
            current = m.group(1)
            shape[current] = [] if not m.group(2).strip() else None
            continue
        m = re.match(r"^  ([A-Za-z_][\w.\-]*):", line)
        if m and current and shape.get(current) is not None:
            shape[current].append(m.group(1))
    return shape


# --- checks ------------------------------------------------------------------


def check_package_hygiene(root: Path) -> None:
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        record("package-hygiene.skill-md-present", "error", False, "SKILL.md 缺失")
        return

    text = read_text(skill_md)
    fields = frontmatter(text)

    name = fields.get("name", "")
    record(
        "package-hygiene.name-matches-directory",
        "error",
        bool(name) and name == root.name,
        f"frontmatter name={name!r} vs 目录 {root.name!r}",
    )

    desc = fields.get("description", "")
    record(
        "package-hygiene.frontmatter-fields",
        "error",
        bool(name) and bool(desc) and len(desc) <= MAX_DESCRIPTION_CHARS,
        f"description 长度 {len(desc)} (上限 {MAX_DESCRIPTION_CHARS})",
    )

    pycache = [rel(root, p) for p in root.rglob("__pycache__")]
    record("package-hygiene.no-pycache", "error", not pycache, ", ".join(pycache))

    residue = [
        rel(root, p)
        for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in (".zip", ".skill")
    ]
    record("package-hygiene.no-release-residue", "error", not residue, ", ".join(residue))

    schemas = [
        rel(root, p) for p in (root / "schemas").glob("*.json") if "design-spec" in p.name
    ]
    record(
        "package-hygiene.single-canonical-schema",
        "error",
        len(schemas) == 1,
        f"design-spec schema 副本: {schemas}",
    )

    has_section = re.search(r"^##\s+版本\s*$", text, re.M) is not None
    has_date = re.search(r"更新:\s*\d{4}-\d{2}-\d{2}", text) is not None
    record(
        "package-hygiene.version-section",
        "error",
        has_section and has_date,
        ""
        if (has_section and has_date)
        else "SKILL.md 需要 `## 版本` 章节且含 `更新: YYYY-MM-DD`",
    )

    readme = root.parent / "README.md"
    if readme.is_file():
        listed = root.name in read_text(readme)
        record(
            "package-hygiene.readme-listing",
            "error",
            listed,
            f"上级 README.md 未登记 {root.name}" if not listed else "",
        )


def check_resource_routing(root: Path) -> None:
    refs = collect_references(root)

    missing = sorted(p for p in refs if not (root / p).exists())
    placeholders = sorted(p for p in missing if "{" in p)
    detail = ""
    if placeholders:
        detail = "未解析占位符: " + ", ".join(placeholders)
    elif missing:
        detail = "指向不存在的文件: " + ", ".join(missing)
    record("resource-routing.references-resolve", "error", not missing, detail)

    allowlist = policy_allowlist(root)
    orphans: list[str] = []
    for directory in RESOURCE_DIRS:
        base = root / directory
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            relative = rel(root, path)
            if relative in allowlist or relative in refs:
                continue
            orphans.append(relative)
    record(
        "resource-routing.no-orphan-resources",
        "error",
        not orphans,
        "无人引用的资产: " + ", ".join(orphans) if orphans else "",
    )

    missing_stage = [
        name for name in EXPECTED_STAGES if not (root / "stages" / f"{name}.md").is_file()
    ]
    record(
        "resource-routing.stage-coverage",
        "error",
        not missing_stage,
        "缺少 Stage 文件: " + ", ".join(missing_stage) if missing_stage else "",
    )

    resource_map = root / "routing" / "resource-map.yaml"
    if not resource_map.is_file():
        record("resource-routing.no-eager-full-load", "error", False, "resource-map.yaml 缺失")
        return
    per_stage = stage_resource_paths(read_text(resource_map))
    heavy: dict[str, str] = {}
    for name, buckets in per_stage.items():
        bad = buckets.get("malformed", [])
        if bad:
            heavy[name] = f"非路径形态条目 {bad}"
            continue
        always = len(buckets["always"])
        conditional = len(buckets["conditional"])
        if always > MAX_ALWAYS_LOADED_PER_STAGE:
            heavy[name] = f"always={always}"
        elif conditional > MAX_CONDITIONAL_PER_STAGE:
            heavy[name] = f"conditional={conditional}"
    record(
        "resource-routing.no-eager-full-load",
        "error",
        not heavy,
        f"单 Stage 加载过多资源 (上限 常驻 {MAX_ALWAYS_LOADED_PER_STAGE} / "
        f"条件 {MAX_CONDITIONAL_PER_STAGE}): {heavy}"
        if heavy
        else "",
    )


def check_stage_routing(root: Path) -> None:
    router = root / "routing" / "stage-router.yaml"
    scope = root / "routing" / "scope-router.yaml"
    resource_map = root / "routing" / "resource-map.yaml"
    if not (router.is_file() and scope.is_file() and resource_map.is_file()):
        record("stage-routing.stage-sets-consistent", "error", False, "路由文件缺失")
        return

    sets = {
        "stage-router.yaml": set(block_keys(read_text(router), "stages")),
        "scope-router.yaml": set(block_keys(read_text(scope), "stages")),
        "resource-map.yaml": set(block_keys(read_text(resource_map), "stages")),
        "stages/": {p.stem for p in (root / "stages").glob("*.md")},
    }
    unique = set().union(*sets.values())
    disagreements = {k: sorted(v) for k, v in sets.items() if v != unique}
    every = sorted(EXPECTED_STAGES) == sorted(unique)
    detail = ""
    if not every:
        detail = (
            f"缺少 {sorted(set(EXPECTED_STAGES) - unique)} "
            f"多余 {sorted(unique - set(EXPECTED_STAGES))}"
        )
    elif disagreements:
        detail = f"Stage 集合不一致: {disagreements}"
    record("stage-routing.stage-sets-consistent", "error", not detail, detail)


def check_info_flow(root: Path) -> None:
    """The information-flow segment set must agree everywhere it is defined."""

    def segments(text: str) -> set[str]:
        out: set[str] = set()
        # Arrow lists come in three shapes: one line per segment ("Context\n→
        # Signal"), a single line ("Context → Signal"), and trailing arrows
        # ("Context →\nSignal"). Join wrapped arrows in both directions first
        # so all parse to the same segment set.
        text = text.replace("\n→", " → ").replace("→\n", "→ ")
        for line in text.splitlines():
            if INFO_FLOW_ANCHOR in line and "→" in line:
                for part in line.split("→"):
                    part = part.strip().strip("`*").strip()
                    if part:
                        out.add(part)
        return out

    per_file: dict[str, set[str]] = {}
    missing: list[str] = []
    for relative in INFO_FLOW_FILES:
        path = root / relative
        if not path.is_file():
            missing.append(f"{relative}(缺失)")
            continue
        found = segments(read_text(path))
        if len(found) < 4:
            # A definition that parses to fewer than four segments is not the
            # six-segment flow -- partial parses (e.g. only lines reachable
            # from "Context") must fail, not pass as "some definition".
            missing.append(f"{relative}(信息流定义不完整: {sorted(found)})")
            continue
        per_file[relative] = found
    drift = {
        name: sorted(found)
        for name, found in per_file.items()
        if per_file and found != next(iter(per_file.values()))
    }
    ok = not missing and not drift
    detail = ""
    if missing:
        detail = "; ".join(missing)
    elif drift:
        detail = f"信息流环节集不一致: {drift}"
    record(
        "consistency.info-flow-alignment",
        "error",
        ok,
        detail,
    )


def check_numeric_projection(root: Path) -> None:
    """Numbers written in more than one file must agree everywhere they appear."""

    problems: list[str] = []

    # Award weights: the same Webby / Awwwards / FWA percentages must come out
    # of every file that states them. Collect every occurrence -- keeping only
    # the last per award would hide a file contradicting itself.
    weights: dict[str, list[str]] = {}
    for relative in AWARD_WEIGHT_FILES:
        path = root / relative
        if not path.is_file():
            problems.append(f"{relative}(缺失)")
            continue
        found = [
            f"{m.group(1)}={m.group(2)}"
            for m in re.finditer(r"(Webby|Awwwards|FWA)[^\n%]*?(\d+)\s*%", read_text(path))
        ]
        if not found:
            problems.append(f"{relative}(未找到奖项权重)")
            continue
        weights[relative] = found
    values = list(weights.values())
    if len(values) > 1 and any(v != values[0] for v in values[1:]):
        problems.append(f"奖项权重不一致: {weights}")

    # Hard gates: the ordered threshold sequence in SKILL.md must equal the
    # ordered fail sequence in the rubric.
    gates: dict[str, list[str]] = {}
    for relative, section_pattern, threshold_pattern in HARD_GATE_FILES:
        path = root / relative
        if not path.is_file():
            problems.append(f"{relative}(缺失)")
            continue
        m = re.search(section_pattern, read_text(path), re.S)
        if not m:
            problems.append(f"{relative}(未找到硬门槛章节)")
            continue
        extracted = re.findall(threshold_pattern, m.group(0))
        if not extracted:
            # An empty extraction means the wording moved away from the
            # pattern; comparing two empty sequences would pass vacuously.
            problems.append(f"{relative}(硬门槛章节未提取到阈值)")
            continue
        gates[relative] = extracted
    gate_values = list(gates.values())
    if len(gate_values) == 2 and gate_values[0] != gate_values[1]:
        problems.append(f"硬门槛阈值序列不一致: {gates}")

    # Token threshold: every file that phrases the extraction rule must carry
    # the「三次」bound; an unqualified「重复出现」reads as a different rule.
    for relative in TOKEN_THRESHOLD_FILES:
        path = root / relative
        if not path.is_file():
            problems.append(f"{relative}(缺失)")
            continue
        rules = [
            line.strip()
            for line in read_text(path).splitlines()
            if "重复" in line and "提取" in line and ("Token" in line or "token" in line)
        ]
        if not rules:
            # The threshold rule was deleted or rephrased away from the
            # scannable vocabulary -- absence must fail, not pass silently.
            problems.append(f"{relative}(未找到可校验的 Token 提取规则行)")
            continue
        vague = [rule for rule in rules if "三次" not in rule]
        if vague:
            problems.append(f"{relative} Token 提取阈值含糊: {vague}")

    record(
        "consistency.numeric-projection",
        "error",
        not problems,
        "数值双写不一致: " + "; ".join(problems) if problems else "",
    )


def check_registry_sync(root: Path) -> None:
    """The checks this script runs must be exactly the checks the policy lists."""
    self_name = "evals.check-registry-sync"
    policy = root / "evals" / "evolution-policy.yaml"
    if not policy.is_file():
        record(self_name, "error", False, "evolution-policy.yaml 缺失")
        return
    registered: set[str] = set()
    inside = False
    for line in read_text(policy).splitlines():
        if re.match(r"^  checks:\s*$", line):
            inside = True
            continue
        if inside:
            if line.strip() and not line.startswith(" "):
                break
            m = re.match(r"^    ([A-Za-z_][\w.\-]*):", line)
            if m:
                registered.add(m.group(1))
    recorded = {check for check, _, _, _ in RESULTS}
    extra = sorted(recorded - registered)
    missing = sorted(
        name
        for name in (registered - recorded) - {self_name}
        # Conditional checks legitimately absent when their environment is not
        # there; the policy says "独立安装时跳过" and the sync must respect it.
        if name not in CONDITIONAL_CHECKS or CONDITIONAL_CHECKS[name](root)
    )
    problems: list[str] = []
    # Self-exclusion from `missing` only holds while the policy actually
    # registers this check -- otherwise deleting its own entry would pass.
    if self_name not in registered:
        problems.append(f"{self_name} 自身未登记在 deterministic.checks")
    if extra:
        problems.append(f"脚本输出但 policy 未登记: {extra}")
    if missing:
        problems.append(f"policy 登记但脚本未输出: {missing}")
    record(self_name, "error", not problems, "；".join(problems))


def check_scope_contract_packs(root: Path) -> None:
    """context.packs in the example scope contract must point at real packs."""

    path = root / SCOPE_CONTRACT_TEMPLATE
    if not path.is_file():
        record(
            "resource-routing.scope-contract-packs-resolve",
            "error",
            False,
            f"{SCOPE_CONTRACT_TEMPLATE} 缺失",
        )
        return
    inside = False
    offenders: list[str] = []
    for line in read_text(path).splitlines():
        if re.match(r"^  packs:\s*$", line):
            inside = True
            continue
        if inside:
            if line.strip() and not line.lstrip().startswith("-"):
                inside = False
                continue
            m = re.match(r"^\s+-\s+(\S+)\s*$", line)
            if m:
                if not (root / "packs" / f"{m.group(1)}.md").is_file():
                    offenders.append(m.group(1))
    record(
        "resource-routing.scope-contract-packs-resolve",
        "error",
        not offenders,
        "context.packs 指向不存在的 pack: " + ", ".join(offenders) if offenders else "",
    )


def check_consistency(root: Path) -> None:
    """Cross-file invariants: one authority per fact, everything else a projection."""
    scope = root / "routing" / "scope-router.yaml"
    skill_md = root / "SKILL.md"

    # SKILL.md inlines the permission baseline as a safety projection; the
    # machine authority is scope-router.yaml. Drift between them means the model
    # reads one permission and the router enforces another.
    if scope.is_file() and skill_md.is_file():
        authority = stage_write_modes(read_text(scope))
        projection: dict[str, str] = {}
        for line in read_text(skill_md).splitlines():
            m = re.match(
                r"^\|\s*([a-z][a-z0-9-]*)\s*\|\s*([a-z][a-z0-9-]*)\s*\|\s*$", line
            )
            if m and m.group(1) in EXPECTED_STAGES:
                projection[m.group(1)] = m.group(2)
        drift = {
            name: (projection.get(name), authority.get(name))
            for name in sorted(set(projection) | set(authority))
            if projection.get(name) != authority.get(name)
        }
        record(
            "consistency.write-mode-projection",
            "error",
            not drift,
            f"SKILL.md 权限表与 scope-router.yaml 漂移 (SKILL.md, scope-router): {drift}"
            if drift
            else "",
        )

    problems: list[str] = []
    for relative in STRATEGY_UPPERCASE_SITES:
        path = root / relative
        if not path.is_file():
            problems.append(f"{relative}(缺失)")
            continue
        text = read_text(path)
        absent = [t for t in STRATEGY_TOKENS if t not in text]
        if absent:
            problems.append(f"{relative} 缺 {absent}")
    for relative in STRATEGY_KEY_SITES:
        path = root / relative
        if not path.is_file():
            problems.append(f"{relative}(缺失)")
            continue
        text = read_text(path)
        if path.suffix == ".json":
            absent = [t.lower() for t in STRATEGY_TOKENS if f'"{t.lower()}"' not in text]
        else:
            absent = [
                t.lower()
                for t in STRATEGY_TOKENS
                if not re.search(rf"^\s+{t.lower()}:", text, re.M)
            ]
        if absent:
            problems.append(f"{relative} 缺 {absent}")
    md_problems: list[str] = []
    for relative in STRATEGY_LOWERCASE_SITES:
        path = root / relative
        if not path.is_file():
            md_problems.append(f"{relative}(缺失)")
            continue
        text = read_text(path)
        absent = [t.lower() for t in STRATEGY_TOKENS if t.lower() not in text]
        if absent:
            md_problems.append(f"{relative} 缺 {absent}")
    record(
        "consistency.implementation-strategies",
        "error",
        not problems,
        "策略词表不一致（必须六项齐全）: " + "; ".join(problems) if problems else "",
    )
    # The human-readable mirror is a separate entry in the policy registry;
    # folding it into the record above desynchronized script and policy.
    record(
        "consistency.md-template-strategy-vocabulary",
        "error",
        not md_problems,
        "人读模板策略词表不全（必须六项小写齐全）: " + "; ".join(md_problems)
        if md_problems
        else "",
    )

    versions: dict[str, str] = {}
    unreadable: list[str] = []
    for relative, pattern, label in VERSION_PATTERNS:
        path = root / relative
        if not path.is_file():
            unreadable.append(f"{label}:{relative}(缺失)")
            continue
        m = re.search(pattern, read_text(path), re.M)
        if not m:
            unreadable.append(f"{label}:{relative}(未找到版本号)")
            continue
        versions[f"{label}:{relative}"] = normalize_version(m.group(1))
    distinct = sorted(set(versions.values()))
    ok = not unreadable and len(distinct) == 1
    detail = ""
    if unreadable:
        detail = "; ".join(unreadable)
    elif not ok:
        detail = f"版本号不一致: {versions}"
    record("consistency.version-sync", "error", ok, detail)


def check_schemas(root: Path) -> None:
    spec = load_json(root, "schemas/design-spec.json")
    page_dsl = load_json(root, "schemas/page-dsl.schema.json")
    if spec is None or page_dsl is None:
        record("schemas.page-dsl-alignment", "error", False, "Schema 缺失或不是合法 JSON")
        return

    screens = spec.get("properties", {}).get("screens", {}).get("items", {})
    spec_required = set(screens.get("required", []))
    dsl_required = set(page_dsl.get("required", []))
    record(
        "schemas.page-dsl-alignment",
        "error",
        spec_required == dsl_required,
        f"page-dsl required 与 screens[] required 不一致: "
        f"仅 page-dsl {sorted(dsl_required - spec_required)} / "
        f"仅 screens[] {sorted(spec_required - dsl_required)}"
        if spec_required != dsl_required
        else "",
    )

    template = root / "templates" / "design-specification.yaml"
    if not template.is_file():
        record("schemas.template-matches-schema", "error", False, "骨架模板缺失")
        return
    shape = yaml_mapping_shape(read_text(template))
    props = spec.get("properties", {})
    problems: list[str] = []

    absent_required = sorted(set(spec.get("required", [])) - set(shape))
    if absent_required:
        problems.append(f"骨架缺少 required 字段 {absent_required}")

    unknown_top = sorted(k for k in shape if k not in props)
    if unknown_top:
        problems.append(f"骨架含 schema 未声明的顶层字段 {unknown_top}")

    for key, children in shape.items():
        if not children or key not in props:
            continue
        allowed = props[key].get("properties", {})
        unknown = sorted(c for c in children if c not in allowed)
        if unknown:
            problems.append(f"{key} 下有 schema 未声明的字段 {unknown}")

    record(
        "schemas.template-matches-schema",
        "error",
        not problems,
        "骨架与 Schema 不一致: " + "; ".join(problems) if problems else "",
    )


def check_evals(root: Path) -> None:
    data = load_json(root, "evals/trigger-evals.json")
    if data is None:
        record("evals.trigger-set", "error", False, "evals/trigger-evals.json 缺失或非法 JSON")
        return
    cases = data.get("evals") if isinstance(data, dict) else data
    if not isinstance(cases, list):
        record("evals.trigger-set", "error", False, "trigger-evals.json 结构不正确")
        return
    positives = [c for c in cases if isinstance(c, dict) and c.get("should_trigger") is True]
    negatives = [c for c in cases if isinstance(c, dict) and c.get("should_trigger") is False]
    malformed = [
        c for c in cases if not isinstance(c, dict) or "query" not in c or "should_trigger" not in c
    ]
    ok = (
        not malformed
        and len(positives) >= MIN_TRIGGER_CASES_PER_CLASS
        and len(negatives) >= MIN_TRIGGER_CASES_PER_CLASS
    )
    record(
        "evals.trigger-set",
        "error",
        ok,
        f"触发回归集需 ≥{MIN_TRIGGER_CASES_PER_CLASS} 正例与 "
        f"≥{MIN_TRIGGER_CASES_PER_CLASS} 负例且字段完整；"
        f"实际 正 {len(positives)} / 负 {len(negatives)} / 畸形 {len(malformed)}"
        if not ok
        else "",
    )


def check_scope_safety(root: Path) -> None:
    scope = root / "routing" / "scope-router.yaml"
    if not scope.is_file():
        record("scope-safety.forbidden-declared", "error", False, "scope-router.yaml 缺失")
        return
    # A stage that omits `default_forbidden` entirely is as dangerous as one
    # that declares it empty -- the previous check only caught `[]`, so
    # dropping the whole key passed as if it were safe.
    offenders: list[str] = []
    current: str | None = None
    declared = False
    inside = False
    for line in read_text(scope).splitlines():
        if re.match(r"^stages:\s*$", line):
            inside = True
            continue
        if inside:
            if line.strip() and not line.startswith(" "):
                break
            m = re.match(r"^  ([A-Za-z][\w.\-]*):\s*$", line)
            if m:
                if current is not None and not declared:
                    offenders.append(current)
                current = m.group(1)
                declared = False
                continue
            if current and re.match(r"^\s+default_forbidden:", line):
                declared = True
                # Strip inline comments before judging emptiness: `[]  # none`
                # or `null` is an empty declaration wearing documentation.
                value = line.split(":", 1)[1].split("#", 1)[0].strip()
                if value in ("", "null", "~", "{}") or value.strip("[] \t") == "":
                    offenders.append(current)
    if current is not None and not declared:
        offenders.append(current)
    record(
        "scope-safety.forbidden-declared",
        "error",
        not offenders,
        "default_forbidden 缺失或为空的 Stage: " + ", ".join(offenders) if offenders else "",
    )


def check_profile_selection(root: Path) -> None:
    profiles = sorted((root / "profiles").glob("*/profile.yaml"))
    if not profiles:
        record("profile-selection.activation-guard", "error", False, "未找到 profile.yaml")
        return
    problems: list[str] = []
    for path in profiles:
        text = read_text(path)
        has_required = re.search(r"^\s+required_any:", text, re.M) is not None
        min_match = re.search(r"^\s+min_supporting_matches:\s*(\d+)\s*$", text, re.M)
        guard_ok = min_match is not None and int(min_match.group(1)) >= 2
        if not (has_required and guard_ok):
            problems.append(
                f"{rel(root, path)} (required_any={has_required}, "
                f"min_supporting_matches={min_match.group(1) if min_match else 'None'})"
            )
    record(
        "profile-selection.activation-guard",
        "error",
        not problems,
        "激活守卫不足（需 required_any 且 min_supporting_matches>=2）: "
        + ", ".join(problems)
        if problems
        else "",
    )


def check_context_budget(root: Path) -> None:
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        record("context-budget.core-lean", "error", False, "SKILL.md 缺失")
        return
    text = read_text(skill_md)
    lines = len(text.splitlines())
    chars = len(text)
    ok = lines <= MAX_SKILL_BODY_LINES and chars <= MAX_SKILL_BODY_CHARS
    record(
        "context-budget.core-lean",
        "error",
        ok,
        f"SKILL.md {lines} 行 / {chars} 字符 "
        f"(上限 {MAX_SKILL_BODY_LINES} 行 / {MAX_SKILL_BODY_CHARS} 字符)",
    )


# --- entry point -------------------------------------------------------------


def main(argv: list[str]) -> int:
    root = (
        Path(argv[1]).resolve()
        if len(argv) > 1
        else Path(__file__).resolve().parent.parent
    )
    if not (root / "SKILL.md").is_file():
        print(f"error: {root} 不是一个 skill 目录（缺少 SKILL.md）")
        return 1

    print(f"skill: {root}")
    print()

    check_package_hygiene(root)
    check_resource_routing(root)
    check_stage_routing(root)
    check_consistency(root)
    check_info_flow(root)
    check_numeric_projection(root)
    check_scope_contract_packs(root)
    check_schemas(root)
    check_evals(root)
    check_scope_safety(root)
    check_profile_selection(root)
    check_context_budget(root)
    check_registry_sync(root)

    failures = 0
    width = max(len(c) for c, _, _, _ in RESULTS)
    for check, level, ok, detail in RESULTS:
        mark = "PASS" if ok else "FAIL"
        if not ok:
            failures += 1
        line = f"  [{mark}] {check.ljust(width)}"
        if detail:
            line += f"  {detail}"
        print(line)

    print()
    if failures:
        print(f"deterministic evals: {failures} 项失败 / 共 {len(RESULTS)} 项")
        print("按 evals/evolution-policy.yaml 的发布门禁，不得发布。")
        return 1
    print(f"deterministic evals: 全部通过 / 共 {len(RESULTS)} 项")
    print("仍需完成 qualitative evals（见 evals/evolution-policy.yaml）才能发布。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
