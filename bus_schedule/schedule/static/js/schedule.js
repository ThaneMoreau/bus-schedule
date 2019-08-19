$('body').on('change', '#dispatch_station_select', function() {
    var from = $('#dispatch_station_select').find(":selected").val()
    $.get('arrive_stations?from=' + from, function(data) {
        $('#arrive_station_select').empty();
        $.each(data, function(value, option) {
            $('#arrive_station_select').append(
                $('<option>').text(option).attr('value', value)
            );
        });
    });
    $('#arrive_station_select').removeAttr("disabled");
  });

$('body').on('click', '#trips-btn', function() {
    var from = $('#dispatch_station_select').find(":selected").val()
    var to = $('#arrive_station_select').find(":selected").val()
    if (from != -1 && to != -1) {
        $.get('trips_table?from=' + from + '&to=' + to, function(data) {
            $('#trips_table').remove();
            $('#content').append(data);
        });
    }
});

$('body').on('click', '.text-info', function(e) {
    e.preventDefault();
    $.get('route_details?system_id=' + $(this).data('id'), function(data) {
        $('#routeDetailsModalCenter').remove();
        $('#content').append(data);
        $('#routeDetailsModalCenter').modal('show');
    });
});
