class LockerItem:
    def __init__(self, filename, filedata):
        self.filename = filename
        self.filedata = filedata

    def get_file_info(self):
        return self.filename
