"""The extraction schema, loaded from config/extraction.yaml.

Two tables, following docs/data_dictionary/extraction_schema.md:
  studies   — one row per study_id, the unit of analysis (D004)
  estimates — one row per reported effect estimate; all are preserved (provenance rule 8)

A field whose `status` is `unresolved` depends on a protocol decision that has not been made.
Extraction can still record what a study reported, but the validator says so rather than treating
any value as protocol-conformant.
"""
from __future__ import annotations

from dataclasses import dataclass, field as dc_field

import yaml

from scripts.common.config import ROOT, PipelineError

EXTRACTION_CONFIG = ROOT / "config" / "extraction.yaml"
STUDIES = "studies"
ESTIMATES = "estimates"
TABLES = (STUDIES, ESTIMATES)
# Loaded separately by load_rob_schema(); not an extraction table, because no instrument is chosen.
RISK_OF_BIAS = "risk_of_bias"
UNRESOLVED = "unresolved"
PROVISIONAL = "provisional"


@dataclass(frozen=True)
class Field:
    name: str
    type: str
    description: str = ""
    values: tuple[str, ...] = ()
    status: str = ""
    depends_on: str = ""

    @property
    def is_unresolved(self) -> bool:
        return self.status == UNRESOLVED


@dataclass(frozen=True)
class Table:
    name: str
    fields: tuple[Field, ...]
    required: tuple[str, ...]

    @property
    def columns(self) -> tuple[str, ...]:
        return tuple(f.name for f in self.fields)

    def field(self, name: str) -> Field | None:
        return next((f for f in self.fields if f.name == name), None)


@dataclass(frozen=True)
class Schema:
    tables: dict[str, Table]
    missing_codes: tuple[str, ...]
    thresholds: dict[str, float] = dc_field(default_factory=dict)

    def table(self, name: str) -> Table:
        if name not in self.tables:
            raise PipelineError(f"unknown table {name!r}; expected one of {TABLES}")
        return self.tables[name]

    @property
    def unresolved_fields(self) -> tuple[Field, ...]:
        return tuple(f for t in self.tables.values() for f in t.fields if f.is_unresolved)


def load_schema() -> Schema:
    with open(EXTRACTION_CONFIG, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    tables = {}
    for name in TABLES:
        if name not in data:
            raise PipelineError(f"{EXTRACTION_CONFIG.name}: missing table {name!r}")
        spec = data[name]
        fields = tuple(
            Field(name=fname, type=f.get("type", "text"), description=f.get("description", ""),
                  values=tuple(f.get("values", ())), status=f.get("status", ""),
                  depends_on=f.get("depends_on", ""))
            for fname, f in spec["fields"].items()
        )
        required = tuple(spec.get("required", ()))
        unknown = [r for r in required if r not in {f.name for f in fields}]
        if unknown:
            raise PipelineError(f"{name}: required field(s) not defined: {unknown}")
        for f in fields:
            if f.type == "enum" and not f.values:
                raise PipelineError(f"{name}.{f.name}: enum field with no values")
            if f.is_unresolved and not f.depends_on:
                raise PipelineError(
                    f"{name}.{f.name}: an unresolved field must name the decision it waits on"
                )
        tables[name] = Table(name=name, fields=fields, required=required)

    return Schema(tables=tables,
                  missing_codes=tuple(data.get("missing_codes", ())),
                  thresholds=dict(data.get("thresholds", {})))


def load_rob_schema() -> Table:
    """The provisional risk-of-bias worksheet schema, pending P023.

    Deliberately NOT part of `load_schema()`. The appraisal instrument has not been chosen, so
    these columns are structural only and must not be mistaken for an adopted data model: loading
    them separately is what keeps `Schema.tables` meaning "the extraction tables". The instrument's
    domain names and judgement categories are absent by design and are never invented here.
    """
    with open(EXTRACTION_CONFIG, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if RISK_OF_BIAS not in data:
        raise PipelineError(f"{EXTRACTION_CONFIG.name}: missing table {RISK_OF_BIAS!r}")
    spec = data[RISK_OF_BIAS]
    if spec.get("status") != PROVISIONAL:
        raise PipelineError(
            f"{RISK_OF_BIAS}: must be marked `status: provisional` until P023 is settled, "
            f"found {spec.get('status')!r}"
        )
    if spec.get("depends_on") != "P023":
        raise PipelineError(f"{RISK_OF_BIAS}: must record `depends_on: P023`")
    fields = tuple(
        Field(name=fname, type=f.get("type", "text"), description=f.get("description", ""),
              values=tuple(f.get("values", ())), status=f.get("status", ""),
              depends_on=f.get("depends_on", ""))
        for fname, f in spec["fields"].items()
    )
    for f in fields:
        if f.values:
            raise PipelineError(
                f"{RISK_OF_BIAS}.{f.name}: no field may carry a values list, because that would "
                "assert the categories of an instrument that has not been chosen (P023)"
            )
    return Table(name=RISK_OF_BIAS, fields=fields, required=tuple(spec.get("required", ())))
