/*
    JS file for login page
*/

app.login = {

    loginUsername: ko.observable(''),
    loginPassword: ko.observable(''),

    registerUsername: ko.observable(''),
    registerPassword: ko.observable(''),
    registerConfirmPassword: ko.observable(''),
    registerEmail: ko.observable(''),

    login: function() {
        var self = this;

        var loginUrl = '/external/login?username={loginUsername}&password={loginPassword}';
        $.post(loginUrl.format(ko.toJS(self)), function(response) {
            if (response.success) {
                window.location.href = '/dashboard.html';
            }
            else {
                bootbox.alert(response.message);
            }
        });
    },

    register: function() {
        var self = this;

        var registerUrl = '/external/register?username={registerUsername}&password={registerPassword}&email={registerEmail}';
        $.post(registerUrl.format(ko.toJS(self)), function(response) {
            if (response.success) {
                bootbox.alert("Thank you for registering. An email has been sent to you with a confirmation link inside.");
            }
            else {
                bootbox.alert(response.message);
            }
        });
    }
};

ko.applyBindings(app.login, $('body')[0]);
