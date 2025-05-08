from __future__ import annotations

import copy
import dataclasses
import datetime
import functools
import posixpath
import urllib.parse
from pathlib import Path
from typing import Callable, Iterable, Any, ClassVar
from xml.etree import ElementTree as ET

import markdown

from util import sluggify, get_slug_and_optional_date

markdown_parser = markdown.Markdown(extensions=['meta', 'extra'])


def get_highest_level_heading_tag(body: ET.Element) -> str | None:
    """ return the highest level heading tag occurring in `body`, or None if there are no headings.  """
    for tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        if (el := body.find(tag)) is not None:
            return el.tag
    return None


def section_by_heading(body: ET.Element, heading: str = None) -> None:
    """ split body into sections based on top-level headings. """
    if heading is None:
        heading = get_highest_level_heading_tag(body)
    sections = []
    section = []
    for el in body:
        if el.tag == heading:
            sections.append(section)
            section = [el]
        else:
            section.append(el)
    sections.append(section)

    def make_section_element(children: Iterable[ET.Element]) -> ET.Element:
        el = ET.SubElement(body, 'section')
        el.extend(children)
        return el

    body[:] = [*sections[0], *(make_section_element(children) for children in sections[1:])]


def extract_title(body: ET.Element, include_markup: bool = False) -> str | None:
    """ returns the text of the first highest-level header"""
    for tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        if (h := body.find(f'.//{tag}')) is not None:
            break
    else:
        return None
    if include_markup:
        raise NotImplementedError()
    return h.text


def identify_primary_image(body: ET.Element) -> ET.Element | None:
    """ find the primary image in document body.

    If there is an image with .headline class, this is the primary image.
    Otherwise, the first image element is returned, or None if there are no images.
    """
    return next((img for img in body.iter('img') if 'headline' in img.get('class', '').split()), None) or next(body.iter('img'), None)


def process_headline_image(body: ET.Element) -> None:
    """ give headline images the class `headline` and move them to a div.

    An image is considered a headline image if:
        - it is the first image in the document, and
        - it is the only child of a top-level <p> element, and
        - it is not preceded by any text content.
    """
    for i, el in enumerate(body):
        if el.text:
            return
        if el.tag == 'p' and len(el) == 1 and el[0].tag == 'img':
            el.tag = 'div'
            classes = el.get('class', '').split()
            if 'headline' not in classes:
                classes.append('headline')
                el.set('class', ' '.join(classes))


def mutate_image_to_picture(el: ET.Element) -> ET.Element:
    """ change an <img> element to a <picture> element with <source> and <img> children in-place. """
    src = urllib.parse.urlsplit(el.get('src'))
    root, ext = posixpath.splitext(src.path)
    webp_url = urllib.parse.urlunsplit(src._replace(path=root+'.webp'))
    fallback_url = urllib.parse.urlunsplit(src._replace(path=root+'.jpg')) if ext == '.webp' else el.get('src')

    el.tag = 'picture'
    ET.SubElement(el, 'source', srcset=webp_url, type='image/webp')
    ET.SubElement(el, 'img', attrib=el.attrib, src=fallback_url)
    el.attrib = {}
    return el


