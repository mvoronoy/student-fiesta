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
    """Вміє лише друкувати - більше жодних зайвих методів."""

    def print_document(self):
        print("Printing document")


class MultiFunctionDevice(Printer, Scanner, Fax):
    """БФП реалізує всі три інтерфейси."""

    def print_document(self):
        print("Printing document")

    def scan_document(self):
        print("Scanning document")

    def fax_document(self):
        print("Faxing document")


if __name__ == "__main__":
    printer = SimplePrinter()
    printer.print_document()

    mfd = MultiFunctionDevice()
    mfd.print_document()
    mfd.scan_document()
    mfd.fax_document()