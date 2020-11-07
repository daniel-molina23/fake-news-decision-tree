
class TitleHandler:
    def __init__(self, title):
        self.title = title
        self.data = {} # dictionary
    def execute(self):
        self.extractCapitals()
        return self.data

    def extractCapitals(self):
        count = 0
        if isinstance(self.title, str):
            for char in self.title:
                if char.isupper():
                    count+=1
            self.data['title_capital_freq'] = count
        else:
            self.data['title_capital_freq'] = count
            