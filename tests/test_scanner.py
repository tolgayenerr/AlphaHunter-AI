import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scanner import scan_market

print("BIST taranıyor...")

df = scan_market()

print(df.head())

print()

print("Toplam hisse:", len(df))