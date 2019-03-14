import argparse
import sys


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        print('error: %s\n' % message, file=sys.stderr)
        self.print_help()
        sys.exit(1)