@dataclasses.dataclass
class Document:
    slug: str
    root: ET.Element
    """ Markdown-generated root element directly contains all <p>, <h1>, <h2>, etc. """
    primary_image: ET.Element = None
    """ image used in preview and at the top of page """
    metadata: dict[str] = dataclasses.field(default_factory=dict)

    METADATA_TRANSFORMERS: ClassVar[dict[str, Callable[[str], Any]]] = {
        'date': datetime.date.fromisoformat
    }
    """ functions applied to markdown metadata with matching keys """

    @classmethod
    def load_file(cls, path: Path, default_metadata: dict = {}, metadata_overrides: dict = {}):
        """ Create a Document from a path to markdown source

        :param path: path to .md file
        :param default_metadata: metadata which will be overwritten by metadata extracted from the document
        :param metadata_overrides: metadata which will overwrite metadata extracted from the document
        :return: A new Document. Slug is based on the filename.
        """
        if path.suffix not in ('.md', '.html', '.htm'):
            raise ValueError(f'Document.load_file() expects a markdown file, got {path}')
        slug, date = get_slug_and_optional_date(path.stem)
        if date is not None:
            metadata_overrides = {'date': date, **metadata_overrides}
        return cls.from_string(path.read_text(), slug=slug, default_metadata=default_metadata, metadata_overrides=metadata_overrides)

    @classmethod
    def from_string(cls, text: str, slug: str | None = None, *, default_metadata: dict = {}, metadata_overrides: dict = {}) -> Document:
        """ Create a Document from Markdown source text.

        :param text: Markdown source
        :param slug: document identifier. Defaults to document title.
        :param default_metadata: metadata which will be overwritten by metadata extracted from the document
        :param metadata_overrides: metadata which will overwrite metadata extracted from the document
        :return: A new Document.
        """
        inner_html = markdown_parser.reset().convert(text)
        document_metadata = getattr(markdown_parser, 'Meta', None) or {}
        cls.transform_document_metadata(document_metadata)
        metadata = {**default_metadata, **document_metadata, **metadata_overrides}
        root = ET.fromstring(f'<html>{inner_html}</html>')
        # deep copy to avoid problems with double-rewriting urls.
        primary_image = copy.deepcopy(identify_primary_image(root))
        # for img in list(root.iter('img')):
        #     mutate_image_to_picture(img)
        mutate_image_to_picture(primary_image)

        instance = cls(slug, root, metadata=metadata, primary_image=primary_image)
        if instance.slug is None:
            instance.slug = sluggify(instance.title)
        return instance

    @functools.cached_property
    def title(self) -> str:
        return extract_title(self.root)

    def inner_html(self):
        return ET.tostring(self.root, encoding='unicode').replace('<html>', '').replace('</html>', '')

    @staticmethod
    def _rewrite_urls(tree: ET.Element | ET.ElementTree, fn: Callable[[str], str]) -> None:
        for el in tree.iter('img'):
            el.set('src', fn(el.get('src')))
        for el in tree.iter('a'):
            el.set('href', fn(el.get('href')))
        for el in tree.iter('source'):
            el.set('srcset', ','.join(fn(src.strip()) for src in el.get('srcset').split(',')))

    def rewrite_urls(self, fn: Callable[[str], str]) -> None:
        self._rewrite_urls(self.root, fn)
        self._rewrite_urls(self.primary_image, fn)

    @classmethod
    def transform_document_metadata(cls, metadata: dict):
        for key, value in metadata.items():
            value = '\n'.join(value)  # lines are split for some reason
            if key in cls.METADATA_TRANSFORMERS:
                value = cls.METADATA_TRANSFORMERS[key](value)
            metadata[key] = value

    def iter_img_srcs(self, root: ET.Element = None) -> Iterable[str]:
        """ iterate over all image urls referenced in the document. """
        if root is None:
            root = self.root
        for el in root.iter():
            if src := el.get('src'):
                yield src
            if srcset := el.get('srcset'):
                yield from (src.strip() for src in srcset.split(','))

    def iter_dependencies(self) -> Iterable[urllib.parse.SplitResult]:
        """ iterate over all local image urls referenced in the document. """
        yield from (url for src in self.iter_img_srcs() if not (url := urllib.parse.urlsplit(src)).netloc)
        # FIXME: gallery item dependencies should be separate. Also why do we yield SplitResult here?
        if self.primary_image:
            for src in self.iter_img_srcs(root=self.primary_image):
                if (url := urllib.parse.urlsplit(src)).netloc:
                    continue
                yield url._replace(path=posixpath.splitext(url.path)[0] + '.webp')
