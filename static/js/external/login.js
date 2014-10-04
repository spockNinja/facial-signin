/*
    JS file for login page
*/

app.index = function() {
    var self = {};

    self.login = ko.validatedObservable({
        username: ko.observable('').extend({required: true}),
        password: ko.observable('').extend({required: true})
    });

    self.register = ko.validatedObservable({
        username: ko.observable('').extend({
            required: true,
            exists: {
                async: true,
                validator: function (val, params, callback) {
                    var userCheckUrl = '/external/checkUsername?username='+val;
                    $.post(userCheckUrl, function(response) {
                        callback({isValid: response.success, message: response.message});
                    });
                }
            }
        }),
        password: ko.observable('').extend({required: true}),
        confirmPassword: ko.observable('').extend({
            equal: { message: 'Passwords must match', params: self.registerPassword}
        }),
        email: ko.observable('').extend({
            email: {message: 'Please provide a real email address', params: true},
            exists: {
                async: true,
                validator: function (val, params, callback) {
                    var emailCheckUrl = '/external/checkEmail?email='+val;
                    $.post(emailCheckUrl, function(response) {
                        callback({isValid: response.success, message: response.message});
                    });
                }
            }
        })
    });


    self.readyToRegister = ko.computed( function() {
        if (self.register().username.isValidating() || self.register().email.isValidating()) {
            return false;
        }
        return self.register.isValid();
    });

    self.login = function() {
        var loginUrl = '/external/login?username={username}&password={password}';
        $.post(loginUrl.format(ko.toJS(self.login)), function(response) {
            if (response.success) {
                window.location.href = '/dashboard';
            }
            else {
                bootbox.alert(response.message);
            }
        });
    };

    self.register = function() {
        var registerUrl = '/external/register?username={username}&password={password}&email={email}';
        $.post(registerUrl.format(ko.toJS(self.register)), function(response) {
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

ko.applyBindings(app.index, $('body')[0]);
