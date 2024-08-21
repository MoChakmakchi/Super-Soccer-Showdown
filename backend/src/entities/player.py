
class Player:
    def __init__(self, name: str, weight: float, height: float, img_url: str = ""):
        if weight < 0 or height < 0:
            raise ValueError("Weight and height must be non-negative.")
        self.name: str = name
        self.weight: float = weight
        self.height: float = height
        self.img_url: str = img_url
