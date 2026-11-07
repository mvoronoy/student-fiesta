from pathlib import Path

DB_PATH = Path(__file__).with_name("emoji.db")

class Glyph:
    """Легковаговик: незмінні дані про один емодзі."""
    def __init__(self, number, symbol):
        self.number = number
        self.symbol = symbol

    def show(self):
        return f"{self.symbol}"


class GlyphFactory:
    """Фабрика легковаговиків: кешує створені об'єкти."""
    def __init__(self):
        self.pool = {}

    def obtain(self, code):
        """Повертає (гліф, чи_створений_щойно)."""
        if code in self.pool:
            return self.pool[code], False

        symbol = find_record_in_db(code)
        if symbol is None:
            return None, False

        glyph = Glyph(len(self.pool) + 1, symbol)
        self.pool[code] = glyph
        return glyph, True


def find_record_in_db(code):
    """Шукає символ у файлі emoji.db за формате code=symbol"""
    if not DB_PATH.exists():
        return None

    for line in DB_PATH.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            parts = line.split("=", 1)
            if parts[0].strip() == code:
                return parts[1].strip()
    return None


def process(line, factory):
    """Обробка команди користувача."""
    words = line.strip().split()
    if not words:
        return

    if len(words) != 2 or words[0] != "draw":
        print(f"'{line}': очікується формат 'draw <id>' (наприклад, draw symbol-A)")
        return

    code = words[1]
    glyph, is_new = factory.obtain(code)

    if glyph is None:
        print(f"draw {code} -> id '{code}' не знайдено в сховищі emoji.db")
        return

    status = "новий об'єкт" if is_new else "той самий об'єкт з кешу"
    print(f"draw {code} -> {glyph.show()}    [{status} №{glyph.number}]")


def main():
    factory = GlyphFactory()

    test_lines = [
           "draw symbol-A",
           "draw symbol-B",
           "draw symbol-D",
           "draw symbol-E",
           "draw symbol-A",
           "draw symbol-C",
           "draw symbol-Z"
    ]

    print("=== Автоматичні тестові запити ===")
    for line in test_lines:
        process(line, factory)

    print(f"\nУсього унікальних об'єктів у пам'яті (кеші): {len(factory.pool)}")

    print("\Введіть свої команди (наприклад: draw symbol-A). Для виходу натисніть Enter:")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            break
        process(line, factory)


if __name__ == "__main__":
    main()