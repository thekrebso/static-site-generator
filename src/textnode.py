from enum import Enum
from typing import Optional


class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    text: str
    text_type: TextType
    url: Optional[str]

    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self) -> str:
        url = f'"{self.url}"' if isinstance(self.url, str) else "None"
        return f'TextNode("{self.text}", {self.text_type}, {url})'
