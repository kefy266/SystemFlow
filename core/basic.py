import os
import platform
import json
import subprocess

def isletim_sistemi():
    return platform.system()

def user():
    return os.getlogin()

def cpu_cekirdek():
    return os.cpu_count()

def cpu_yuk():
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return os.cpu_count()

def gorev_yoneticisi():
    return os.getpid()


def ram():
    result = subprocess.run(["free", "-h"], capture_output=True, text=True, check=True)
    mem_line = next(line for line in result.stdout.splitlines() if line.startswith("Mem:"))
    _, total, used, free, shared, cache, available = mem_line.split()
    return f"{used} used of {total} (available: {available})"

def cekirdek():
    sonuc = subprocess.run(["uname", "-r"], capture_output=True, text=True)
    return sonuc.stdout.strip()

def mevcut_dizin():
    return os.getcwd()


veriler = {
    "isletim_sistemi": isletim_sistemi(),
    "kullanici": user(),
    "cpu_cekirdek": cpu_cekirdek(),
    "cpu_yuk": cpu_yuk(),
    "pid": gorev_yoneticisi(),
    "ram": ram(),
    "cekirdek": cekirdek(),
    "mevcut_dizin": mevcut_dizin()
}

VERILER_YOLU = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "veriler.json")
with open(VERILER_YOLU, "w", encoding="utf-8") as dosya:
    json.dump(veriler, dosya, ensure_ascii=False, indent=4)