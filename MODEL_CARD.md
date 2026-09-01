# Research Model Card

## Intended use
Engineering demonstration of a DICOM-to-segmentation pipeline using synthetic or properly de-identified research data.

## Excluded use
Diagnosis, treatment, prescribing, triage, prognosis, patient communication, or autonomous clinical decision-making.

## Model
Default mode is a deterministic intensity threshold, not a disease model.

## Limitations
The demo output has no clinical meaning. Performance is not established on clinical populations, scanners, modalities, or acquisition protocols.

## Human oversight
Every result starts as `not_reviewed` and requires an identified qualified reviewer.
