import sys
import logging
import os.path

from src.feed_record_processor import FeedRecordProcessor

def main():
    logging.basicConfig(filename='log.log', level=logging.INFO, filemode='w')
    logger = logging.getLogger(__name__)

    argument_list = sys.argv[1:]
    if len(argument_list) != 1:
        logger.fatal(f"Application should take exactly 1 parameter (path to file with records),"
                     f" found: {len(argument_list)}")
        exit(1)

    story_count = FeedRecordProcessor.process(sys.argv[1])
    logger.info(f"Total stories count: {story_count}")


if __name__ == "__main__":
    main()
