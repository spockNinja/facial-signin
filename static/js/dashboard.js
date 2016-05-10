app.Dashboard = (function() {
    var dash = {};

    dash.faceData = ko.observable();
    dash.comparisonPhoto = ko.observable();

    dash.takePhoto = function() {
        app.openCamera(function(rawResponse) {
            console.log(rawResponse);
        });
    };

    dash.confirmPhoto = function() {
        $.post('/confirmPhoto', JSON.stringify(dash.faceData()), function(response) {
            if (!response.success) {
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
