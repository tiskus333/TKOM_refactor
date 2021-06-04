from Lexer.lexer import Lexer
from Parser.parser import Parser
from StaticAnalysis.analyzer import StaticAnalyzer
from argparse import ArgumentParser


if __name__ == '__main__':

    description = 'testing for passing multiple arguments and to get list of args'
    parser = ArgumentParser(description=description)
    parser.add_argument('-r', '--rename', action='append', dest='rename_list',
                        type=str, nargs='*',
                        help="Examples: -r scope old_name new_name")
    parser.add_argument('-m', '--merge', action='append', dest='merge_list',
                        type=str, nargs='*',
                        help="Examples: -m scope class_name")
    parser.add_argument('-o', '--output_file', action='store',
                        default='out.txt', help='File to store the output')
    parser.add_argument('-i', '--input_file', action='store',
                        help='File to read from', default='my_code.txt')
    opts = parser.parse_args()

    print("List of items: {}".format(opts))
    lexer = Lexer(opts.input_file)
    parser = Parser(lexer=lexer)
    analyzer = StaticAnalyzer(parser)

    if opts.rename_list:
        for rename in opts.rename_list:
            analyzer.change_class_name(rename[0], rename[1], rename[2])
    if opts.merge_list:
        for merge in opts.merge_list:
            analyzer.merge_classes(merge[0], merge[1])

    analyzer.traverse(parser.AST)
    analyzer.save_file(file=opts.output_file)
