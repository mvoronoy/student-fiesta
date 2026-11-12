# В оригінальному варіанті абстрактний клас Machine змушував всі похідні класи реалізовувати одночасно print_document(), scan_document() та fax_document()
# Нам же потрібно було, щоб інтерфейси були сегреговані, тобто щоб клієнти не залежали від інтерфейсів, які вони не використовують.
# Тому великий інтерфейс Machine був розбитий на вузькоспеціалізовані інтерфейси (Printer, Scanner, Fax), щоб класи реалізовували лише потрібні їм можливості.

from abc import ABC, abstractmethod

class Printer(ABC):
    @abstractmethod
    def print_document(self):
        pass

class Scanner(ABC):
    @abstractmethod
    def scan_document(self):
        pass

class Fax(ABC):
    @abstractmethod
    def fax_document(self):
        pass

class SimplePrinter(Printer):
    def print_document(self):
        print("Printing document")

class MultiFunctionPrinter(Printer, Scanner, Fax):
    def print_document(self):
        print("Printing document")

    def scan_document(self):
        print("Scanning document")

    def fax_document(self):
        print("Faxing document")
