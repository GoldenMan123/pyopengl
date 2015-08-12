class Locale:
    '''
    Class Locale loads strings for current locale written in 'main.locale' file
    '''
    def __init__(self):
        '''
        Initialize Locale
        @return:
        '''
        self.strings = []
        # Read current locale from 'main.locale'
        locale = open("main.locale", "r").read().split('\n')[0]
        # Read string from current locale
        f = open(locale, "r").read().decode('string-escape').decode("utf-8").split('\n')
        for i in f:
            if len(i) == 0:
                continue
            self.strings.append(i)

    def get(self, i):
        '''
        Get i-th string from locale
        @param i: index of string
        @return: i-th string
        '''
        return self.strings[i]