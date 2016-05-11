app.Dashboard = (function() {
    var dash = {};

    dash.faceData = ko.observable();
    dash.comparisonPhoto = ko.observable();
    dash.successMessage = ko.observable();

    dash.takePhoto = function() {
        app.openCamera(function(response) {
            if (response.success) {
                dash.faceData(response.data);
                dash.comparisonPhoto(response.img);
            }
            else {
                bootbox.alert(response.message);
            }
        });
    };

    dash.takeAnother = function() {
        dash.faceData(null);
        dash.comparisonPhoto(null);
        dash.takePhoto();
    };

    dash.confirmPhoto = function() {
        $.post('/confirmPhoto', JSON.stringify(dash.faceData()), function(response) {
            if (response.success) {
                dash.faceData(null);
                dash.comparisonPhoto(null);
                dash.successMessage('Base photo successfully uploaded!');
            }
            else {
                bootbox.alert(response.message);
            }
        });
    };

    dash.init = function() {
        ko.applyBindings(dash, $('#dashboard-container')[0]);
    };

    return dash;
})();

app.Dashboard.init();
