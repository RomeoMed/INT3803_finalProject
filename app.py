import re
import datetime
import logging
from lib import helpers
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
    # returns the main registration page.
    return render_template('index.html')


@app.route('/get_states', methods=['GET'])
def get_states():
    _logger.info('/get_states request --processing data.')
    try:
        states = request_handler.get_states()
        if states:
            return jsonify(states)

    except Exception as e:
        _logger.info('Error processing data: %s' % str(e))
        flash('Something Went Terribly Wrong!')
        return render_template('error.html')

@app.route('/get_locations_by_state', methods=['GET'])
def get_locations():
    _logger.info("/get_locations_by_state --processing")
    state = request.args.get('state')
    state_obj = {}
    try:
        result = request_handler.get_locations(state)
        if result:
            for res in result:
                state_obj[res[0]] = res[1]
            return jsonify(state_obj)
    except Exception as e:
        _logger.info('ERROR---------> %s' % e)


@app.route('/get_locations_data', methods=['GET'])
def get_locations_data():
    _logger.info('/get_locations_data --processing request')
    id = request.args.get('location_id')
    style = request.args.get('travel_style')
    response = []
    try:
        result = request_handler.get_location_data(id, style)
        if 'None Found' not in result:
            converter = helpers.ConvertDecimalToString()
            for res in result:
                overall = (res[12] / (res[2] * 5)) * 100
                round(overall, 2)
                tmp_obj = {
                    'address': res[0],
                    'csz': res[1],
                    'total_reviews': res[2],
                    'value': '{0}%'.format(converter.process(res[3])),
                    'location': '{0}%'.format(converter.process(res[4])),
                    'sleep': '{0}%'.format(converter.process(res[5])),
                    'room': '{0}%'.format(converter.process(res[6])),
                    'clean': '{0}%'.format(converter.process(res[7])),
                    'service': '{0}%'.format(converter.process(res[8])),
                    'checkin': '{0}%'.format(converter.process(res[9])),
                    'business': '{0}%'.format(converter.process(res[10])),
                    'overall': res[11],
                    'total_overall': '{0:.2f}%'.format(round(overall, 2))
                }

                response.append(tmp_obj)

            return jsonify(response)
        else:
            return jsonify({'error' : 'No trips for selected location & travel_type'})
    except Exception as e:
        _logger.info('ERROR-------> %s' % e)

@app.route('/get_dashboard_select', methods=['GET'])
# Handler for the admin/reports page. Gets the data from the DB, and
# returns it to a table in the html file.
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
# Handler for the admin/reports page. Gets the data from the DB, and
# returns it to a table in the html file.
def get_panel_data():
    location_id = request.args.get('id')
    _logger.info('/get_panel_data for: %s' % location_id)
    res_obj = {}
    try:
        result = request_handler.get_panel_data(location_id)
        if result:
            return jsonify(result)
    except Exception as e:
        _logger.info('ERROR--------> %s' % e)


if __name__ == '__main__':
    _logger.info('Server is Listening.....')
    app.run(debug=True)
