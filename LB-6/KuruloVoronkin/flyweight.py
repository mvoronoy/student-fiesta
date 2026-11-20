import os
import sys
from abc import ABC, abstractmethod


class EmojiFlyweight(ABC):
    @abstractmethod
    def draw(self) -> None:
        pass


class Emoji(EmojiFlyweight):
    def __init__(self, symbol_id: str, unicode_char: str, description: str):
        self._symbol_id = symbol_id
        self._unicode_char = unicode_char
        self._description = description
        print(f"  [NEW] Створено об'єкт Emoji для '{symbol_id}' (адреса в пам'яті: {hex(id(self))})")

    @property
    def symbol_id(self) -> str:
        return self._symbol_id

    @property
    def unicode_char(self) -> str:
        return self._unicode_char

    def draw(self) -> None:
        print(f"draw {self._symbol_id} -> {self._unicode_char} ({self._description})")


class EmojiDatabase:
    def __init__(self, db_file: str = "emoji.db"):
        self._db_file = db_file
        self._ensure_db_exists()

    @property
    def db_file(self) -> str:
        return self._db_file

    def _ensure_db_exists(self) -> None:
        if os.path.exists(self._db_file):
            return

        default_data = {
            "symbol-A": ("😀", "Усміхнене обличчя"),
            "symbol-B": ("🚀", "Ракета"),
            "symbol-C": ("❤️", "Червоне серце"),
            "symbol-D": ("🍕", "Шматочок піци"),
            "symbol-E": ("🔥", "Вогонь"),
            "symbol-F": ("💻", "Ноутбук"),
            "symbol-G": ("🎉", "Святкова хлопавка"),
            "symbol-H": ("🌟", "Сяюча зірка"),
            "symbol-I": ("🐱", "Мордочка кота"),
            "symbol-J": ("☕", "Гаряча кава"),
            "symbol-K": ("⚡", "Блискавка"),
            "symbol-L": ("🎯", "Влучання в ціль"),
            "symbol-M": ("🧠", "Мозок"),
            "symbol-N": ("🔒", "Закритий замок"),
            "symbol-O": ("📦", "Коробка"),
            "symbol-P": ("🛠️", "Молоток і гайковий ключ"),
            "symbol-Q": ("🌍", "Планета Земля"),
            "symbol-R": ("🎵", "Музична нота"),
            "symbol-S": ("🏆", "Кубок переможця"),
            "symbol-T": ("📚", "Стопка книг"),
            "symbol-U": ("💡", "Лампочка ідеї"),
            "symbol-V": ("🛡️", "Щит захисту"),
            "symbol-W": ("⏱️", "Секундомір"),
            "symbol-X": ("🎲", "Гральний кубик"),
            "symbol-Y": ("🧩", "Пазл"),
            "symbol-Z": ("✅", "Зелена галочка"),
        }

        with open(self._db_file, "w", encoding="utf-8") as f:
            for key, (char, desc) in default_data.items():
                f.write(f"{key}|{char}|{desc}\n")

    def load(self, symbol_id: str) -> tuple[str, str] | None:
        print(f"  [DB] Пошук '{symbol_id}' у сховищі '{self._db_file}'...")
        if not os.path.exists(self._db_file):
            return None

        with open(self._db_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3 and parts[0] == symbol_id:
                    return parts[1], parts[2]
        return None


class EmojiFactory:
    def __init__(self, database: EmojiDatabase):
        self._database = database
        self._cache: dict[str, Emoji] = {}

    def get_emoji(self, symbol_id: str) -> Emoji | None:
        if symbol_id in self._cache:
            emoji = self._cache[symbol_id]
            print(f"  [CACHE] Повторне використання '{symbol_id}' (адреса в пам'яті: {hex(id(emoji))})")
            return emoji

        record = self._database.load(symbol_id)
        if record is None:
            print(f"  [ERROR] Ідентифікатор '{symbol_id}' відсутній у '{self._database.db_file}'!")
            return None

        unicode_char, description = record
        emoji = Emoji(symbol_id, unicode_char, description)
        self._cache[symbol_id] = emoji
        return emoji

    def show_stats(self) -> None:
        print("\n=== Статистика кешу Flyweight ===")
        print(f"Унікальних об'єктів у пам'яті: {len(self._cache)}")
        for sym_id, obj in self._cache.items():
            print(f" - {sym_id}: {obj.unicode_char} (адреса: {hex(id(obj))})")
        print("=================================\n")


def execute_command(command: str, factory: EmojiFactory) -> None:
    parts = command.strip().split(maxsplit=1)
    if len(parts) != 2 or parts[0] != "draw":
        print(f"  [ERROR] Невірний формат команди: '{command}'. Очікується: draw <id>")
        return

    emoji = factory.get_emoji(parts[1])
    if emoji is not None:
        emoji.draw()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    db = EmojiDatabase("emoji.db")
    factory = EmojiFactory(db)

    demo_requests = [
        "draw symbol-A",
        "draw symbol-B",
        "draw symbol-A",
        "draw symbol-C",
        "draw symbol-B",
        "draw symbol-A",
        "draw symbol-D",
        "draw symbol-D",
        "draw symbol-UNKNOWN",
    ]

    print("=== Демонстрація роботи патерну Flyweight ===")
    for cmd in demo_requests:
        print(f"\nЗапит: {cmd}")
        execute_command(cmd, factory)

    factory.show_stats()

    print("Інтерактивний режим (доступні symbol-A ... symbol-Z, для виходу введіть 'exit'):")
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        execute_command(user_input, factory)

    factory.show_stats()


if __name__ == "__main__":
    main()