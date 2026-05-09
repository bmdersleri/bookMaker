"""API yanit duzeltmelerini test eder.

Calistirma:
    python tools/test_api_response_fixes.py
"""

import json
import sys
import tempfile
from pathlib import Path

# Proje yolunu ekle
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


def test_openai_finish_reason():
    """Test: chat() yaniti finish_reason iceriyor mu?"""
    print("\n=== TEST 1: chat() finish_reason kontrolu ===")
    from bookmaker.llm.openai import OpenAICompatibleClient
    import inspect

    client = OpenAICompatibleClient(api_key="test-key", model="deepseek-chat", timeout=10)
    source = inspect.getsource(client.chat)

    checks = {
        "finish_reason cikariliyor": "finish_reason" in source,
        "max_tokens varsayilan 8192": "8192" in source and "max_tokens" in source,
        "_save_api_response cagriliyor": "_save_api_response" in source,
        "Truncation uyarisi var": "TRUNCATION" in source,
    }

    all_pass = True
    for check, result in checks.items():
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print(f"  [{status}] {check}")
    return all_pass


def test_generate_text_truncation():
    """Test: generate_text() truncation uyarisi iceriyor mu?"""
    print("\n=== TEST 2: generate_text() truncation uyarisi ===")
    from bookmaker.llm.openai import OpenAICompatibleClient
    import inspect

    client = OpenAICompatibleClient(api_key="test-key", timeout=10)
    source = inspect.getsource(client.generate_text)

    checks = {
        "finish_reason kontrolu var": "finish_reason" in source,
        "Truncation uyarisi var": "TRUNCATION" in source,
        "content uzunlugu loglaniyor": "len(result.get" in source,
    }

    all_pass = True
    for check, result in checks.items():
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print(f"  [{status}] {check}")
    return all_pass


def test_api_log_dir():
    """Test: api_log_dir parametresi var mi?"""
    print("\n=== TEST 3: api_log_dir parametresi ===")
    from bookmaker.llm.openai import OpenAICompatibleClient
    import inspect

    sig = inspect.signature(OpenAICompatibleClient.__init__)
    params = list(sig.parameters.keys())

    checks = {
        "api_log_dir parametresi var": "api_log_dir" in params,
    }

    all_pass = True
    for check, result in checks.items():
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print(f"  [{status}] {check}")

    # _save_api_response metodu var mi?
    if hasattr(OpenAICompatibleClient, "_save_api_response"):
        print("  [PASS] _save_api_response metodu var")
    else:
        print("  [FAIL] _save_api_response metodu YOK!")
        all_pass = False

    # _api_call_counter var mi?
    client = OpenAICompatibleClient(api_key="test-key", timeout=10, api_log_dir="")
    if hasattr(client, "_api_call_counter"):
        print("  [PASS] _api_call_counter var")
    else:
        print("  [FAIL] _api_call_counter YOK!")
        all_pass = False

    return all_pass


def test_save_api_response_with_dir():
    """Test: _save_api_response dosya olusturuyor mu?"""
    print("\n=== TEST 4: _save_api_response dosya olusturma ===")
    from bookmaker.llm.openai import OpenAICompatibleClient

    with tempfile.TemporaryDirectory() as tmpdir:
        client = OpenAICompatibleClient(
            api_key="test-key", timeout=10, api_log_dir=tmpdir,
        )

        payload = {
            "model": "deepseek-chat", "max_tokens": 8192,
            "temperature": 0.7,
            "messages": [
                {"role": "system", "content": "Test system prompt"},
                {"role": "user", "content": "Test user prompt"},
            ],
        }
        response = {
            "content": "Test yanit", "model": "deepseek-chat",
            "usage": {"completion_tokens": 5, "prompt_tokens": 10},
            "finish_reason": "stop", "retries": 0,
        }
        client._save_api_response("test", payload, response, None, 0)

        log_dir = Path(tmpdir) / "api_logs"
        json_files = list(log_dir.glob("*.json"))

        if not json_files:
            print("  [FAIL] Log dosyasi olusturulmadi!")
            return False

        print(f"  [PASS] {len(json_files)} log dosyasi olusturuldu")
        with open(json_files[0], "r", encoding="utf-8") as f:
            log = json.load(f)

        checks = {
            "call alani var": log.get("call") == "test",
            "model alani var": log.get("model") == "deepseek-chat",
            "response alani var": log.get("response") is not None,
            "finish_reason kaydedildi": log["response"].get("finish_reason") == "stop",
            "system_prompt_preview var": "Test system prompt" in log["payload"]["system_prompt_preview"],
        }

        all_pass = True
        for check, result in checks.items():
            status = "PASS" if result else "FAIL"
            if not result:
                all_pass = False
            print(f"  [{status}] {check}")
        return all_pass


