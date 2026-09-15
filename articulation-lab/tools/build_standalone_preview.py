#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import mimetypes
import re
from pathlib import Path

STYLE_RE = re.compile(r'<link\s+rel="stylesheet"\s+href="([^"]+)"\s*/?>')
SCRIPT_RE = re.compile(r'<script\s+src="([^"]+)"></script>')
AUDIO_RE = re.compile(r'(?P<q>[\'\"])(assets/audio/real/[^\'\"]+\.wav)(?P=q)')


def encode_audio(app_dir: Path, js: str) -> str:
    cache: dict[str, str] = {}

    def repl(match: re.Match[str]) -> str:
        rel = match.group(2)
        if rel not in cache:
            path = app_dir / rel
            if not path.exists():
                raise FileNotFoundError(f"Missing audio asset referenced by presets: {rel}")
            mime = mimetypes.guess_type(path.name)[0] or 'audio/wav'
            payload = base64.b64encode(path.read_bytes()).decode('ascii')
            cache[rel] = f'data:{mime};base64,{payload}'
        q = match.group('q')
        return f'{q}{cache[rel]}{q}'

    return AUDIO_RE.sub(repl, js)


def build(app_dir: Path, output: Path) -> None:
    index_path = app_dir / 'index.html'
    html = index_path.read_text(encoding='utf-8')

    style_paths = STYLE_RE.findall(html)
    if not style_paths:
        raise RuntimeError('No stylesheet link found in index.html')
    for rel in style_paths:
        css = (app_dir / rel).read_text(encoding='utf-8')
        html = html.replace(
            f'<link rel="stylesheet" href="{rel}" />',
            f'<style data-source="{rel}">\n{css}\n</style>'
        )
        html = html.replace(
            f'<link rel="stylesheet" href="{rel}">',
            f'<style data-source="{rel}">\n{css}\n</style>'
        )

    script_paths = SCRIPT_RE.findall(html)
    if not script_paths:
        raise RuntimeError('No external scripts found in index.html')

    for rel in script_paths:
        js = (app_dir / rel).read_text(encoding='utf-8')
        if rel.endswith('data/vowel-presets.js'):
            js = encode_audio(app_dir, js)
        html = html.replace(
            f'<script src="{rel}"></script>',
            f'<script data-source="{rel}">\n{js}\n</script>'
        )

    if 'src="' in html or 'href="styles/' in html:
        raise RuntimeError('Standalone build still contains external local dependencies')
    if 'assets/audio/real/' in html:
        raise RuntimeError('Standalone build still contains unembedded real-audio paths')

    banner = '<!-- Articulation Lab v0.4 standalone build: local CSS/JS and vetted real-voice WAVs are embedded. -->\n'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(banner + html, encoding='utf-8')
    print(f'Wrote {output} ({output.stat().st_size} bytes)')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-dir', type=Path, default=Path('articulation-lab'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build(args.app_dir, args.output)


if __name__ == '__main__':
    main()
