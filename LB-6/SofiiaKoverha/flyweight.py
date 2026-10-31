import os

class EmojiDatabase:
    @staticmethod
    def get_emoji_unicode(symbol_id):
        if not os.path.exists("emoji.db"):
            return None
        with open("emoji.db", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("=")
                if len(parts) == 2 and parts[0] == symbol_id:
                    return parts[1]
        return None

class Emoji:
    def __init__(self, symbol_id, unicode_char):
        self.symbol_id = symbol_id
        self.unicode_char = unicode_char
        print(f"[LOG] Завантаження та створення НОВОГО об'єкта для {symbol_id}")

    def draw(self):
        return self.unicode_char

class EmojiFactory:
    def __init__(self):
        self._emojis = {}

    def get_emoji(self, symbol_id):
        if symbol_id not in self._emojis:
            unicode_char = EmojiDatabase.get_emoji_unicode(symbol_id)
            if unicode_char:
                self._emojis[symbol_id] = Emoji(symbol_id, unicode_char)
            else:
                print(f"[Помилка] Ідентифікатор '{symbol_id}' відсутній у базі даних.")
                return None
        else:
            print(f"[LOG] Повторне використання ІСНУЮЧОГО об'єкта для {symbol_id}")

        return self._emojis[symbol_id]

if __name__ == "__main__":
    with open("emoji.db", "w", encoding="utf-8") as f:
        f.write("symbol-A=😀\n")
        f.write("symbol-B=🚀\n")
        f.write("symbol-C=❤️\n")
        f.write("symbol-D=🐱\n")

    factory = EmojiFactory()

    commands = [
        "draw symbol-A",
        "draw symbol-B",
        "draw symbol-A",
        "draw symbol-C",
        "draw symbol-B",
        "draw symbol-A",
        "draw symbol-X"
    ]

    print("--- Початок обробки запитів ---")
    for command in commands:
        if command.startswith("draw "):
            symbol_id = command.split(" ")[1]
            emoji_obj = factory.get_emoji(symbol_id)

            if emoji_obj:
                print(f"{command} -> {emoji_obj.draw()}")
            print("-" * 30)