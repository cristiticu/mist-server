from licenses.model import License
from shared.persistence.file_repository import FileRepository


class LicensesPersistence(FileRepository[License]):
    def __init__(self, *, filepath: str, persist_contents: bool = False):
        super().__init__(filepath=filepath, persist_contents=persist_contents,
                         factory=lambda dict: License(**dict))
