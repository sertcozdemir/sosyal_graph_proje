# graph_algorithms/base.py
from abc import ABC, abstractmethod
from core.graph import Graph


class Algorithm(ABC):
    """
    Tüm algoritmalar için ortak soyut temel sınıf.
    """

    def __init__(self, graph: Graph):
        self.graph = graph

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Algoritmanın ana çalıştırma noktası.
        """
        ...
