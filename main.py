from Lexer.lexer import Lexer
from Parser.parser import Parser
from StaticAnalysis.analyzer import StaticAnalyzer
from argparse import ArgumentParser


if __name__ == '__main__':

    description = 'testing for passing multiple arguments and to get list of args'
    parser = ArgumentParser(description=description)
    parser.add_argument('-r', '--rename', action='append', dest='rename_list',
                        type=str, nargs='*',
                        help="Examples: -r old_name new_name")
    parser.add_argument('-m', '--merge', action='append', dest='merge_list',
                        type=str, nargs='*',
                        help="Examples: -m class_name")
    parser.add_argument('-o', '--output_file', action='store',
                        default='out.txt', help='File to store the output')
    parser.add_argument('-i', '--input_file', action='store',
                        help='File to read from', required=True)
    opts = parser.parse_args()

    print("List of items: {}".format(opts))
    lexer = Lexer(opts.input_file)
    parser = Parser(lexer=lexer)
    analyzer = StaticAnalyzer(parser)
    if opts.rename_list:
        for rename in opts.rename_list:
            assert(len(rename) == 2)
            analyzer.change_class_name(rename[0], rename[1])
    if opts.merge_list:
        for merge in opts.merge_list:
            assert(len(merge) == 1)
            analyzer.merge_classes(merge[0])

    if not opts.merge_list and not opts.rename_list:
        analyzer.format()

    analyzer.save_file(file=opts.output_file)
