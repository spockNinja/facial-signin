/*
    JS file for login page
*/

app.login = function() {
    var self = {};

    self.loginUsername = ko.observable('');
    self.loginPassword = ko.observable('');

    self.readyToLogin = ko.computed( function() {
        return self.loginUsername() && self.loginPassword();
    });

    self.registerUsername = ko.observable('');
    self.registerPassword = ko.observable('');
    self.registerConfirmPassword = ko.observable('').extend({
        equal: { message: 'Passwords must match', params: self.registerPassword}
    });
    self.registerEmail = ko.observable('').extend({
        email: {message: 'Please provide a real email address', params: true}
    });


    self.readyToRegister = ko.computed( function() {
        return self.registerUsername() && self.registerPassword() &&
               self.registerConfirmPassword.isValid() && self.registerEmail.isValid();
    });

    self.login = function() {
        var loginUrl = '/external/login?username={loginUsername}&password={loginPassword}';
        $.post(loginUrl.format(ko.toJS(self)), function(response) {
            if (response.success) {
                window.location.href = '/dashboard';
            }
            else {
                bootbox.alert(response.message);
            }
        });
    };

    self.register = function() {
        var registerUrl = '/external/register?username={registerUsername}&password={registerPassword}&email={registerEmail}';
        $.post(registerUrl.format(ko.toJS(self)), function(response) {
            if (response.success) {
                bootbox.alert("Thank you for registering. An email has been sent to you with a confirmation link inside.");
            }
            else {
                bootbox.alert(response.message);
            }
        });
    };

    return self;
}();

ko.applyBindings(app.login, $('body')[0]);
