from collections import Counter


class InstanceCounter:
    def __init__(self, db: any, sql: str, params: any):
        self._db = db
        self._sql = sql
        self._query_params = params
        self.include = ['SMELL', 'LOUD', 'POOR', 'BAD', 'RUDE', 'UNCOMFORTABLE',
                        'STUPID', 'UGLY', 'ANNOYING', 'GROSS', 'STINKY', 'COLD',
                        'HOT', 'MEAN', 'BROKEN', 'BROKE', 'SMELLY', 'LATE', 'EXPENSIVE',
                        'POOR', 'DUMB', 'ANGRY', 'FAULTY', 'TOUGH', 'HARD']

    def _get_data(self) -> any:
        return self._db.select_with_params(self._sql, self._query_params)

    def find_most_common(self) -> any:
        combined_review = """"""
        data = self._get_data()
        for value in data:
            (trip_id, review_id,
             review_content, overall_rating) = value
            combined_review = combined_review + ' ' + review_content
        split_msg = combined_review.split()
        counter = Counter(word for word in split_msg if word.upper() in self.include)
        most_common = counter.most_common(6)
        print(most_common)

        return most_common


if __name__ == '__main__':
    from db import Database

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
                        tr.review_content, 
                        tr.overall_rating 
                 FROM trip_info ti 
                 JOIN trip_review tr 
                    ON ti.trip_id = tr.trip_id 
                 WHERE tr.overall_rating <= %s 
                    AND ti.location_id = %s
                    AND ti.travel_type = %s  
                 ORDER BY tr.overall_rating DESC, travel_type;"""

        _db = Database()
        counter = InstanceCounter(_db, sql, [rating, location_id, travel_type])
        most_common = counter.find_most_common()
        print(most_common)
