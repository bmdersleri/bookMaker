"""
bookmaker.production.screenshot_strategies.flutter_utils
=========================================================
Flutter/Dart kod analizi ve test/web şablon üretimi için ortak yardımcılar.
FlutterGoldenStrategy ve FlutterWebStrategy tarafından paylaşılır.

NOT: Bu modül src/bookmaker/code/adapters/flutter.py'den bağımsızdır.
FlutterCodeAdapter dart analyze çalıştırır; bu modül screenshot üretir.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Flutter SDK kontrolü
# ---------------------------------------------------------------------------

def flutter_cmd() -> str:
    """Platform'a göre doğru flutter komutunu döner (Windows: flutter.bat)."""
    return "flutter.bat" if sys.platform == "win32" else "flutter"


def check_flutter() -> str | None:
    """
    Flutter SDK'nın PATH'de olup olmadığını kontrol eder.
    Kuruluysa versiyon stringini, değilse None döner.
    """
    cmd = flutter_cmd()
    if shutil.which(cmd) is None:
        return None
    try:
        result = subprocess.run(
            [cmd, "--version"],
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode == 0:
            # İlk satır: "Flutter 3.x.y channel stable ..."
            first_line = result.stdout.strip().splitlines()[0]
            return first_line[:80]
    except Exception:
        pass
    return None


def find_runner_dir(start: Path | None = None) -> Path:
    """
    tools/flutter_screenshot_runner/ klasörünü proje kökünde arar.
    Bulamazsa FileNotFoundError fırlatır.
    """
    search = start or Path.cwd()
    for candidate in [search, *search.parents]:
        runner = candidate / "tools" / "flutter_screenshot_runner"
        if (runner / "pubspec.yaml").exists():
            return runner
    raise FileNotFoundError(
        "tools/flutter_screenshot_runner/ bulunamadı.\n"
        "Kurulum: flutter pub get komutunu tools/flutter_screenshot_runner/ içinde çalıştırın."
    )


# ---------------------------------------------------------------------------
# Dart kod analizi
# ---------------------------------------------------------------------------

def is_full_app(code: str) -> bool:
    """void main() + runApp() içeren tam bir Flutter uygulaması mı?"""
    return "void main()" in code and "runApp(" in code


def is_widget_class(code: str) -> bool:
    """StatelessWidget veya StatefulWidget extend eden sınıf tanımı mı?"""
    return bool(re.search(
        r"class\s+\w+\s+extends\s+(Stateless|Stateful)Widget",
        code,
    ))


def is_widget_expression(code: str) -> bool:
    """Tek widget ifadesi mi? (class veya main() tanımı yok)"""
    return not is_full_app(code) and not is_widget_class(code)


def extract_imports(code: str) -> list[str]:
    """Koddan import satırlarını ayıklar."""
    return re.findall(r"^import\s+['\"].*?['\"];", code, re.MULTILINE)


def strip_imports(code: str) -> str:
    """Import satırlarını koddan kaldırır."""
    return re.sub(
        r"^import\s+['\"].*?['\"];\n?", "", code, flags=re.MULTILINE
    ).strip()


def extract_class_name(code: str) -> str | None:
    """Widget class adını çıkarır. Bulamazsa None döner."""
    m = re.search(
        r"class\s+([A-Z]\w+)\s+extends\s+(Stateless|Stateful)Widget",
        code,
    )
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Golden test şablonu
# ---------------------------------------------------------------------------

_GOLDEN_TEST_TEMPLATE = """\
// bookMaker tarafından otomatik üretildi — düzenlemeyin
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
{extra_imports}

{user_code}

void main() {{
  testWidgets('bookmaker_screenshot', (WidgetTester tester) async {{
    await tester.pumpWidget(
{widget_tree}
    );
    await tester.pumpAndSettle();
    await expectLater(
      find.byType(MaterialApp),
      matchesGoldenFile('goldens/screenshot.png'),
    );
  }});
}}
"""


def build_golden_test(code: str) -> str:
    """
    Dart widget kodundan golden test dosyası üretir.

    3 giriş formatını destekler:
      - Widget ifadesi : ElevatedButton(onPressed: () {}, child: Text('X'))
      - Widget sınıfı  : class MyWidget extends StatelessWidget { ... }
      - Tam uygulama  : void main() { runApp(...); }
    """
    imports = extract_imports(code)
    body = strip_imports(code)
    extra_imports = "\n".join(imports) if imports else ""

    if is_full_app(code):
        # Tam uygulama — runApp() argümanını widget tree olarak al
        m = re.search(r"runApp\((.+?)\);", body, re.DOTALL)
        app_widget = m.group(1).strip() if m else "const MaterialApp()"
        user_code = ""
        widget_tree = f"      {app_widget}"

    elif is_widget_class(code):
        class_name = extract_class_name(body) or "MyWidget"
        user_code = body
        widget_tree = (
            f"      MaterialApp(\n"
            f"        debugShowCheckedModeBanner: false,\n"
            f"        home: Scaffold(\n"
            f"          body: Center(child: const {class_name}()),\n"
            f"        ),\n"
            f"      )"
        )

    else:
        # Widget ifadesi — direkt Center içine al
        user_code = ""
        widget_tree = (
            f"      MaterialApp(\n"
            f"        debugShowCheckedModeBanner: false,\n"
            f"        home: Scaffold(\n"
            f"          body: Center(\n"
            f"            child: {body},\n"
            f"          ),\n"
            f"        ),\n"
            f"      )"
        )

    return _GOLDEN_TEST_TEMPLATE.format(
        extra_imports=extra_imports,
        user_code=user_code,
        widget_tree=widget_tree,
    )


# ---------------------------------------------------------------------------
# Web main.dart şablonu
# ---------------------------------------------------------------------------

_WEB_MAIN_TEMPLATE = """\
// bookMaker tarafından otomatik üretildi — düzenlemeyin
import 'package:flutter/material.dart';
{extra_imports}

{user_code}

void main() {{
  runApp(const _BookMakerPreviewApp());
}}

class _BookMakerPreviewApp extends StatelessWidget {{
  const _BookMakerPreviewApp();

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: {home_widget},
    );
  }}
}}
"""


def build_web_main(code: str) -> str:
    """
    Dart widget/uygulama kodundan Flutter web main.dart üretir.
    """
    imports = extract_imports(code)
    body = strip_imports(code)
    extra_imports = "\n".join(imports) if imports else ""

    if is_full_app(code):
        # Tam uygulama — olduğu gibi kullan
        return "// bookMaker tarafından otomatik üretildi\n" + code

    elif is_widget_class(code):
        class_name = extract_class_name(body) or "MyWidget"
        return _WEB_MAIN_TEMPLATE.format(
            extra_imports=extra_imports,
            user_code=body,
            home_widget=f"const {class_name}()",
        )

    else:
        # Widget ifadesi
        return _WEB_MAIN_TEMPLATE.format(
            extra_imports=extra_imports,
            user_code="",
            home_widget=(
                f"Scaffold(\n"
                f"        body: Center(\n"
                f"          child: {body},\n"
                f"        ),\n"
                f"      )"
            ),
        )
