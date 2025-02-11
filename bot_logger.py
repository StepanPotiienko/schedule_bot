import logging as log


class BotLogger:
    name: str = "LOG: "
    level: int = log.INFO

    logger = log.Logger(name=name, level=level)
    log.basicConfig(level=log.INFO)

    def write_to_file(self, data: str):
        with open("log.txt", "w") as file:
            file.write(self.name + data + "\n")

    def info(self, data: str):
        self.logger.info(data)
        print(self.name + data)
        self.write_to_file(data)

    def warning(self, data: str):
        self.logger.warning(data)
        print(self.name + data)
        self.write_to_file(data)

    def error(self, data: str):
        self.logger.error(data)
        print(self.name + data)
        self.write_to_file(data)
