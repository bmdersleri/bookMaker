#!/usr/bin/env python3
"""Root .md dosyalarini kucuk harfe cevir (Windows case-insensitive FS fix)"""
import pathlib, os, tempfile

root = pathlib.Path(r"D:\bookMaker_Deepseek")

rename_map = {
    "MASTER_PLAN.md": "master_plan.md",
    "SESSION.md": "session.md", 
    "RESUME.md": "resume.md",
    "TODO.md": "todo.md",
    "FAULT.md": "fault.md",
    "WORKSPACE.md": "workspace.md",
    "CHAPTER_SPEC.md": "chapter_spec.md",
    "CODING_PLAN.md": "coding_plan.md",
    "CHAPTER_AUTHORING_WORKFLOW.md": "chapter_authoring_workflow.md",
    "PRODUCTION_FAULT.md": "production_fault.md",
    "KULLANIM_KILAVUZU.md": "kullanim_kilavuzu.md",
}

print("=== Cross-referanslar guncelleniyor ===")
# Once cross-referanslari guncelle
for f in root.glob("*.md"):
    if f.name in rename_map:
        text = f.read_text("utf-8")
        original = text
        for old_name, new_name in rename_map.items():
            text = text.replace(f"`{old_name}`", f"`{new_name}`")
        if text != original:
            f.write_text(text, "utf-8")
            print(f"  [OK] {f.name}")

print("\n=== Dosyalar yeniden adlandiriliyor ===")
# Windows case-insensitive FS: MASTER_PLAN.md -> master_plan.md
# Iki asamali: once temp isme, sonra hedef isme
for old_name, new_name in rename_map.items():
    old_path = root / old_name
    new_path = root / new_name
    if not old_path.exists():
        tmp_name = f"_{old_name}.tmp"
        tmp_path = root / tmp_name
        # Belki eski temp dosyasi kalmistir
        if tmp_path.exists():
            tmp_path.unlink()
        old_path.rename(tmp_path)
        print(f"  [1] {old_name} -> {tmp_name}")
        tmp_path.rename(new_path)
        print(f"  [2] {tmp_name} -> {new_name}")
    else:
        print(f"  [-] {old_name} zaten yok (belki onceki denemede basarili oldu)")

# Dogrula
print("\n=== Dogrulama ===")
for new_name in rename_map.values():
    if (root / new_name).exists():
        print(f"  [OK] {new_name}")
    else:
        print(f"  [!!] {new_name} BULUNAMADI!")

# Eski uppercase isimler kaldi mi?
for old_name in rename_map:
    if (root / old_name).exists():
        print(f"  [!!] ESKI DOSYA KALDI: {old_name}")

print("\n=== Tamam ===")
