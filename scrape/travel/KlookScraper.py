
import scrape.travel.KlookActivityListScraper as klook
import write.JsonFileWriter as json_writer
import logging
import utils.commonutils as utils
from pathlib import Path

PATH_OUT = Path("../../../../config/output")
logging.basicConfig(filename="logs.txt", format='%(asctime)s -%(levelname)s-%(message)s',
                    level=logging.INFO, filemode="a")


def main():
    results =klook.get_results()
    json_writer.write(PATH_OUT / ("KlookResults" + utils.current_datetime_str()), results)


if __name__ == "__main__":
    main()

