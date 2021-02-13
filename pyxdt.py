import subprocess
import functools
import itertools
import re


def hint_last(iterable):
    try:
        iterable = iter(iterable)
        a = next(iterable)
        for b in iterable:
            yield (a, False)
            a = b
        yield (a, True)
    except StopIteration:
        return


def findall_int(*args):
    return [int(n) for n in re.findall('\d+', str(args))]


def consume(iterable, function=int, all=False):
    return (list if(all) else next)(map(function, iterable))


class X11:
    def __init__(self):
        self.instructions = []
        self.modifiers = []
        self.parsers = []

    def clean(self):
        self.instructions = []
        self.modifiers = []
        self.parsers = []

        return self

    def run(self):
        self.outputs = []

        proc = subprocess.run(
                ['xdotool'] + list(itertools.chain(*self.instructions)),
                stdout=subprocess.PIPE,
                universal_newlines=True
        )

        self.stdout = proc.stdout
        self.stderr = proc.stderr
        self.status = proc.returncode

        if proc.returncode:
            return self.clean()

        it = iter(self.stdout.rstrip().split('\n'))
        xs = zip(self.instructions, self.parsers)

        for ((command, *_), parser), last in hint_last(xs):
            if (parser and not (command in self.modifiers and not last)):
                self.outputs.append(parser(it))

        return self.clean()

    def instruction(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            command = [function.__name__]
            for key, value in kwargs.items():
                command.append('--' + key)
                if value is True:
                    continue
                command.append(str(value))
            command.extend([str(x) for x in args])

            self.instructions.append(command)
            self.parsers.append(function(self, *args, **kwargs))

            return self
        return wrapper

    def windowstack_modifier(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            self.modifiers.append(function.__name__)

            return function(self, *args, **kwargs)
        return wrapper

# KEYBOARD COMMANDS

    @instruction
    def key(self, *args, **kwargs):
        pass

    @instruction
    def keydown(self, *args, **kwargs):
        pass

    @instruction
    def keyup(self, *args, **kwargs):
        pass

    @instruction
    def type(self, *args, **kwargs):
        pass

# MOUSE COMMANDS

    @instruction
    def mousemove(self, *args, **kwargs):
        pass

    @instruction
    def mousemove_relative(self, *args, **kwargs):
        pass

    @instruction
    def click(self, *args, **kwargs):
        pass

    @instruction
    def mousedown(self, *args, **kwargs):
        pass

    @instruction
    def mouseup(self, *args, **kwargs):
        pass

    @instruction
    def getmouselocation(self, *args, **kwargs):
        def parser(iterator):
            keys = ['x', 'y', 'screen', 'window']

            if ('shell' in kwargs):
                iterator = zip(*[iterator] * 4)

            return dict(zip(keys, findall_int(next(iterator))))
        return parser

    @instruction
    def behave_screen_edge(self, *args, **kwargs):
        pass

# WINDOW COMMANDS

    @instruction
    @windowstack_modifier
    def search(self, *args, **kwargs):
        def parser(iterator):
            return consume(iterator, all=True)
        return parser

    @instruction
    @windowstack_modifier
    def selectwindow(self, *args, **kwargs):
        return consume

    @instruction
    def behave(self, *args, **kwargs):
        pass

    @instruction
    def getwindowpid(self, *args, **kwargs):
        def parser(iterator):
            return consume(iterator, all='%@' in args)
        return parser

    @instruction
    def getwindowname(self, *args, **kwargs):
        def parser(iterator):
            return consume(iterator, str, all='%@' in args)
        return parser

    @instruction
    def getwindowgeometry(self, *args, **kwargs):
        def parser(iterator):
            if ('shell' in kwargs):
                iterator = zip(*[iterator] * 6)
                keys = ['window', 'x', 'y', 'width', 'height', 'screen']
            else:
                keys = ['window', 'x', 'y', 'screen', 'width', 'height']
                iterator = zip(*[iterator] * 3)

            iterator = (zip(keys, findall_int(xs)) for xs in iterator)

            return consume(iterator, dict, all='%@' in args)
        return parser

    @instruction
    @windowstack_modifier
    def getwindowfocus(self, *args, **kwargs):
        return consume

    @instruction
    def windowsize(self, *args, **kwargs):
        pass

    @instruction
    def windowfocus(self, *args, **kwargs):
        pass

    @instruction
    def windowmap(self, *args, **kwargs):
        pass

    @instruction
    def windowminimize(self, *args, **kwargs):
        pass

    @instruction
    def windowraise(self, *args, **kwargs):
        pass

    @instruction
    def windowreparent(self, *args, **kwargs):
        pass

    @instruction
    def windowclose(self, *args, **kwargs):
        pass

    @instruction
    def windowkill(self, *args, **kwargs):
        pass

    @instruction
    def windowunmap(self, *args, **kwargs):
        pass

    @instruction
    def set_window(self, *args, **kwargs):
        pass

# DESKTOP AND WINDOW COMMANDS

    @instruction
    def windowactivate(self, *args, **kwargs):
        pass

    @instruction
    @windowstack_modifier
    def getactivewindow(self, *args, **kwargs):
        return consume

    @instruction
    def set_num_desktops(self, *args, **kwargs):
        pass

    @instruction
    def get_num_desktops(self, *args, **kwargs):
        return consume

    @instruction
    def get_desktop_viewport(self, *args, **kwargs):
        def parser(iterator):
            if ('shell' in kwargs):
                iterator = zip(*[iterator] * 2)

            return dict(zip(['x', 'y'], findall_int(next(iterator))))
        return parser

    @instruction
    def set_desktop_viewport(self, *args, **kwargs):
        pass

    @instruction
    def set_desktop(self, *args, **kwargs):
        pass

    @instruction
    def get_desktop(self, *args, **kwargs):
        return consume

    @instruction
    def set_desktop_for_window(self, *args, **kwargs):
        pass

    @instruction
    def get_desktop_for_window(self, *args, **kwargs):
        return consume

# MISCELLANEOUS COMMANDS

    @instruction
    def exec(self, *args, **kwargs):
        pass

    @instruction
    def sleep(self, *args, **kwargs):
        pass
