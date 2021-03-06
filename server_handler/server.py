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

    def get_location_data(self, state: str):
        self._logger.info("------->get_location_data state: {0}".format(state))
        query = """SELECT 
                        CONCAT(l.address1, ', ',
                                l.address2),
                        CONCAT(l.city, ' ', l.state, ', ', l.zip) AS CSZ,
                        ts.total_reviews, ts.possible_score, ts.value,
                        ts.location, ts.sleep, ts.room,
                        ts.clean, ts.service, ts.checkin,
                        ts.business
                  FROM total_rating_scores ts
                  JOIN hotel_location l
                    ON ts.location_id = l.location_id
                  WHERE l.state = %s
                  ORDER BY ts.location_id"""

        with self._db as _db:
            result = _db.select_with_params(query, [state])

        if result:
            return_obj = []
            for res in result:
                tmp_obj = {
                    'address': res[0],
                    'csz': res[1],
                    'total_reviews': res[2],
                    'possible_score': res[3] or 0,
                    'value': res[4] or 0,
                    'location': res[5] or 0,
                    'sleep': res[6] or 0,
                    'room': res[7] or 0,
                    'clean': res[8] or 0,
                    'service': res[9] or 0,
                    'checkin': res[10] or 0,
                    'business': res[11] or 0
                }
                return_obj.append(tmp_obj)

            return return_obj
        else:
            self._logger.info("------> result: None Found")
            return 'None Found'

    def get_panel_data(self, id_num: any):
        return_obj = {}

        self._logger.info("-------->get_panel_data")
        query = """SELECT COUNT(*) AS total_reviews
                    FROM trip_info
                    WHERE location_id = %s"""

        query1 = """SELECT COUNT(*), overall_rating FROM trip_review tr
                    JOIN trip_info 
                        ON trip_info.trip_id = tr.trip_id
                    WHERE location_id = %s
                    GROUP BY overall_rating;"""

        query2 = """ SELECT possible_score,
                            value,
                            location,
                            sleep,
                            room,
                            clean,
                            service,
                            checkin,
                            business
                    FROM total_rating_scores
                    WHERE location_id = %s;
                    """

        with self._db as _db:
            total_revs = _db.select_with_params(query, [id_num])
            rating_groups = _db.select_with_params(query1, [id_num])
            total_scores = _db.select_with_params(query2, [id_num])

        return_obj['total_reviews'] = total_revs[0][0] or 0
        if rating_groups and total_scores:
            pos_total, neg_total = self._get_metrics(rating_groups)

            return_obj['pos_total'] = pos_total
            return_obj['neg_total'] = neg_total
            return_obj['possible_score'] = total_scores[0][0] or 0
            return_obj['value'] = round(float(total_scores[0][1] or 0), 2)
            return_obj['location'] = round(float(total_scores[0][2] or 0), 2)
            return_obj['sleep'] = round(float(total_scores[0][3] or 0), 2)
            return_obj['room'] = round(float(total_scores[0][4] or 0), 2)
            return_obj['clean'] = round(float(total_scores[0][5] or 0), 2)
            return_obj['service'] = round(float(total_scores[0][6] or 0), 2)
            return_obj['checkin'] = round(float(total_scores[0][7] or 0), 2)
            return_obj['business'] = round(float(total_scores[0][8] or 0), 2)

        return return_obj

    def _get_metrics(self, data: any):
        total_pos = 0
        total_neg = 0

        for item in data:
            count = item[0] or 0
            rating = item[1] or 0

            if rating <= 3:
                total_neg += count
            else:
                total_pos += count
        return total_pos, total_neg

    def get_travel_style_analysis(self, id_num: str):
        self._logger.info('get_treval_style_analysis for id: {0}'.format(id_num))
        query = """                 
                    SELECT travel_type,
                        SUM(rating) / COUNT(rating) AS avg_rating
                    FROM tmp_rating_by_travel_type
                    WHERE location_id = %s
                    GROUP BY travel_type;
                """

        with self._db as _db:
            result = _db.select_with_params(query, [id_num])

        if result:
            return_obj = {}
            for res in result:
                if res[0] == 'No filling in':
                    travel_style = 'Unknown'
                else:
                    travel_style = res[0]
                value = round(float(res[1] or 0), 2)

                return_obj[travel_style] = value

            return return_obj

    def get_doughnut(self, loc_id: str):
        self._logger.info('get_doughnut id: {0}'.format(loc_id))
        query = """
                    SELECT 
                        avg_overall_score,
                        avg_neg_score,
                        avg_neut_score,
                        avg_pos_score
                    FROM avg_sentiment_analysis
                    WHERE location_id = %s;
                """

        with self._db as _db:
            result = _db.select_with_params(query, [loc_id])

        if result:
            return_obj = {
                'neg_score': round(float(result[0][1] or 0), 2),
                'neut_score': round(float(result[0][2] or 0), 2),
                'pos_score': round(float(result[0][3] or 0), 2),
                'overall': round(float(result[0][0] or 0), 2)
            }
            return return_obj


    def get_reviews(self, location_id: str):
        self._logger.info('get_reviews for {0}'.format(location_id))
        query = """
                    SELECT 	
                        tr.review_content AS content
                    FROM trip_review tr
                    JOIN trip_info ti
                        ON ti.trip_id = tr.trip_id
                    WHERE ti.location_id = %s
                    LIMIT 10;
                """
        with self._db as _db:
            result = _db.select_with_params(query, (location_id,))

        if result:
            index = 0
            return_obj = {}
            for res in result:
                return_obj[index] = res[0]
                index += 1
            return return_obj
