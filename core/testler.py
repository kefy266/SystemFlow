import os
import json
import time
import subprocess


def disk_speedtest():
    size_mb = 64
    block = b"\0" * (1024 * 1024)
    test_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".disk-speed-test.dat",
    )

    try:
        write_started = time.perf_counter()
        with open(test_file, "wb", buffering=0) as dosya:
            for _ in range(size_mb):
                dosya.write(block)
            os.fsync(dosya.fileno())
        write_elapsed = time.perf_counter() - write_started

        read_started = time.perf_counter()
        with open(test_file, "rb", buffering=0) as dosya:
            while dosya.read(len(block)):
                pass
        read_elapsed = time.perf_counter() - read_started

        return {
            "write_mbps": round(size_mb / write_elapsed, 2),
            "read_mbps": round(size_mb / read_elapsed, 2),
        }
    except OSError as hata:
        return {"error": str(hata)}
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def hiztesti():
    try:
        sonuc = subprocess.run(
            ["speedtest-cli", "--json"],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(sonuc.stdout)
    except FileNotFoundError:
        return {"error": "speedtest-cli bulunamadi"}
    except subprocess.CalledProcessError as hata:
        return {"error": hata.stderr.strip() or str(hata)}
    except json.JSONDecodeError as hata:
        return {"error": f"Gecersiz JSON sonucu: {hata}"}

        
testveriler = {
    "disk_speedtest": disk_speedtest(),
    "speedtest": hiztesti(),
}

VERILER_YOLU = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vtesteriler.json")
with open(VERILER_YOLU, "w", encoding="utf-8") as dosya:
    json.dump(testveriler, dosya, ensure_ascii=False, indent=4)

