from typing import Optional
from functools import reduce


class HTMLNode():
    def __init__(
            self, 
            tag: Optional[str] = None, 
            value: Optional[str] = None, 
            children: Optional[list['HTMLNode']] = None, 
            props: Optional[dict[str,str]] = None
        ) -> None:
        
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("child classes should implement this method")

    def props_to_html(self) -> str:
        if not isinstance(self.props, dict):
            return ""
        return reduce(lambda acc, pair: acc + f' {pair[0]}="{pair[1]}"', self.props.items(), "")

    def __repr__(self) -> str:
        tag = f'"{self.tag}"' if isinstance(self.tag, str) else "None"
        value = f'"{self.value}"' if isinstance(self.value, str) else "None"
        children = self.children if isinstance(self.children, list) else "None"
        props = self.props if isinstance(self.props, dict) else "None"

        return f'HTMLNode({tag}, {value}, {children}, {props})'


class LeafNode(HTMLNode):
    def __init__(
            self, 
            tag: Optional[str],
            value: str,
            props: Optional[dict[str,str]] = None
        ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == "" or not isinstance(self.value, str):
            raise ValueError("value is required for a leaf node")
        
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
