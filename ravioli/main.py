import sys
from pathlib import Path

from ravioli import c_parser
from ravioli.line_counter import LineCounter

if __name__ == "__main__":
    folder = Path('../motobox')

    if len(sys.argv) > 1:
        folder = Path(sys.argv[1])

    # Find all the source files.
    source_files = list(folder.glob('**/*.c'))

    # Find all the subfolder paths within this directory. We'll pass all of them to preprocessor, so that we
    # most likely can find all of our include files.
    paths = list(folder.glob('**/'))
    paths = [str(path) for path in paths if path.is_dir()]

    print(f"Found {len(source_files)} source files...")

    for f in source_files:
        print(f"   {str(f)}")
        try:
            results = c_parser.parse(str(f), paths)
            loc = LineCounter.count_file(f)
            max_scc = max(results['complexity'].values())
            sf = max_scc + (5*results['global_count']) + (loc // 20)
            print(f"SLOC: {loc}, SCC: {max_scc}, Globals: {results['global_count']}, SF: {sf}")
        except:
            print("   Unable to parse")

    # with open("../motobox/Sources/can.c", 'r') as f:
    #     pprint(find_functions(f.read()))
