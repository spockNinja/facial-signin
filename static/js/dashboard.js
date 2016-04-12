Webcam.attach( '#my_camera' );

snapshot_uri = null;
function take_snapshot() {
    Webcam.snap( function(data_uri) {
        snapshot_uri = data_uri;
        document.getElementById('my_result').innerHTML = '<img src="'+data_uri+'"/>';
    } );
}

function upload_snapshot() {
    if (snapshot_uri) {

        $.post('/analyzePhoto', snapshot_uri, function(response) {
            console.log(response);
        }).fail(function _handleFailure(jqXHR, textStatus, errorThrown) {
            document.open();
            document.write(jqXHR.responseText);
            document.close();
        });
    }
}
