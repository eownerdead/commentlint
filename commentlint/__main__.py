import argparse
import typing as T

import language_tool_python as langtool
from pygments import lexer, lexers, token


def main():
    args = parse_args()
    src = open(args.file).read()

    if args.lexer is None:
        lex = lexers.get_lexer_for_filename(args.file)
    else:
        lex = lexers.get_lexer_by_name(args.lexer)

    comments = extract_comment(src, lex)
    lt = langtool.LanguageTool('en-UK')
    for (idx, s) in comments:
        m = lt.check(s)
        for i in m:
            diagnostic(src, idx + i.offset, i.errorLength,
                       args.file, i.ruleId, i.message, i.replacements)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument('-l', '--lexer')
    p.add_argument('file')

    return p.parse_args()


def extract_comment(code: str,
                    lexer: lexer.Lexer) -> T.List[T.Tuple[int, str]]:
    return [(idx, s) for (idx, ty, s) in lexer.get_tokens_unprocessed(code)
            if ty in token.Comment]


def diagnostic(src: str, idx: int,
               lenght: int, file: str, id: str, msg: str, help: str):
    line = src[:idx].count('\n') + 1
    col = src[:idx][::-1].find('\n') + 1

    line_boarder = len(str(line))

    print(f'warning: {msg} ({id})')
    print(f' - {file}:{line}:{col}')
    print('{} |'.format(' ' * line_boarder))
    print(f'{line} | {src.splitlines()[line-1]}')
    print('{} | {}{} '
          .format(' ' * line_boarder, ' ' * (col - 1), '^' * lenght), end='')
    if len(help) != 0:
        print('help: {}'.format(', '.join(help)))
    print()


if __name__ == "__main__":
    main()
