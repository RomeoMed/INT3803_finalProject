import logging
import os
from logging.handlers import RotatingFileHandler
from store_data import DataHandler

logPath = r'log\main.log'
# Set the name of the object we are logging for
_logger = logging.getLogger("Project3803")
_logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=20971520, backupCount=10)
# Format the log message to display the time, object name, the logging level, and the message.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
_logger.addHandler(handler)


def main():
    data_dir = 'data_cleanser'
    files = ['tourist.csv', 'trip_info.csv', 'travel_style.csv', 'trip_coll_badge.csv',
             'aspect_star_rating.csv', 'trip_review.csv']

    try:
        for file in files:
            file_path = os.path.join(data_dir, file)
            table_name = get_table_name(file)
            table_cols = get_table_cols(table_name)
            _logger.info('Getting ready to import %s in Table %s' % (file, table_name))

            importer = DataHandler(file_path, table_name, table_cols)
            total_imported = importer.store_data()

            _logger.info('Total rows imported = %s' % str(total_imported))

    except Exception as e:
        _logger.info('ERROR---------->%s' % e)


def get_table_name(file: str) -> str:
    """
    Gets the table name based on the file name.
    :param file:
    :return:
    """
    if file == 'updated_location.csv':
        return 'hotel_location'
    elif file == 'tourist.csv':
        return 'tourist'
    elif file == 'trip_info.csv':
        return 'trip_info'
    elif file == 'travel_style.csv':
        return 'trip_travel_style'
    elif file == 'trip_coll_badge.csv':
        return 'trip_collective_badge'
    elif file == 'aspect_star_rating.csv':
        return 'aspect_star_rating'
    elif file == 'trip_review.csv':
        return 'trip_review'


def get_table_cols(table_name: str) -> any:
    """
    Gets the column names for the tables that have auto_incremented pks
    :param table_name: the input file
    :return: a list of column names
    """
    if table_name == 'trip_travel_style':
        return ['trip_id','beach_goer','like_a_local','history_buff','urban_explorer',
                'thrifty_traveler','no_travel_style','foodie','nature_lover','luxury_traveler',
                'quiet_seeker','art_architec_lover','family_vacationer','trendsetter','thrill_seeker','nightlife_seeker','vegetarian','sixty_plus','shopping_fan',
                'backpacker','eco_tourist']
    elif table_name == 'trip_collective_badge':
        return ['trip_id', 'rev_reviews', 'new_rev_reviews', 'helpful_rev_votes', 'readership_readers_num',
                'hotel_exp_level', 'resort_exp_level', 'attr_exp_level', 'senior_rev_reviews', 'contributor_reviews',
                'passport_cities', 'restaurant_exp_level', 'explorer_reviews', 'senoir_contrib_level',
                'new_photographer', 'lux_h_expert_level', 'top_contrib_reviews', '2015_trav_choice', 'beg_photos',
                'junior_photos', 'photographer', 'senior_photographer', 'expert_photographer', 'top_photographer',
                'bb_and_inn_expert', '2016_h_expert', 'botique_h_expert', '2015_att_expert']
    elif table_name == 'aspect_star_rating':
        return ['trip_id', 'value_rating', 'location_rating', 'sleep_qual_rating', 'rooms_raiting',
                'cleanliness_raiting', 'service_rating', 'checkin_raiting', 'buss_srvc_raiting']
    elif table_name == 'trip_review':
        return ['trip_id', 'review_title', 'review_content', 'overall_rating']
    else:
        return None


if __name__ == '__main__':
    main()