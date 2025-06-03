# pdf2tg

## Описание / Description

**pdf2tg** — Python-скрипт для проверки почтового ящика на новые письма с PDF-вложениями от заданного отправителя.
Сохраняет вложения, отправляет их в Telegram, помечает письма как прочитанные и удаляет локальные копии.

**pdf2tg** is a Python script that checks your email inbox for new PDF attachments from a specific sender.
It saves attachments, sends them to Telegram, marks emails as read, and deletes local copies.

---

## Требования / Requirements

- Python 3.7+
- Библиотеки: `imaplib`, `email`, `requests`, `logging`

---

## Установка / Installation

```bash
git clone https://github.com/fsdevcom2000/pdf2tg.git
cd pdf2tg
pip install -r requirements.txt
