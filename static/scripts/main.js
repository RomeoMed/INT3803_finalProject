$(document).ready(function(){
    var barChart = null;
    var ratingChart = null;
    var doughnutChart = null;
    var slideIndex;

    $('#value_ratings').addClass('hide_me');
    get_location_states();

    // Get the addresses based on the state
    $('#state_selector').change(function(){
        var selected = $(this).val();
    });

    $('#submit').click(function(){
        var state = $('#state_selector').find('option:selected').val();
        get_location_data(state)
    });

    get_dashboard_select();

    $('#dashboard_button').click(function(){
        var location_id = $('#dashboard-locations').find('option:selected').attr('value')
        var location_address = $('#dashboard-locations').find('option:selected').text();
        if (barChart != null) {
            barChart.destroy();
            $('canvas#ratings_chart').remove();
            $('div#bar_container').append('<canvas id="ratings_chart"></canvas>');
        }
        if (ratingChart != null) {
            ratingChart.destroy();
            $('canvas#travel_style_chart').remove();
            $('div#travel_style_container').append('<canvas id="travel_style_container"></canvas>')
        }
        if (doughnutChart != null) {
            doughnutChart.destroy();
            $('canvas#donut_chart').remove();
            $('div#donut_container').append('<canvas id="travel_style_container"></canvas>');
        }
        get_panel_metrics(location_id, location_address);
    });

    $('#review_button').click(function(){
        var location_id = $('#review-locations').find('option:selected').attr('value')
        var location_address = $('#review-locations').find('option:selected').text();
        $('#location_span').text(location_address);
        get_reviews(location_id);
    });
});

var get_location_states = function() {
    $.ajax({
            url: '/get_states',
            //data: call_data, //$('form').serialize(),
            type: 'GET',
            success: function(response) {
                var dropdown = $('#state_selector');
                $.each(response, function(i, val) {
                    var state = val[0];
                    dropdown.append($("<option></option>")
                                        .attr("value", state)
                                        .text(state));
                });
            },
            error: function(error) {
            }
        });
};

var get_dashboard_select = function() {
    $.ajax({
            url: '/get_dashboard_select',
            type: 'GET',
            success: function(response) {
                var dropdown = $('#dashboard-locations');
                var reviewDropdown = $('#review-locations')
                $.each(response, function(i, val) {
                    var address = val;
                    var id = i;
                    dropdown.append($("<option></option>")
                                        .attr("value", id)
                                        .text(address));
                    reviewDropdown.append($("<option></option>")
                                        .attr("value", id)
                                        .text(address));
                });
            },
            error: function(error) {
            }
        });
};

var get_location_data = function(state) {
    var data = {
        'state' : state,
    };

    $.ajax({
            url: '/get_locations_data',
            data: data,
            type: 'GET',
            success: function(response) {
                if (response.error) {
                    alert(response.error);
                }
                else {
                    $('#value_ratings').removeClass('hide_me');
                    var locationT = $('#value_ratings');
                    if ( $.fn.DataTable.isDataTable(locationT) ) {
                        locationT.DataTable().destroy();
                    }
                    locationT.DataTable({
                        "paginate": true,
                        "filter": true,
                        "sort": true,
                        "aaData": response,
                        'searching': true,
                        "scrollY": "600px",
                        "scrollX": true,
                        "fixedHeader": {'header': true},
                        "columns": [
                            {"width": "40%"},
                            {"width": "7%"},
                            {"width": "7%"},
                            {"width": "7%"},
                            {"width": "7%"},
                            {"width": "7%"},
                            {"width": "7%"},
                            {"width": "7%"},
                            {"width": "7%"},
                            {"width": "7%"},
                            {"width": "7%"}
                        ],
                        "aoColumns": [
                            {mData: 'address'},
                            {mData: 'total_reviews'},
                            {mData : 'overall'},
                            {mData: 'value'},
                            {mData : 'location'},
                            {mData : 'sleep'},
                            {mData : 'room'},
                            {mData : 'clean'},
                            {mData : 'service'},
                            {mData : 'checkin'},
                            {mData : 'business'}
                        ],
                    });
                }

            },
            error: function(error) {
            }
        });

};

