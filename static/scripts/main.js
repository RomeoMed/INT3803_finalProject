$(document).ready(function(){
    $('#value_ratings').addClass('hide_me');
    $('#submit').attr("disabled", "disabled");
    $('.dyno_address').addClass('hide_me');
    // Get the locations for the dropdown
    get_location_states();

    // Get the addresses based on the state
    $('#state_selector').change(function(){
        var selected = $(this).val();
        get_locations(selected);
    });

    $('#address_selector').change(function(){
        $('#submit').removeAttr("disabled");
    });

    $('#submit').click(function(){
        var element1 = $('#address_selector');
        var element2 = $('#travel_style');
        var location_id = element1.find('option:selected').attr("value");
        var travel_style = element2.find('option:selected').attr("value");
        if (location_id && travel_style) {
            get_location_data(location_id, travel_style);
        }
    });

    $('#dash').click(function(){
        get_dashboard_select();
    });

    $('#dashboard_button').click(function(){
        get_panel_metrics();
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
                $.each(response, function(i, val) {
                    var address = val;
                    var id = i;
                    dropdown.append($("<option></option>")
                                        .attr("value", id)
                                        .text(address));
                });
            },
            error: function(error) {
            }
        });
};

var get_locations = function(state) {
    var data = {'state' : state};
    $.ajax({
            url: '/get_locations_by_state',
            data: data,
            type: 'GET',
            success: function(response) {
                var dropdown = $('#address_selector');
                $.each(response, function(i, val) {
                    var address = val;
                    var id = i;
                    dropdown.append($("<option></option>")
                                        .attr("value", id)
                                        .text(address));
                });
                $('.dyno_address').removeClass('hide_me');
            },
            error: function(error) {
            }
        });
};

var get_location_data = function(id, style) {
    var data = {
        'location_id' : id,
        'travel_style' : style
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
                    //var locationT = $('#loc_data');
                    var locationT = $('#value_ratings');
                    locationT.DataTable({
                        "paginate": true,
                        "filter": true,
                        "sort": true,
                        "aaData": response,
                        //"sDom": '<"top"<"clear">>rt<"bottom"lip<"clear">>',
                        'searching': true,
                        "aoColumns": [
                            {mData : 'overall'},
                            {mData: 'total_reviews'},
                            {mData: 'value'},
                            {mData : 'location'},
                            {mData : 'sleep'},
                            {mData : 'room'},
                            {mData : 'clean'},
                            {mData : 'service'},
                            {mData : 'checkin'},
                            {mData : 'business'},
                            {mData : 'total_overall'}
                        ],
                        /*data: response,
                        columns: [
                            {data : 'address'},
                            {data : 'csz'},
                            {data : 'total_reviews'},
                            {data: 'value'},
                            {data : 'location'},
                            {data : 'sleep'},
                            {data : 'room'},
                            {data : 'clean'},
                            {data : 'service'},
                            {data : 'checkin'},
                            {data : 'business'},
                            {data : 'overall'},
                            {data : 'total_overall'}
                        ]*/
                    });
                }
                $('#value_ratings').removeClass('hide_me');
            },
            error: function(error) {
            }
        });

};
