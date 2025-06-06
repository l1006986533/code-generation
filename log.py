class logger:
    def __init__(self, path='gpt.log'):
        self.logger = open(path, 'w')
        self.cache = ""

    def write(self, content):
        if isinstance(content, dict):
            for k, v in content.items():
                self.cache += str(f"{k}\n{v}\n")
                print(f"{k}\n{v}\n")
                self.logger.write(f"{k}\n{v}\n")
        elif isinstance(content, list):
            for item in content:
                self.cache += str(item)
                print(item)
                self.logger.write(str(item))
        else:
            self.cache += str(content)
            print(content)
            self.logger.write(str(content))


LOG = logger()


def get_logger():
    return LOG
