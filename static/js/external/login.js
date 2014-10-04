/*
    JS file for login page
*/

app.index = function() {
    var self = {};

    self.loginForm = ko.validatedObservable({
        username: ko.observable('').extend({required: true}),
        password: ko.observable('').extend({required: true})
    });

    self.registerForm = ko.validatedObservable({
        username: ko.observable('').extend({
            required: true,
            checkExists: '/external/checkUsername?username='
        }),
        password: ko.observable('').extend({required: true}),
        confirmPassword: ko.observable(''),
        email: ko.observable('').extend({
            email: {message: 'Please provide a real email address', params: true},
            checkExists: '/external/checkEmail?email='
        })
    });

    // add the equal validator, since the reference didn't exist at creation
    self.registerForm().confirmPassword.extend({
        equal: { message: 'Passwords must match', params: self.registerForm().password}
    });

    self.readyToRegister = ko.computed( function() {
        if (self.registerForm().username.isValidating() || self.registerForm().email.isValidating()) {
            return false;
        }
        return self.registerForm.isValid();
    });

    self.login = function() {
        var loginUrl = '/external/login?username={username}&password={password}';
        $.post(loginUrl.format(ko.toJS(self.loginForm)), function(response) {
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
        $.post(registerUrl.format(ko.toJS(self.registerForm)), function(response) {
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
