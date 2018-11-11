import logging
from db import Database
from data_analysis.analysis import Analyzer
from logging.handlers import RotatingFileHandler

def main():
    logPath = r'log\analysis.log'
    # Set the name of the object we are logging for
    _logger = logging.getLogger("Project3803_Analysis")
    _logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(logPath, maxBytes=20971520, backupCount=10)
    # Format the log message to display the time, object name, the logging level, and the message.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

    table = 'trip_review'
    data_id = 1
    failed_ids = []

    with Database() as _db:
        while data_id <= 634277:
            sql = '%s WHERE trip_id = %s' % (table, str(data_id))
            result = _db.select_from(sql)
            if not result or result == 0:
                failed_ids.append(data_id)
            else:
                message = result[0][3]
                if message:
                    analyzer = Analyzer(data_id, message, _db, _logger)
                    optional_id = analyzer.get_scores()
                    if optional_id:
                        failed_ids.append(optional_id)
                else:
                    failed_ids.append(data_id)
                    _logger.info('No message for trip_id: %s' % data_id)

            data_id += 1

    if failed_ids:
        for ids in failed_ids:
            _logger.info('failed id ------>%s' % ids)


if __name__ == '__main__':
    main()
