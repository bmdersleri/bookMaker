# Chapter Validator Contract

## Key Modules

```text
src/bookmaker/chapter/parser.py
src/bookmaker/chapter/validator.py
src/bookmaker/chapter/validation_modes.py
src/bookmaker/chapter/book_validator.py
src/bookmaker/chapter/scoring.py
tests/test_chapter_validation_modes.py
tests/test_chapter_validator_profile_modes.py
tests/unit/test_validator.py
```

## Metadata Blocks

Parser-recognized meta blocks use HTML comments:

````markdown
<!-- CODE_META
code_id: example_001
file: lib/main.dart
validation_mode: runnable
language: dart
test: flutter_test
-->
```dart
void main() {}
```
````

Unit tests may instantiate `MetaBlock` directly when focused on validator internals.

## Test Mode Sets

Java execution modes:

```text
compile
run
run_assert
compile_run
compile_run_assert
```

Flutter/Dart execution modes:

```text
dart_analyze
dart_test
dart_format_check
flutter_analyze
flutter_test
widget_test
integration_test
```

Non-execution modes:

```text
screenshot_only
review_only
skip
none
```

## Profile Resolution

Use `resolve_validation_profile_from_manifest(manifest)` for manifest-derived profile. It should return canonical `java`, `flutter`, `generic`, or `None` for unknown manifest values when legacy fallback must remain possible.

`validate(..., profile=None)` means no explicit profile was supplied; validator may infer from path as a transition fallback. Passing `profile="java"` or `profile="flutter"` must override path inference.

## Issue Category Stability

Keep existing category strings stable unless the user requests a breaking validator policy change. Important profile category:

```text
code.test_not_allowed_for_profile
```
