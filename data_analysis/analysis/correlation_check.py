from db import Database

"""
    Takes the results from the value ratings for the hotels with 
    the lowest scores, calculates the total possible score for each
    catagory by travel type based on the number of reviews and stores
    a percent value for each category by travel type and location.
"""
class Correlation:
    def __init__(self, data: any, travel_type: str, location: int, rating: int):
        self._data = data
        self.travel_type = travel_type
        self.location_id = location
        self.rating = rating

    def _get_collective_rating(self, query: str, trip_id: str):
        with Database() as _db:
            result = _db.select_columns(query, trip_id)
        return result

    def get_ratings(self):
        result_dict = {}

        result_dict['travel_style'] = travel_type
        result_dict['location_id'] = location_id

        tmp_list = ['total_reviews', 'total_val', 'total_location',
                    'total_sleep', 'total_room', 'total_clean',
                    'total_service', 'total_checkin', 'total_business',
                    'avg_overall_rtng', 'total_overall_rtng']

        for tmp in tmp_list:
            result_dict[tmp] = 0

        for row in self._data:
            result_dict['total_reviews'] += 1
            (trip_id, review_id, tmp) = row
            print(trip_id)
            trip_id = str(trip_id)
            new_sql = "SELECT * FROM aspect_star_rating WHERE trip_id = %s"

            data = self._get_collective_rating(new_sql, trip_id)

            for ratings in data:
                (asr_id, trip_id, value,
                 location, sleep_qual, room,
                 clean, service, checkin,
                 bus_serv) = ratings

                result_dict['total_val'] += self.test_value(value)
                result_dict['total_location'] += self.test_value(location)
                result_dict['total_sleep'] += self.test_value(sleep_qual)
                result_dict['total_room'] += self.test_value(room)
                result_dict['total_clean'] += self.test_value(clean)
                result_dict['total_service'] += self.test_value(service)
                result_dict['total_checkin'] += self.test_value(checkin)
                result_dict['total_business'] += self.test_value(bus_serv)
                result_dict['total_overall_rtng'] += self.rating
        result_dict['avg_overall_rtng'] = result_dict['total_overall_rtng'] / result_dict['total_reviews']
        print(result_dict)
        return result_dict


    def test_value(self, value: any) -> int:
        if value:
            if isinstance(value, str):
                if value.isdigit():
                    value = int(value)
                else:
                    value = 0
            else:
                return value
        else:
            return 0


if __name__ == '__main__':

    sql = 'SELECT location_id, total_review, ' \
          '       rating, travel_type ' \
          'FROM tmp_rating_by_travel_type ' \
          'WHERE total_review > 50 ' \
          'ORDER BY total_review DESC, location_id;'

    location_id = ''
    total_review = ''
    rating = ''
    travel_type = ''

    with Database() as _db:
        data = _db.select(sql)

    for result in data:
        (location_id, total_review,
         rating, travel_type) = result
        print('Results for id: %s rating: %s travel type: %s' % (location_id, rating, travel_type))

        sql = """SELECT ti.trip_id,
                        tr.review_id,
                        tr.overall_rating
                FROM trip_info ti
                JOIN trip_review tr
                ON ti.trip_id = tr.trip_id
                WHERE tr.overall_rating <= %s
                    AND ti.location_id = %s
                    AND ti.travel_type = %s
                ORDER BY tr.overall_rating DESC, travel_type;"""

        with Database() as _db:
            data = _db.select_with_params(sql, [rating, location_id, travel_type])

        corr = Correlation(data, travel_type, location_id, rating)
        ratings_dict = corr.get_ratings()

        possible_score = int(ratings_dict['total_reviews']) * 5
        ignore_list = ['travel_style', 'total_reviews', 'location_id',
                       'avg_overall_rtng', 'total_overall_rtng']

        for k, v in ratings_dict.items():
            if k not in ignore_list:
                value = (int(v) / possible_score) * 100
                value = round(value, 2)
                ratings_dict[k] = value
        print(ratings_dict)

        colunms = ['location_id', 'travel_type', 'total_reviews', 'value_score',
                   'location_score', 'sleep_score', 'room_score', 'clean_score',
                   'service_score', 'checkin_score', 'business_score', 'avg_overall_rating',
                   'total_overall_rating']

        data = [ratings_dict['location_id'], ratings_dict['travel_style'], ratings_dict['total_reviews'],
                ratings_dict['total_val'], ratings_dict['total_location'], ratings_dict['total_sleep'],
                ratings_dict['total_room'], ratings_dict['total_clean'], ratings_dict['total_service'],
                ratings_dict['total_checkin'], ratings_dict['total_business'], ratings_dict['avg_overall_rtng'],
                ratings_dict['total_overall_rtng']]

        with Database() as _db:
            _db.insert_into_table('value_score', data, colunms)


