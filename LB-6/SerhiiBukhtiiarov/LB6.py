import os

DB_FILENAME = "emoji.db"

def create_sample_database():
    if not os.path.exists(DB_FILENAME):
        data = {
            "symbol-A": "😀",
            "symbol-B": "🚀",
            "symbol-C": "❤️",
            "symbol-D": "🔥",
            "symbol-E": "🎉"
        }
        with open(DB_FILENAME, "w", encoding="utf-8") as f:
            for symbol_id, char in data.items():
                f.write(f"{symbol_id}:{char}\n")

class Emoji:
    def __init__(self, symbol_id: str, character: str):
        self.symbol_id = symbol_id
        self.character = character

    def draw(self):
        print(f"{self.character}", end="")


class EmojiDatabase:
    def __init__(self, db_filename: str = DB_FILENAME):
        self.db_filename = db_filename

    def find_emoji_data(self, symbol_id: str) -> str | None:
        if not os.path.exists(self.db_filename):
            raise FileNotFoundError(f"Сховище {self.db_filename} не знайдено!")

        with open(self.db_filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                s_id, char = line.split(":", 1)
                if s_id.strip() == symbol_id:
                    return char.strip()
        return None


class EmojiFactory:
    def __init__(self, database: EmojiDatabase):
        self._database = database
        self._flyweights: dict[str, Emoji] = {}

    def get_emoji(self, symbol_id: str) -> Emoji:
        if symbol_id in self._flyweights:
            print(f"[CACHE HIT] Об'єкт '{symbol_id}' взято з кешу фабрики.", end=" ")
            return self._flyweights[symbol_id]

        print(f"[CACHE MISS] Завантаження з бази даних '{symbol_id}'...", end=" ")
        char_data = self._database.find_emoji_data(symbol_id)

        if char_data is None:
            raise ValueError(f"Помилка: Ідентифікатор '{symbol_id}' відсутній у сховищі!")

        emoji = Emoji(symbol_id, char_data)
        self._flyweights[symbol_id] = emoji
        return emoji

    def get_loaded_count(self) -> int:
        return len(self._flyweights)


class Client:
    def __init__(self, factory: EmojiFactory):
        self.factory = factory

    def execute_command(self, command: str):
        parts = command.strip().split()
        if len(parts) != 2 or parts[0] != "draw":
            print(f"Невідома команда: '{command}'")
            return

        symbol_id = parts[1]
        print(f"Запит: {command} -> Результат: ", end="")

        try:
            emoji = self.factory.get_emoji(symbol_id)
            emoji.draw()
            print()
        except ValueError as e:
            print(f"\n{e}")


if __name__ == "__main__":
    create_sample_database()

    db = EmojiDatabase(DB_FILENAME)
    factory = EmojiFactory(db)
    client = Client(factory)

    requests = [
        "draw symbol-A",
        "draw symbol-B",
        "draw symbol-A",
        "draw symbol-C",
        "draw symbol-B",
        "draw symbol-A",
        "draw symbol-X"
    ]

    for req in requests:
        client.execute_command(req)

    print(f"\nЗагальна кількість унікальних об'єктів у пам'яті: {factory.get_loaded_count()}")