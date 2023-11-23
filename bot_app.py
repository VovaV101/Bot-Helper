import json
from abc import ABC, abstractmethod
from bot_helper.bot import main as bot_main

class DataLoader(ABC):
    @abstractmethod
    def load_data(self, file_path):
        pass

class InformationPresenter(ABC):
    @abstractmethod
    def present_information(self, data_type, data):
        pass

class JSONDataLoader(DataLoader):
    def load_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return None

class UserInterface(ABC):
    @abstractmethod
    def show_information(self, information):
        pass

class ConsoleUserInterface(UserInterface):
    def show_information(self, information):
        print(information)

class ConsoleInformationPresenter(InformationPresenter):
    def present_information(self, data_type, data):
        if data:
            print(f"{data_type}:\n{json.dumps(data, indent=2)}")
        else:
            print(f"{data_type} is empty.")

class ExtendedBot:
    def __init__(self, information_presenters, data_loader):
        self.information_presenters = information_presenters
        self.data_loader = data_loader

    def run(self):
        # Load data from JSON files
        address_book_data = self.load_data('address_book.json')
        notes_data = self.load_data('notes_data.json')

        # Display different parts of the interface using the presenters
        for presenter in self.information_presenters:
            presenter.present_information("Address Book", address_book_data)
            presenter.present_information("Notes", notes_data)
            presenter.present_information("Available Commands", "help - all commands")

        # Run the main logic of the bot
        bot_main()

    def load_data(self, file_path):
        return self.data_loader.load_data(file_path)

if __name__ == "__main__":
    # Create instances of presenters for console interaction
    console_presenter = ConsoleInformationPresenter()

    # Create an instance of JSONDataLoader for data loading
    json_data_loader = JSONDataLoader()

    # Create a list of presenters to pass to ExtendedBot
    information_presenters = [console_presenter]

    # Create an instance of ExtendedBot with the list of presenters and JSON data loader
    extended_bot = ExtendedBot(information_presenters, json_data_loader)

    # Run your extended bot
    extended_bot.run()