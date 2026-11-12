#
#  Fix violation of Interface Segregation Principle (ISP)
# Clients should not be forced to depend on methods they do not use.
#

from abc import ABC, abstractmethod

class Printer(ABC):
    @abstractmethod
    def print_document(self):
        ...


class Scanner(ABC):
    @abstractmethod
    def scan_document(self):
        ...


class FaxMachine(ABC):
    @abstractmethod
    def fax_document(self):
        ...


class SimplePrinter(Printer):
    def print_document(self):
        print("Printing document")


class MultiFunctionDevice(Printer, Scanner, FaxMachine):
    def print_document(self):
        print("MFD: printing document")

    def scan_document(self):
        print("MFD: scanning document")

    def fax_document(self):
        print("MFD: faxing document")