var get_panel_metrics = function(location_id, location_address) {
     var data = {'id' : location_id}
     $.ajax({
            url: '/get_panel_data',
            data: data,
            type: 'GET',
            success: function(response) {
                if (response.error) {
                    alert(response.error);
                }
                else {
                    console.log(response.total_reviews);
                    $('#stays p').html(response.total_reviews);
                    $('#neg_revs p').html(response.neg_total);
                    $('#pos_revs p').html(response.pos_total);

                    var val = response.value;
                    var loc = response.location;
                    var sleep = response.sleep;
                    var room = response.room;
                    var clean = response.clean;
                    var service = response.service;
                    var checkin = response.checkin;
                    var business = response.business;
                    var total_possible = response.possible_score;

                    var chart = new Chart($('#ratings_chart'), {
                        type: 'bar',
                        data: {
                            labels: ["Value", "Location", "Sleep", "Room", "Cleanliness",
                                        "Service", "Check-in", "Business"],
                            datasets: [
                                {
                                    label: "Aggregate Rating",
                                    backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                                    data: [val,loc,sleep,room,clean,service,checkin,business]
                                }
                            ]
                        },
                        options: {
                            legend: { display: false },
                            title: {
                                display: true,
                                text: 'Total Scores by Category'
                            },
                            scales: {
                                yAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Total Rating'
                                    },
                                    ticks: {
                                        beginAtZero: true,
                                        max: total_possible
                                    }
                                }]
                            }
                        }
                    });
                    barChart = chart;
                    get_score_comparison(total_possible,val,loc,sleep,room,clean,
                                        service,checkin,business);
                }
                get_travel_style_analysis(data);
            },
            error: function(error) {
            }
        });

};

var get_score_comparison = function(total_possible,val,loc,sleep,room,clean,
                                        service,checkin,business) {
    var lowest_score = val;
    var highest_score = val;
    var lowest_val = 'value';
    var highest_val = 'value';
    var score_dict = {
        'value': val,
        'location': loc,
        'sleep': sleep,
        'room': room,
        'clean': clean,
        'service': service,
        'checkin': checkin,
        'business': business
    };

    for (var key in score_dict) {
        var val = score_dict[key];
        if ( val < lowest_score){
            lowest_score = val;
            lowest_val = key
        }
        if (val > highest_score) {
            highest_score = val;
            highest_val = key;
        }
    }
    $('#lowest_rating p').html(lowest_val);
    $('#highest_rating p').html(highest_val);

};

var get_travel_style_analysis = function(data) {
    $.ajax({
            url: '/get_travel_style_analysis',
            data: data,
            type: 'GET',
            success: function(response) {
                if (response.error) {
                    alert(response.error);
                }
                else {

                    var ts_chart = new Chart($('#travel_style_chart'), {
                        type: 'bar',
                        data: {
                            labels: ["Couples", "Business", "Families", "Unknown",
                                        "Solo", "Friends"],
                            datasets: [
                                {
                                    label: "Ratings by Travel Style",
                                    backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                                    data: [response.Couples, response.Business, response.Families,
                                            response.Unknown, response.Solo, response.Friends]
                                }
                            ]
                        },
                        options: {
                            legend: { display: false },
                            title: {
                                display: true,
                                text: 'Average Overall Rating by Travel Type'
                            },
                            scales: {
                                yAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Average Overall Rating'
                                    },
                                    ticks: {
                                        beginAtZero: true,
                                        max: 5
                                    }
                                }]
                            }
                        }
                    });
                    ratingChart = ts_chart;
                }
                get_doughnut_chart(data);
            },
            error: function(error) {
            }
        });
}

var get_doughnut_chart = function(data){
    $.ajax({
            url: '/get_doughnut_chart',
            data: data,
            type: 'GET',
            success: function(response) {
                if (response.error) {
                    alert(response.error);
                }
                else {
                    var overall_score = response.overall;
                    var dn_chart = new Chart($('#donut_chart'), {
                        type: 'doughnut',
                        data: {
                            labels: ['Negative Score', 'Neutral Score', 'Positive Score'],
                            datasets: [
                                {
                                    label: "Sentiment Analysis",
                                    backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9"],
                                    data: [response.neg_score, response.neut_score,
                                            response.pos_score]
                                }
                            ]
                        },
                        options: {
                            title: {
                                display: true,
                                text: 'Sentiment Analysis Scores'
                            }
                        }
                    });
                    ratingChart = dn_chart;
                }
            },
            error: function(error) {
            }
        });
}

var get_reviews = function(location_id) {
    var data = {'id': location_id};
    $.ajax({
           url: '/get_reviews',
           data: data,
           type: 'GET',
           success: function(response) {
               var slideContainer = $('#siteDisplay');
               $.each(response, function(i, val) {
                   var review = val
                   slideContainer.append($('<div class="reviewSlides"><p>'
                                           + review + '</p></div>'));
               });
               slideIndex = 1;
               showDivs(slideIndex);
           },
           error: function(error) {
           }
       });
}
var plusDivs = function(n) {
    showDivs(slideIndex += n);
};

var showDivs = function(n) {
    var i;
    var x = $('.reviewSlides');
    if (n > x.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = x.length
    }

    for (i = 0; i < x.length; i++) {
        $(x[i]).addClass('displayNone');
    }

    $(x[slideIndex-1]).removeClass('displayNone');
}
