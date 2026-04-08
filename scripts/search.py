#!/usr/bin/env python3
"""행정안전부 공통표준용어 검색 스크립트 (확장형).

다중 사전 지원:
  1. references/*.csv 자동 탐지 (행안부 표준 + 프로젝트 자체 약어)
  2. --csv로 외부 경로 추가 가능

Usage:
    python search.py <keyword> [--top N] [--csv PATH ...] [--no-default] [--exact]

Examples:
    python search.py 회원
    python search.py 게시물 --top 10
    python search.py 돌봄 --csv /path/to/new_standard.csv
    python search.py 회원 --no-default --csv /other/custom.csv
"""
import csv, sys, argparse, os, glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REF_DIR = os.path.join(SCRIPT_DIR, '..', 'references')

NAME_COLS = ['공통표준용어명','공통표준단어명','용어명','단어명','name']
ABBR_COLS = ['공통표준용어영문약어명','공통표준단어영문약어명','영문약어명','abbr']
DOMAIN_COLS = ['공통표준도메인명','도메인명','domain']
DESC_COLS = ['공통표준용어설명','공통표준단어설명','설명','description']

def find_col(row, candidates):
    for c in candidates:
        if c in row and row[c]:
            return row[c]
    return ''

def discover_csvs():
    return sorted(glob.glob(os.path.join(REF_DIR, '*.csv')))

def search(keyword, csv_paths, top=10, exact=False):
    results = []
    for csv_path in csv_paths:
        src = os.path.basename(csv_path)
        try:
            with open(csv_path, encoding='utf-8-sig', newline='') as f:
                for row in csv.DictReader(f):
                    name = find_col(row, NAME_COLS)
                    abbr = find_col(row, ABBR_COLS)
                    if not name or not abbr:
                        continue
                    if exact and keyword != name:
                        continue
                    if not exact and keyword not in name:
                        continue
                    results.append({
                        'name': name, 'abbr': abbr,
                        'domain': find_col(row, DOMAIN_COLS),
                        'desc': find_col(row, DESC_COLS)[:80],
                        'source': row.get('출처', src),
                        'len': len(name),
                    })
        except FileNotFoundError:
            print(f'⚠ CSV not found: {csv_path}', file=sys.stderr)
        except Exception as e:
            print(f'⚠ Error reading {csv_path}: {e}', file=sys.stderr)

    results.sort(key=lambda x: (x['len'], x['source']))
    seen, deduped = set(), []
    for r in results:
        if r['abbr'] not in seen:
            seen.add(r['abbr'])
            deduped.append(r)
    return deduped[:top]

def main():
    p = argparse.ArgumentParser(description='행안부 공통표준용어 검색 (확장형)')
    p.add_argument('keyword')
    p.add_argument('--top', type=int, default=10)
    p.add_argument('--csv', nargs='+', default=[])
    p.add_argument('--no-default', action='store_true')
    p.add_argument('--exact', action='store_true')
    args = p.parse_args()

    csv_paths = [] if args.no_default else discover_csvs()
    csv_paths.extend(args.csv)
    if not csv_paths:
        print('❌ 검색할 CSV 없음', file=sys.stderr); sys.exit(1)

    print(f'📂 검색 대상: {len(csv_paths)}개 CSV', file=sys.stderr)
    for cp in csv_paths:
        print(f'   - {os.path.basename(cp)}', file=sys.stderr)
    print(file=sys.stderr)

    results = search(args.keyword, csv_paths, args.top, args.exact)
    if not results:
        print(f'"{args.keyword}" 결과 없음'); sys.exit(0)

    print(f'{"용어명":<20} {"약어":<25} {"도메인":<15} {"출처":<30} 설명')
    print('-' * 120)
    for r in results:
        print(f'{r["name"]:<20} {r["abbr"]:<25} {r["domain"]:<15} {r["source"]:<30} {r["desc"]}')

if __name__ == '__main__':
    main()
