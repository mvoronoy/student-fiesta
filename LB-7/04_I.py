#
#  Fix violation of Interface Segregation Principle (ISP)
# Clients should not be forced to depend on methods they do not use.
#

from abc import ABC, abstractmethod

class Machine(ABC):
    @abstractmethod
    def print_document(self):
        pass

    @abstractmethod
    def scan_document(self):
        pass

    @abstractmethod
    def fax_document(self):
        pass


class SimplePrinter(Machine):
    def print_document(self):
        print("Printing document")

    def scan_document(self):
        raise NotImplementedError()

    def fax_document(self):
        raise NotImplementedError()
