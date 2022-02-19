from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class BoundingBox:
    left: int
    top: int
    right: int
    bottom: int
    x: int = field(init=False)
    y: int = field(init=False)
    width: int = field(init=False)
    height: int = field(init=False)

    def __post_init__(self) -> None:
        self.x = self.left
        self.y = self.top
        self.width = self.right - self.left
        self.height = self.bottom - self.top

    def to_pil_bbox(self) -> Tuple[int, int, int, int]:
        return (self.left, self.top, self.right, self.bottom)
