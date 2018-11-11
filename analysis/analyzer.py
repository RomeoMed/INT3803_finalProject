from nltk.sentiment.vader import SentimentIntensityAnalyzer

"""
    The analyzer class uses nltk to perform sentiment analysis on the 
    review messages.
"""


class Analyzer:
    def __init__(self, trip_id: int, message: str, db: any, logger: any):
        self._trip_id = trip_id
        self._review_message = message
        self._db = db
        self._logger = logger
        self._sid = SentimentIntensityAnalyzer()

    def get_scores(self) -> any:
        """
        Gets the polarity scores for the review message
        :return: void on success, the trip ID on failure
        """
        try:
            scores = self._sid.polarity_scores(self._review_message)
            self._store_scores(scores)
        except Exception as e:
            self._logger.info('ERROR------>Unable to get scores for %s, error: %s' % (self._trip_id, e))
            return self._trip_id

    def _store_scores(self, scores: any) -> None:
        """
        Stores the scores in the database
        :return: void
        """
        compound = None
        negative = None
        neutral = None
        positive = None

        for k,v in scores.items():
            if k == 'compound':
                compound = v
            elif k == 'pos':
              positive = v
            elif k == 'neg':
                negative = v
            elif k == 'neu':
                neutral = v

        sql = 'sentiments (trip_id, overall_score, neg_score, neut_score, pos_score) values (%s, %s,%s,%s,%s)'
        self._db.insert_into(sql, [self._trip_id, compound, negative, neutral, positive])
