import logging
from types import SimpleNamespace

from status import Status
import re

logger = logging.getLogger(__name__)
pattern: str = "[A-Z|0-9]{6}"


class Story:
    """
    Object containing a story
    entities: list of records (1 entity = 1 line in JSON file)
    rp_document_id: story hash. Required to verify the record belongs to the same object
    document_record_count: expected records count for the story
    """
    entities = []
    rp_document_id: str
    document_record_count: int

    def __init__(self, record: SimpleNamespace):

        self.rp_document_id = record.RP_DOCUMENT_ID
        self.document_record_count = record.DOCUMENT_RECORD_COUNT
        self.entities = []
        self.add_record(record)

    def add_record(self, record: SimpleNamespace) -> None:
        """
        :param record: line in JSON file
        """
        if self.validate_record(record) == Status.CORRECTABLE_ERROR or self.validate_record(record) == Status.OK:
            self.entities.append(record)

    def validate_record(self, record: SimpleNamespace) -> Status:
        """
        Validates the record. Throws error to the log in case of failure.
        The following rules are applied:
        1. The 1-st record index should be 1.
        2. Document count for all the records relates to the same story should be the same.
        3. The records for the same object
            should come sequentially. So, the 1-st record index should be 1, next 2 and so on.
        :param record: line in JSON file
        :return: validation status
        """
        status = Status.OK
        if not (re.search(pattern, record.RP_ENTITY_ID)):
            logger.warning(f"Bad entity ID found: {record.RP_ENTITY_ID} ")

        if len(self.entities) != 0:
            if record.DOCUMENT_RECORD_COUNT != self.document_record_count:
                logger.warning(
                    f"Wrong document count! Expected: {self.document_record_count}, found: record.rp_document_count")
                status = Status.CORRECTABLE_ERROR
            if record.DOCUMENT_RECORD_INDEX != self.entities[-1].DOCUMENT_RECORD_INDEX + 1:
                logger.error(f"Missed record detected! Expected record index: "
                             f"{self.entities[-1].DOCUMENT_RECORD_INDEX + 1}, found: {record.DOCUMENT_RECORD_INDEX}")
                status = Status.UNCORRECTABLE_ERROR
        else:
            if record.DOCUMENT_RECORD_INDEX != 1:
                logger.error(f"Record {record.RP_ENTITY_ID} starting index is wrong! Expected: 1 "
                             f"found: {record.DOCUMENT_RECORD_INDEX}")
                status = Status.UNCORRECTABLE_ERROR
        return status

    def validate_integrity(self) -> None:
        """
        Checks the whole story. Throws error to the log in case of failure.
        The rules are:
        1. Records count should be exactly the same as the DOCUMENT_RECORD_COUNT.
        2. All the story is coming in one time. It's unacceptable that story starts in the middle of another story.
        :return: Nothing
        """
        if len(self.entities) != self.document_record_count:
            logger.error(f"Object {self.rp_document_id} is not complete: expected {self.document_record_count} records,"
                         f"found: {len(self.entities)}")
