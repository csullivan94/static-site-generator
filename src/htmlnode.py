from ctypes.wintypes import tagMSG

from gi.overrides.keysyms import value

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = [] if children is None else children
        self.props = {} if props is None else props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props_list = []
        for key in self.props:
            props_list.append(f' {key}="{self.props[key]}"')
        return ''.join(props_list)

    def __repr__(self):
        return f'HTMLNode(tag="{self.tag}", value="{self.value}", children={self.children}, props={self.props})'

    def __eq__(self, htmlnode):
        if self.tag == htmlnode.tag and self.value == htmlnode.value and self.children == htmlnode.children and self.props == htmlnode.props:
            return True


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)
        self.props = {} if props is None else props

        if value == None:
            raise ValueError('value required for LeafNode')

    def __repr__(self):
        return f'LeafNode(tag="{self.tag}", value="{self.value}", props={self.props})'

    def to_html(self):
        if self.tag == None:
            return self.value
        if len(self.props) > 0:
            props_html = self.props_to_html()
            return f'<{self.tag}{props_html}>{self.value}</{self.tag}>'

        return f'<{self.tag}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag, props)

        if children==None:
            raise ValueError('children required for ParentNode')

        self.children = children

        if self.tag == None:
            raise ValueError('tag required for parent node')

        if self.children == None:
            raise ValueError('children required for parent node')

        if value != None:
            raise ValueError('value not accepted in parent node')

    def __repr__(self):
        return f'ParentNode(tag="{self.tag}", children={self.children}, props={self.props})'

    def __eq__(self, htmlnode):
        if self.tag == htmlnode.tag and self.children == htmlnode.children and self.props == htmlnode.props:
            return True

    def to_html(self, i=0, html=None):
        html = [f'<{self.tag}>'] if html is None else html

        if i >= len(self.children):
            html.append(f'</{self.tag}>')
            return ''.join(html)

        if isinstance(self.children[i], LeafNode):
            html.append(self.children[i].to_html())
            i += 1
            return self.to_html(i, html)

        if isinstance(self.children[i], ParentNode):
            html.append(f'{self.children[i].to_html()}')
            i += 1
            return self.to_html(i, html)















