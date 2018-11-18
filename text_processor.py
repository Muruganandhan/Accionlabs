import Queue
import re
import sys


class TextProcessor:
    queue = Queue.Queue()

    ASTERISK = "*"
    DOT = "."
    PATTERN = '(^[\\*\\.]+)'

    current_section = [0]

    def parse(self):

        s = sys.stdin.read()
        prefixes = re.findall(TextProcessor.PATTERN, s, re.MULTILINE)
        self.pre_processing(prefixes)
        indent = 0

        for line in s.split("\n"):

            # Skips empty lines
            if not line.strip():
                continue

            if line.startswith(TextProcessor.ASTERISK) or line.startswith(TextProcessor.DOT):
                prefix = self.queue.get()
                indent = len(prefix)
                sys.stdout.write(re.sub(TextProcessor.PATTERN, prefix, line))
            else:
                sys.stdout.write('{0} {1}'.format(' '*indent, line))
            sys.stdout.write('\n')

    def pre_processing(self, prefixes):
        for idx in range(0, len(prefixes)):
            prefix = prefixes[idx]
            if prefix.startswith(TextProcessor.ASTERISK):
                self.queue.put(self._build_sections(prefix))
            elif prefix.startswith(TextProcessor.DOT):
                try:
                    next_prefix = prefixes[idx + 1]
                except IndexError:
                    next_prefix = None
                self.queue.put(self._build_indent(prefix, next_prefix))

    def _build_indent(self, current, nxt=None):
        if current and nxt and nxt.startswith(TextProcessor.DOT):
            current_length = len(current)
            next_length = len(nxt)
            if current_length == next_length:
                return ' ' * (2 + current_length - 1) + '-'
            elif current_length < next_length:
                return ' ' * (2 + current_length - 1) + '+'

        if current:
            current_length = len(current)
            return ' ' * (2 + current_length - 1) + '-'

    def _build_sections(self, asterisks):
        count = len(asterisks)
        t = [0] * (count - 1)
        t.append(1)
        for i in range(count):
            try:
                t[i] = t[i] + self.current_section[i]
            except IndexError:
                pass
        self.current_section = t[:]
        return '.'.join(map(str, self.current_section))


if __name__ == '__main__':
    TextProcessor().parse()