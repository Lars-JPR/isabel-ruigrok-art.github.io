#!/bin/env python3
from __future__ import annotations

import datetime
import functools
import itertools
import logging
import os
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

import jinja2
import markupsafe

from assets import Asset
from document import Document, markdown_parser
from resources import Resource, Piece, Project
from config import CONFIG

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(CONFIG.templates_dir)
)

# Add zero width spaces around sequences of non-alphanumerical characters in sequences of alphanumerical characters.
# e.g. 'tekeningen/schilderijen' -> 'tekeningen[ZWSP]/[ZWSP]schilderijen'
jinja_environment.filters['morebreaks'] = functools.partial(re.sub, re.compile(r"(\w{2,})([^\w\s'-]+)(\w{2,})"), r'\1​\2​\3')


def build_resource(resource: Resource) -> Path:
    page_template = jinja_environment.get_template(f'resource_page.html')
    page_dir = CONFIG.output_dir / resource.DIRECTORY / resource.slug
    page_file = page_dir / 'index.html'
    description = resource.description
    page = page_template.render(
        title=description.title,
        content=description.inner_html()
    )

    logging.info('%s -> %s', resource.slug, page_file)
    page_dir.mkdir(exist_ok=True, parents=True)
    page_file.write_text(page)
    assets = {p.stem: Asset(p) for p in resource.asset_paths}
    for dependency in description.iter_dependencies():
        path = Path(dependency.path)
        if not path.is_absolute():
            path = page_dir / path
        if path.stem in assets:
            assets[path.stem].to(path)
        else:
            logging.warning('Missing asset %s', path)
    return page_file


def gallery_item(resource: Resource) -> dict:
    description = resource.description_with_absolute_urls
    # TODO: automatically determine this from image dimensions
    is_wide = 'wide' in description.primary_image.get('class', '').split()
    picture_html = markupsafe.Markup(re.sub(r'class="[^"]*"', '', ET.tostring(description.primary_image, encoding='unicode')))
    return dict(
        link='/' + '/'.join(resource.DIRECTORY.parts) + '/' + resource.slug + '/',
        title=description.title,
        picture=picture_html,
        wide=is_wide
    )


def build_resources_index(resources: Iterable[Resource], kind: type[Resource] | str) -> Path:
    kind = Path(getattr(kind, 'DIRECTORY', kind))
    output_path = CONFIG.output_dir / kind / 'index.html'
    template = jinja_environment.get_template(f'resource_index.html')
    page = template.render(items=(gallery_item(r) for r in resources if r.DIRECTORY == kind))
    logging.info('-> %s', output_path)
    output_path.write_text(page)
    return output_path


def build_homepage(output_path: Path = Path('index.html')) -> Path:
    output_path = output_path if output_path.is_absolute() else CONFIG.output_dir / output_path
    template = jinja_environment.get_template('index.html')
    about_path = CONFIG.homepage_dir / 'about.md'
    if about_path.exists():
        about = markdown_parser.convert(about_path.read_text())
    else:
        about = ''
        logging.warning('no about.md found in %s', CONFIG.homepage_dir)
    page = template.render(about=about)
    logging.info('-> %s', output_path)
    output_path.write_text(page)
    return output_path


def sync_static_path(src: Path) -> Path:
    dst = CONFIG.output_dir / src.relative_to(CONFIG.input_dir)
    if src.is_file():
        if not dst.exists():
            try:
                os.link(src, dst)
                logging.info('%s => %s', src, dst)
            except OSError:
                shutil.copy2(src, dst)
                logging.info('%s -> %s', src, dst)
        elif dst.samefile(src):
            pass
        else:
            shutil.copy2(src, dst)
            logging.info('%s -> %s', src, dst)
    elif src.is_dir():
        if not dst.exists():
            try:
                shutil.copytree(src, dst, copy_function=os.link)
                logging.info('%s => %s', src, dst)
            except OSError:
                shutil.copytree(src, dst)
                logging.info('%s -> %s', src, dst)
        elif dst.is_symlink():
            pass
        else:
            # TODO: only sync changes.
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)
            logging.info('%s -> %s', src, dst)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('targets', type=Path, nargs='*',
                        help='project .md files to build / include in gallery.\n'
                             'if not given, includes all .md files in the projects directory.')
    parser.add_argument('--clean', action=argparse.BooleanOptionalAction, dest='should_clean', default=False, help='clean output directory before building')
    parser.add_argument('--project-pages', action=argparse.BooleanOptionalAction, dest='should_build_project_pages', default=True, help='build project pages')
    parser.add_argument('--piece-pages', action=argparse.BooleanOptionalAction, dest='should_build_piece_pages', default=True, help='build piece pages')
    parser.add_argument('--gallery', action=argparse.BooleanOptionalAction, dest='should_update_gallery', default=True, help='update project index and homepage')
    parser.add_argument('--sync-static', action=argparse.BooleanOptionalAction, dest='should_sync_static', default=False, help='copy/link static files to output')
    parser.add_argument('-v', '--verbose', action='count', dest='verbosity', default=0)
    parser.add_argument('-q', '--quiet', action='count', dest='quietness', default=0)
    args = parser.parse_args()
    log_level: int = 30 - 10 * (args.verbosity - args.quietness)
    targets: list[Path] = args.targets

    logging.getLogger().setLevel(log_level)

    if targets:
        projects = [Project.from_path(file) for file in targets if CONFIG.projects_dir in file.parents]
        pieces = [Piece.from_path(file) for file in targets if CONFIG.pieces_dir in file.parents]
        other = [file for file in targets if CONFIG.projects_dir not in file.parents and CONFIG.pieces_dir not in file.parents]
        if other:
            logging.warning('ignoring files outside of projects and pieces directories: %s', other)
    else:
        projects = [Project.from_path(file) for file in CONFIG.projects_dir.iterdir()]
        pieces = [Piece.from_path(file) for file in CONFIG.pieces_dir.iterdir()]

    if args.should_clean:
        shutil.rmtree(CONFIG.output_dir, ignore_errors=True)

    if args.should_build_project_pages:
        for project in projects:
            build_resource(project)
    if args.should_build_piece_pages:
        for piece in pieces:
            build_resource(piece)
    if args.should_update_gallery:
        build_resources_index(projects, kind=Project)
        build_resources_index(pieces, kind=Piece)
    if args.should_sync_static:
        for static_path in CONFIG.static_paths:
            sync_static_path(static_path)
    build_homepage()

if __name__ == '__main__':
    main()
