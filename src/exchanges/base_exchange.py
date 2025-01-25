from abc import ABC, abstractmethod

class BaseExchange(ABC):
    """Abstract Base Class for Exchanges."""

    @abstractmethod
    def fetch_order_book(self, symbol):
        """Fetch the spot order book for a given symbol."""
        pass

    @abstractmethod
    def fetch_futures_order_book(self, symbol):
        """Fetch the futures order book for a given symbol."""
        pass
