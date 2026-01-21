#!/usr/bin/env python
"""Скрипт для просмотра отправленных писем из папки sent_emails"""

import os
import sys
from pathlib import Path

EMAIL_DIR = Path(__file__).parent / 'api_yamdb' / 'sent_emails'

if not EMAIL_DIR.exists():
    print(f"❌ Папка {EMAIL_DIR} не найдена")
    print("📧 Письма еще не отправлялись")
    sys.exit(0)

emails = sorted(EMAIL_DIR.glob('*'))

if not emails:
    print("📧 Нет отправленных писем")
    sys.exit(0)

print(f"📧 Найдено писем: {len(emails)}\n")

for email_file in emails:
    print(f"{'='*60}")
    print(f"📬 {email_file.name}")
    print(f"{'='*60}")
    with open(email_file, 'r', encoding='utf-8') as f:
        print(f.read())
    print()
