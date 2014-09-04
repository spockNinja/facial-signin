/*
    JS file for login page
*/

app.login = {

    username: ko.observable(''),
    password: ko.observable(''),
    email: ko.observable(''),

    login: function() {
        var self = this;

        var loginUrl = '/external/login?username={0}&password={1}'.format(self.username(), self.password());
        $.post(loginUrl, function(response) {
            if (response.success) {
                console.log('Woot, logged in');
            }
        });
    },

    register: function() {
        var self = this;

        var registerUrl = '/external/register?username={0}&password={1}&email={2}'.format(self.username(), self.password(), self.email());
        $.post(registerUrl, function(response) {
            if (response.success) {
                console.log('Woot, registered');
            }
        });
    }
};

ko.applyBindings(app.login, $('body')[0]);
