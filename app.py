import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, flash, request, jsonify
from server_handler.server import ServerHandler


logPath = r'log\log.log'
# Set the name of the object we are logging for
_logger = logging.getLogger("FinalProjectApp")
_logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(logPath, maxBytes=20971520, backupCount=10)
# Format the log message to display the time, object name, the logging level, and the message.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
_logger.addHandler(handler)

app = Flask(__name__)
request_handler = ServerHandler()

"""Flask Framework methods to handle routing between the different pages"""


@app.route("/")
def index():
    _logger.info('Request for Home Page.')
    return render_template('index.html')


@app.route('/get_states', methods=['GET'])
def get_states():
    _logger.info('/get_states request --processing data.')
    try:
        # Get the states for the dropdown menu
        states = request_handler.get_states()
        if states:
            # return as json object
            return jsonify(states)

    except Exception as e:
        _logger.info('Error processing data: %s' % str(e))
        flash('Something Went Terribly Wrong!')
        return render_template('error.html')


@app.route('/get_locations_data', methods=['GET'])
def get_locations_data():
    _logger.info('/get_locations_data --processing request')
    # Get the request parameter
    state = request.args.get('state')
    try:
        result = request_handler.get_location_data(state)
        if 'None Found' not in result:
            for res in result:
                total_score = 0
                max_score = 0
                possible_score = res['possible_score']
                for k, v in res.items():
                    if k == 'address':
                        res[k] = v + ' ' + res['csz']
                    if k != 'address' and k != 'csz' and k != 'total_reviews' and k != 'possible_score':
                        # Calculate the total score for each category, calculate the total possible
                        # score based on reviews num or reviews * 5
                        # calculate score percentage for each category.
                        total_score += v
                        max_score += possible_score
                        tmp = round((v / possible_score), 2) * 100
                        res[k] = '%.1f' % tmp + '%'
                if total_score and possible_score:
                    overall = round((total_score/max_score), 2) * 100
                    overall = '%.1f' % overall
                    res['overall'] = "{0}%".format(overall)
                else:
                    res['overall'] = '--%'
            return jsonify(result)
        else:
            return jsonify({'error': 'No trips for selected location & travel_type'})
    except Exception as e:
        _logger.info('ERROR-------> %s' % e)


@app.route('/get_dashboard_select', methods=['GET'])
def getDashboardSelect():
    _logger.info('/getDashboardSelect --processing request')
    state_obj = {}
    try:
        result = request_handler.get_all_locations()
        if result:
            for res in result:
                state_obj[res[0]] = res[1]
            return jsonify(state_obj)
    except Exception as e:
        _logger.info('ERROR--------> %s' % e)


@app.route('/get_panel_data', methods=['GET'])
def get_panel_data():
    # get query parameters
    location_id = request.args.get('id')
    _logger.info('/get_panel_data for: %s' % location_id)
    try:
        result = request_handler.get_panel_data(location_id)
        if result:
            return jsonify(result)
    except Exception as e:
        _logger.info('ERROR--------> %s' % e)


@app.route('/get_travel_style_analysis', methods=['GET'])
def get_travel_style_analysis():
    location_id = request.args.get('id')
    _logger.info('/get_travel_style_analysis --processing request')
    try:
        result = request_handler.get_travel_style_analysis(location_id)
        if result:
            return jsonify(result)
    except Exception as e:
        _logger.info('ERROR--------> %s' % e)


@app.route('/get_doughnut_chart', methods=['GET'])
def get_doughnut_char():
    location_id = request.args.get('id')
    _logger.info('/get_doughnut_chart --processing request')
    try:
        result = request_handler.get_doughnut(location_id)
        if result:
            return jsonify(result)
    except Exception as e:
        _logger.info('ERROR--------> %s' % e)


@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    location_id = request.args.get('id')
    _logger.info('/get_reviews for: %s' % location_id)
    try:
        result = request_handler.get_reviews(location_id)
        if result:
            return jsonify(result)
    except Exception as e:
        _logger.info('ERROR--------> %s' % e)


if __name__ == '__main__':
    _logger.info('Server is Listening.....')
    app.run(debug=True)
