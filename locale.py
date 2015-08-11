class Locale:
    def __init__(self):
        self.strings = []
        locale = open("main.locale", "r").read().split('\n')[0]
        f = open(locale, "r").read().decode('string-escape').decode("utf-8").split('\n')
        for i in f:
            if len(i) == 0:
                continue
            self.strings.append(i)

    def get(self, i):
        return self.strings[i]