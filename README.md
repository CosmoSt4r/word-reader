
# Поиск по ключевым словам в документах

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Поддерживаемые форматы:
 - PDF
 - TXT
 - DOC
 - DOCX

![Screenshot](https://raw.githubusercontent.com/CosmoSt4r/word-reader/screenshots/screenshot.png)

## Запуск

Клонируйте репозиторий:
```bash
git clone https://github.com/CosmoSt4r/word-reader
cd word-reader
```

Запустите с интерфейсом (PyQt5):
```bash
python gui.py
```

Или используйте в качестве модуля:
```py
from wordreader import scanner

result: dict = scanner.find_in_files(
    'поисковый запрос',
    ['file.doc', 'file.docx'],
    case_sensitive=True,
)
```

Запуск тестов:
```bash
pytest tests
```


