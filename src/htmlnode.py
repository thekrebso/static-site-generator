from typing import Optional
from functools import reduce


class HTMLNode():
    def __init__(
            self, 
            tag: Optional[str] = None, 
            value: Optional[str] = None, 
            children: Optional[list[object]] = None, 
            props: Optional[dict[str,str]] = None
        ) -> None:
        
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

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
