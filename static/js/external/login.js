/*
    JS file for login page
*/

app.index = function() {
    var self = {};

    self.loginForm = {
        username: ko.observable('').extend({required: true}),
        password: ko.observable('').extend({required: true})
    };

    self.loginForm.ready = ko.pureComputed(function() {
        return (self.loginForm.username.isValid() &&
                self.loginForm.password.isValid());
    });

    self.registerForm = {
        username: ko.observable('').extend({
            required: true,
            checkExists: '/checkUsername?username='
        }),
        password: ko.observable('').extend({required: true}),
        confirmPassword: ko.observable(''),
        emailFocused: ko.observable(false)
    };

    // To utilize the benefits of textInput but only validate after blur,
    // we have to combine it with hasFocus and onlyIf
    self.registerForm.emailFocused = ko.observable(false);
    var validAfterBlur = function() {
        return !self.registerForm.emailFocused();
    };
    self.registerForm.email = ko.observable('').extend({
        email: {message: 'Please provide a real email address', onlyIf: validAfterBlur},
        checkExists: {params: '/checkEmail?email=', onlyIf: validAfterBlur}
    });

    // add the equal validator, since the reference didn't exist at creation
    self.registerForm.confirmPassword.extend({
        equal: { message: 'Passwords must match', params: self.registerForm.password}
    });

    self.readyToRegister = ko.pureComputed(function() {
        if (self.registerForm.username.isValidating() || self.registerForm.email.isValidating()) {
            return false;
        }
        return ko.validatedObservable(self.registerForm).isValid();
    });

    self.login = function() {
        var loginUrl = '/login?' + $.param(ko.toJS(self.loginForm));
        $.post(loginUrl, function(response) {
            if (response.success) {
                window.location.href = '/dashboard';
            }
            else {
                bootbox.alert(response.message);
            }
        });
    };

    self.register = function() {
        var registerParams = {
            username: self.registerForm.username(),
            password: self.registerForm.password(),
            email: self.registerForm.email()
        };
        var registerUrl = '/register?' + $.param(registerParams);
        $.post(registerUrl, function(response) {
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
