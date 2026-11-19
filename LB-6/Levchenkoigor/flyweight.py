# flyweight.py
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emoji.db")

# Дані для створення emoji.db
DEFAULT_DATA = {
    "symbol-A": "😀", "symbol-B": "🚀", "symbol-C": "❤️", "symbol-D": "🔥",
    "symbol-E": "🎉", "symbol-F": "🌍", "symbol-G": "🐱", "symbol-H": "🐶",
    "symbol-I": "🍕", "symbol-J": "⚽", "symbol-K": "🎸", "symbol-L": "📚",
    "symbol-M": "💡", "symbol-N": "🌈", "symbol-O": "⭐", "symbol-P": "🍎",
    "symbol-Q": "🚗", "symbol-R": "✈️", "symbol-S": "🏠", "symbol-T": "🎮",
    "symbol-U": "☕", "symbol-V": "🌸", "symbol-W": "🐼", "symbol-X": "🎧",
    "symbol-Y": "💎", "symbol-Z": "🏆", "symbol-1": "😎", "symbol-2": "🤖",
    "symbol-3": "👻", "symbol-4": "🦄",
}


class EmojiDatabase:
    """Умовне сховище описів емодзі"""

    def __init__(self, path=DB_FILE):
        self.path = path
        if not os.path.exists(self.path):
            self._create_default()

    def _create_default(self):
        with open(self.path, "w", encoding="utf-8") as f:
            for key, value in DEFAULT_DATA.items():
                f.write(f"{key}={value}\n")

    def find(self, emoji_id):
        """Повертає опис емодзі або None, якщо ідентифікатора немає."""
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key == emoji_id:
                    return value
        return None


class Emoji:
    """Flyweight: незмінний об'єкт з описом емодзі."""

    __slots__ = ("_emoji_id", "_char")

    def __init__(self, emoji_id, char):
        self._emoji_id = emoji_id
        self._char = char

    def draw(self):
        print(f"draw {self._emoji_id} -> {self._char}")


class EmojiFactory:
    """Flyweight Factory: створює об'єкти один раз і використовує повторно."""

    def __init__(self, database):
        self._database = database
        self._pool = {}

    def get_emoji(self, emoji_id):
        emoji = self._pool.get(emoji_id)
        if emoji is not None:
            print(f"  [factory] повторне використання '{emoji_id}'")
            return emoji

        # Lazy initialization: завантаження зі сховища лише при першому зверненні
        char = self._database.find(emoji_id)
        if char is None:
            raise KeyError(f"Емодзі '{emoji_id}' не знайдено у сховищі")

        print(f"  [factory] завантаження '{emoji_id}' зі сховища, створено новий об'єкт")
        emoji = Emoji(emoji_id, char)
        self._pool[emoji_id] = emoji
        return emoji

    @property
    def created_count(self):
        return len(self._pool)


class Client:
    """Client: обробляє команди користувача."""

    def __init__(self, factory):
        self._factory = factory

    def execute(self, command):
        parts = command.strip().split()
        if len(parts) != 2 or parts[0].lower() != "draw":
            print("  Невірна команда. Формат: draw <id>")
            return
        try:
            self._factory.get_emoji(parts[1]).draw()
        except KeyError as e:
            print(f"  Помилка: {e.args[0]}")


def main():
    factory = EmojiFactory(EmojiDatabase())
    client = Client(factory)

    # Демонстраційний сценарій
    demo = [
        "draw symbol-A", "draw symbol-B", "draw symbol-A",
        "draw symbol-C", "draw symbol-B", "draw symbol-A",
        "draw symbol-UNKNOWN",
    ]
    for cmd in demo:
        print(f"> {cmd}")
        client.execute(cmd)

    print(f"\nУнікальних об'єктів створено: {factory.created_count}")

    # Інтерактивний режим
    print("\nВведіть команду (draw <id>) або 'exit' для виходу:")
    while True:
        cmd = input("> ").strip()
        if cmd.lower() in ("exit", "quit"):
            break
        client.execute(cmd)

    print(f"Унікальних об'єктів створено: {factory.created_count}")


if __name__ == "__main__":
    main()