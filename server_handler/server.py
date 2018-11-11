import json
import logging
from db import Database


class ServerHandler:
    def __init__(self):
        self._db = Database()
        self._logger = logging.getLogger('FinalProjectApp')

    def get_states(self):
        with self._db as _db:
            query = """SELECT DISTINCT state FROM hotel_location
                       ORDER BY state ASC"""
            result = _db.select(query)
        self._logger.info("------->get_states: result=%s" % result)
        return result

    def get_locations(self, state: str):
        self._logger.info("------>get_locations for %s" % state)
        query = """SELECT location_id,
                          CONCAT(address1, ' ', 
                            address2, ' ',
                            city, ' ', 
                            state, ', ',
                            zip
                          )
                    FROM hotel_location
                    WHERE state = %s"""
        with self._db as _db:
            result = _db.select_with_params(query, [state])

        if result:
            return result

    def get_all_locations(self):
        self._logger.info("--------> get_all_locations")
        query = """SELECT location_id,
                          CONCAT(address1, ' ', 
                                    address2, ' ',
                                    city, ' ', 
                                    state, ', ',
                                    zip
                                  )
                    FROM hotel_location
                    ORDER BY state ASC"""

        with self._db as _db:
            result = _db.select(query)

        if result:
            return result

    def get_location_data(self, id: int, style: str):
        self._logger.info("------->get_location_data id: %s, style: %s" % (str(id), style))
        query = """SELECT 
                        CONCAT(l.address1, ', ',
                                l.address2),
                        CONCAT(l.city, ', ', l.state, ' ', l.zip) AS CSZ,
                        vs.total_reviews,
                        vs.value_score,
                        vs.location_score,
                        vs.sleep_score,
                        vs.room_score,
                        vs.clean_score,
                        vs.service_score,
                        vs.checkin_score,
                        vs.business_score,
                        vs.avg_overall_rating,
                        vs.total_overall_rating
                  FROM value_score vs
                  JOIN hotel_location l
                    ON vs.location_id = l.location_id
                  WHERE travel_type = %s
                    AND vs.location_id = %s
                  ORDER BY vs.location_id;"""

        with self._db as _db:
            result = _db.select_with_params(query, [style, id])

        if result:
            self._logger.info("------> result: %s" % result)
            return result
        else:
            self._logger.info("------> result: None Fount")
            return 'None Found'