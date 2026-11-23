# Schemas

One JSON Schema per record type. Enumerations live only in `enums.json`; a schema refers to one with
`{"$enum": "<name>"}` and `pipeline/checks.py` expands that marker before validating.
Data files in `data/register/` are arrays of these records.
