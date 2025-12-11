class Node:
    def __init__(self, node_id: int,
                 aktiflik: float = 0.0,
                 etkilesim: float = 0.0,
                 baglanti_sayisi: int = 0):
        self.id = node_id
        self.aktiflik = aktiflik
        self.etkilesim = etkilesim
        self.baglanti_sayisi = baglanti_sayisi
        self.neighbors = set()  # komşu node id'leri

    def __repr__(self) -> str:
        return (f"Node(id={self.id}, aktiflik={self.aktiflik}, "
                f"etkilesim={self.etkilesim}, baglanti_sayisi={self.baglanti_sayisi})")
