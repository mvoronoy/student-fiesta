import os
import sys

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()

DB_FILE = os.path.join(BASE_DIR, "emoji.db")

class EmojiDatabase:
    def __init__(self, path=DB_FILE):
        self.path = path
        self.reads_count = 0

    def load_emoji(self, symbol):
        """Шукає опис у файлі. Файл читається лише при зверненні (lazy)."""
        self.reads_count += 1
        print(f"[DATABASE] Loading description for {symbol}...")

        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key.strip() == symbol:
                    return value.strip()
        return None

    def get_all_symbols(self):
        symbols = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                symbols.append(line.split("=", 1)[0].strip())
        return symbols

class Emoji:
    __slots__ = ("_symbol", "_unicode_value")

    def __init__(self, symbol, unicode_value):
        self._symbol = symbol
        self._unicode_value = unicode_value

    @property
    def symbol(self):
        return self._symbol

    @property
    def unicode_value(self):
        return self._unicode_value

    def draw(self):
        print(f"draw {self._symbol} -> {self._unicode_value}")

class EmojiFactory:
    def __init__(self, database):
        self._database = database
        self._cache = {}
        self.created_count = 0
        self.reused_count = 0

    def get_emoji(self, symbol):
        if symbol in self._cache:
            self.reused_count += 1
            print(f"[FACTORY] Reusing existing object: {symbol}")
            return self._cache[symbol]

        unicode_value = self._database.load_emoji(symbol)

        if unicode_value is None:
            print(f"[ERROR] Emoji '{symbol}' not found in database!")
            return None

        print(f"[FACTORY] Creating new object: {symbol}")
        emoji = Emoji(symbol, unicode_value)
        self._cache[symbol] = emoji
        self.created_count += 1
        return emoji

    def show_statistics(self):
        print("\n========== STATISTICS ==========")
        print(f"Created objects:   {self.created_count}")
        print(f"Reused objects:    {self.reused_count}")
        print(f"Objects in cache:  {len(self._cache)}")
        print(f"Database reads:    {self._database.reads_count}")
        print("Cached emojis:")
        for symbol, emoji in self._cache.items():
            print(f"  {symbol}: {emoji.unicode_value}")
        print("================================")

def run_demo(factory):
    """Демонстрація послідовності запитів із завдання."""
    print("\n--- DEMO ---")
    for symbol in ["symbol-A", "symbol-B", "symbol-A",
                   "symbol-C", "symbol-B", "symbol-A"]:
        print(f"\n> draw {symbol}")
        emoji = factory.get_emoji(symbol)
        if emoji is not None:
            emoji.draw()

    print("\n> draw symbol-XYZ")
    emoji = factory.get_emoji("symbol-XYZ")
    if emoji is not None:
        emoji.draw()

    a1 = factory.get_emoji("symbol-A")
    a2 = factory.get_emoji("symbol-A")
    print(f"\nОдин і той самий об'єкт для symbol-A: {a1 is a2}")

    factory.show_statistics()

def print_help():
    print("======================================")
    print("       FLYWEIGHT EMOJI SYSTEM")
    print("======================================")
    print("Available commands:")
    print("  draw symbol-A   - show emoji by identifier")
    print("  demo            - run the sequence A, B, A, C, B, A")
    print("  stats           - show factory statistics")
    print("  list            - list available identifiers")
    print("  help            - show this help")
    print("  exit            - quit")
    print("======================================")

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    database = EmojiDatabase()
    factory = EmojiFactory(database)

    print_help()

    while True:
        try:
            command = input("\nEnter command: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nProgram terminated.")
            break

        lower = command.lower()

        if lower == "exit":
            print("Program terminated.")
            break
        elif lower == "help":
            print_help()
        elif lower == "stats":
            factory.show_statistics()
        elif lower == "demo":
            run_demo(factory)
        elif lower == "list":
            print("\nAvailable emoji identifiers:")
            for symbol in database.get_all_symbols():
                print(f"  {symbol}")
        elif lower.startswith("draw "):
            symbol = command[5:].strip()
            if not symbol:
                print("[ERROR] Please specify an emoji identifier.")
                continue
            if symbol.lower().startswith("symbol-"):
                symbol = "symbol-" + symbol[7:].upper()

            emoji = factory.get_emoji(symbol)
            if emoji is not None:
                emoji.draw()
        else:
            print("[ERROR] Unknown command. Type 'help' for the list of commands.")


if __name__ == "__main__":
    main()