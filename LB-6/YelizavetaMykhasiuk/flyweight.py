from abc import ABC, abstractmethod
from pathlib import Path

class EmojiDraw(ABC):
    @abstractmethod
    def draw(self):
        pass

class Emoji(EmojiDraw):
    def __init__(self, key, symbol):
        self.key = key
        self.symbol = symbol

    def draw(self):
        print(f"{self.symbol}")

class EmojiDatabase:
    def __init__(self, file_path):
        self._file_path = Path(file_path)
        self.back_up = {
            "symbol-A": "😀",
            "symbol-B": "🚀",
            "symbol-C": "❤️",
            "symbol-D": "😎",
            "symbol-E": "🎃",
            "symbol-F": "🤑",
            "symbol-G": "🥹",
            "symbol-H": "🤖",
            "symbol-I": "🐱",
            "symbol-J": "💻",
            "symbol-K": "🎈",
            "symbol-L": "🗽",
            "symbol-M": "🎮",
            "symbol-N": "📱"
        }

    def load(self, emoji_key):
        with open(self._file_path, encoding="utf-8-sig") as f:
            for line in f:
                key, sep, value = line.strip().partition("=")
                if sep and key.strip() == emoji_key:
                    return value.strip()
        return None

    def load_back_up(self, emoji_key):
        if self._file_path.exists():
            return self.load(emoji_key)
        return self.back_up.get(emoji_key)


class EmojiFactory:
    def __init__(self, database: EmojiDatabase):
        self._database = database
        self._flyweights: dict[str, Emoji] = {}

    def get_emoji(self, key) -> Emoji:
        emoji = self._flyweights.get(key)
        if emoji is None:
            symbol = self._database.load_back_up(key)
            if symbol is None:
                raise ValueError(f"Unknown emoji: {key}")
            print(f"FlyweightFactory: creating new flyweight for {key}.")
            emoji = Emoji(key, symbol)
            self._flyweights[key] = emoji
        else:
            print(f"FlyweightFactory: reusing existing flyweight for {key}.")
        return emoji


class Client:
    def __init__(self, factory: EmojiFactory):
        self._factory = factory

    def run(self):
        while True:
            print("1. Put a command line")
            print("2. Exit")
            choice = input("Your choice: ").strip()

            if choice == "1":
                print("There are commands ranging from A to N")
                line = input("Put a command\n Format: draw symbol-A\n").strip()
                parts = line.split()
                try:
                    self._factory.get_emoji(parts[1]).draw()
                except ValueError:
                    print(f"There is no identifier called {parts[1]}. Only from A to N.")
            elif choice == "2":
                break

if __name__ == "__main__":
    db_path = Path(__file__).resolve().parent / "emoji.db"
    Client(EmojiFactory(EmojiDatabase(str(db_path)))).run()