def test_validate_spec_returns_dict():
    """Test: validate_spec artik dict donduruyor mu?"""
    print("\n=== TEST 5: validate_spec() dict donduruyor ===")
    from bookmaker.generation.spec import validate_spec
    import inspect

    sig = inspect.signature(validate_spec)
    return_annotation = sig.return_annotation

    if hasattr(return_annotation, "__origin__"):
        is_dict = return_annotation.__origin__ is dict
    elif isinstance(return_annotation, str):
        is_dict = "dict" in return_annotation
    else:
        is_dict = return_annotation is dict

    source = inspect.getsource(validate_spec)
    returns_dict = "return {" in source.replace(" ", "") or "return{" in source.replace(" ", "")

    # Duz metin olarak source'ta "notes" ve "response" kelimeleri var mi?
    # (tek/cift tirnak farki olmadan kontrol et)
    has_notes = '"notes"' in source or "'notes'" in source
    has_response = '"response"' in source or "'response'" in source

    checks = {
        "Return type dict": is_dict,
        "return dict literal var": returns_dict,
        "'notes' key exists": has_notes,
        "'response' key exists": has_response,
    }

    all_pass = True
    for check, result in checks.items():
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print(f"  [{status}] {check}")
    return all_pass


def test_pipeline_enrichment_save():
    """Test: Enrichment yanitlari kaydediliyor mu?"""
    print("\n=== TEST 6: Enrichment yanit kaydi ===")
    import inspect
    from bookmaker.generation.pipeline import ChapterGenerator

    source = inspect.getsource(ChapterGenerator.generate_chapter_with_spec)

    checks = {
        "step3_enrich_{k}.md kaydediliyor": "step3_enrich" in source,
        "prompt3_enrich_{k}.txt hala kaydediliyor": "prompt3_enrich" in source,
        "v degeri (gercek yanit) kaydediliyor": "step3_enrich_{k}.md\", v" in source or "step3_enrich_{k}.md\", v" in source.replace(" ", ""),
    }

    all_pass = True
    for check, result in checks.items():
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print(f"  [{status}] {check}")
    return all_pass


def test_save_gen_error_handling():
    """Test: _save_gen hata durumunda uyari veriyor mu?"""
    print("\n=== TEST 7: _save_gen hata yonetimi ===")
    import inspect
    from bookmaker.generation.pipeline import ChapterGenerator

    methods = []
    if hasattr(ChapterGenerator, "_save_gen"):
        methods.append(("_save_gen", inspect.getsource(ChapterGenerator._save_gen)))
    if hasattr(ChapterGenerator, "_save"):
        methods.append(("_save", inspect.getsource(ChapterGenerator._save)))

    if not methods:
        print("  [FAIL] Ne _save_gen ne _save metodu bulundu!")
        return False

    all_pass = True
    for method_name, source in methods:
        has_except = "except Exception" in source
        has_print = "[KAYIT" in source

        print(f"  [{'PASS' if has_except else 'FAIL'}] {method_name}: except Exception var")
        print(f"  [{'PASS' if has_print else 'FAIL'}] {method_name}: print uyarisi var")

        if not has_except or not has_print:
            all_pass = False

    return all_pass


def test_chapter_generator_api_log_dir():
    """Test: ChapterGenerator client'a api_log_dir geciyor mu?"""
    print("\n=== TEST 8: ChapterGenerator api_log_dir ===")
    import inspect
    from bookmaker.generation.pipeline import ChapterGenerator

    source = inspect.getsource(ChapterGenerator._init_clients)

    checks = {
        "api_log_dir geciliyor": "api_log_dir" in source,
        "build dizini kullaniliyor": "build" in source,
    }

    all_pass = True
    for check, result in checks.items():
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print(f"  [{status}] {check}")
    return all_pass


def main():
    print("=" * 60)
    print("API YANIT DUZELTMELERI TESTLERI")
    print("=" * 60)

    results = {
        "chat() finish_reason": test_openai_finish_reason(),
        "generate_text() uyari": test_generate_text_truncation(),
        "api_log_dir parametresi": test_api_log_dir(),
        "_save_api_response calisiyor": test_save_api_response_with_dir(),
        "validate_spec dict donduruyor": test_validate_spec_returns_dict(),
        "Enrichment yanit kaydi": test_pipeline_enrichment_save(),
        "_save_gen hata yonetimi": test_save_gen_error_handling(),
        "ChapterGenerator api_log_dir": test_chapter_generator_api_log_dir(),
    }

    print("\n" + "=" * 60)
    print("SONUCLAR")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {test_name}")

    print(f"\n  Toplam: {passed}/{total} test gecti")
    if passed == total:
        print("  TUM TESTLER GECTI!")
    else:
        print(f"  {total - passed} test basarisiz!")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
