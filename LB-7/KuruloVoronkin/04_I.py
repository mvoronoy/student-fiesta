from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print_document(self) -> None:
        pass


class Scanner(ABC):
    @abstractmethod
    def scan_document(self) -> None:
        pass


class Fax(ABC):
    @abstractmethod
    def fax_document(self) -> None:
        pass


class SimplePrinter(Printer):
    def print_document(self) -> None:
        print("Printing document")


class MultiFunctionPrinter(Printer, Scanner, Fax):
    def print_document(self) -> None:
        print("Printing document")

    def scan_document(self) -> None:
        print("Scanning document")

    def fax_document(self) -> None:
        print("Faxing document")


if __name__ == "__main__":
    printer = SimplePrinter()
    printer.print_document()

    mfp = MultiFunctionPrinter()
    mfp.print_document()
    mfp.scan_document()
    mfp.fax_document()