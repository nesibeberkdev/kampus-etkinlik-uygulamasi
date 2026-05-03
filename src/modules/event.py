class Event:
    """
    Sistemdeki etkinlikleri temsil eder.
    """

    def __init__(self, id, title, description, date, location):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.location = location

    def get_event_info(self):
        return f"{self.title} - {self.date} - {self.location}"