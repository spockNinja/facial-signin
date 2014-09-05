/*
    JS file for login page
*/

app.login = {

    loginUsername: ko.observable(''),
    loginPassword: ko.observable(''),

    registerUsername: ko.observable(''),
    registerPassword: ko.observable(''),
    registerEmail: ko.observable(''),

    login: function() {
        var self = this;

        var loginUrl = '/external/login?username={loginUsername}&password={loginPassword}';
        $.post(loginUrl.format(ko.toJS(self)), function(response) {
            if (response.success) {
                console.log('Woot, logged in');
            }
        });
    },

    register: function() {
        var self = this;

        var registerUrl = '/external/register?username={registerUsername}&password={registerPassword}&email={registerEmail}';
        $.post(registerUrl.format(ko.toJS(self)), function(response) {
            if (response.success) {
                console.log('Woot, registered');
            }
        });
    }
};

ko.applyBindings(app.login, $('body')[0]);
