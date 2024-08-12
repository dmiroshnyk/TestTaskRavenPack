import logging
import json
from types import SimpleNamespace

from story import Story


class FeedRecordProcessor:
    """
    path: contains path to the records file. Could be absolute or relative.
    """

    @staticmethod
    def process(path: str) -> int:
        logger = logging.getLogger(__name__)
        file = open(path, "r")
        entity: Story
        story_count = 0  # A variable to store the distinct number of processed stories (not records)

        i = 0

        prev_rp_document_id = None
        for line in file:
            try:
                record = json.loads(line, object_hook=lambda d: SimpleNamespace(**d))
                if record.RP_DOCUMENT_ID != prev_rp_document_id:  # That means another story was started
                    if prev_rp_document_id is not None:  # That means that is not the first story and we need to
                        # check the integrity of previous one
                        entity.validate_integrity()
                    entity = Story(record)
                    story_count += 1
                else:
                    entity.add_record(record)  # That means the record belongs to the same story
                prev_rp_document_id = record.RP_DOCUMENT_ID
                logger.debug(f"Processed line number {i}")
            except:
                logger.error(f"Can't process line number {i}, data: {line}")  # Bad JSON record format.
                # I assume the program should not try to process the broken file.
                # If it should - simply comment the raise on the next line
                raise
            finally:
                i += 1
        entity.validate_integrity()  # Check the last story
        return story_count
