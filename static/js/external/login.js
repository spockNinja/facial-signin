/*
    JS file for login page
*/

app.index = function() {
    var self = {};

    self.needToRegister = ko.observable(false);
    self.username = ko.observable().extend({
        required: true,
        checkExists: {params: '/checkUsername?username=', onlyIf: self.needToRegister}
    });
    self.password = ko.observable().extend({required: true});

    self.confirmPassword = ko.observable().extend({
        required: true,
        equal: { message: 'Passwords must match', params: self.password}
    });

    // To utilize the benefits of textInput but only validate after blur,
    // we have to combine it with hasFocus and onlyIf
    self.emailFocused = ko.observable(false);
    var validateEmail = function() {
        return !self.emailFocused();
    };
    self.email = ko.observable().extend({
        required: true,
        email: {message: 'Please provide a real email address', onlyIf: validateEmail},
        checkExists: {params: '/checkEmail?email=', onlyIf: validateEmail}
    });

    self.readyToLogin = ko.pureComputed(function() {
        return (self.username.isValid() &&
                self.password.isValid());
    });

    self.readyToRegister = ko.pureComputed(function() {
        if (self.username.isValidating() || self.email.isValidating()) {
            return false;
        }
        return ko.validatedObservable({
            username: self.username, email: self.email,
            password: self.password, confirmPassword: self.confirmPassword

        }).isValid();
    });

    self.loginOrRegister = function() {
        if (self.needToRegister()) {
            self.register();
        }
        else {
            self.login();
        }
    };

    self.login = function() {
        var loginInfo = {
            username: self.username(),
            password: self.password()
        };
        var loginUrl = '/login?' + $.param(loginInfo);
        $.post(loginUrl, function(response) {
            if (response.success) {
                window.location.href = '/dashboard';
            }
            else if (response.message === 'takePhoto') {
                self.comparePhoto();
            }
            else {
                bootbox.alert(response.message);
            }
        });
    };

    self.comparePhoto = function() {
        app.openCamera(function(response) {
            if (response.success) {
                $.post('/compareFace', JSON.stringify(response.data), function(compareResp) {
                    if (compareResp.success) {
                        window.location.href = '/dashboard';
                    }
                    else {
                        bootbox.alert("Face match failed! If it's really you, try again. If not, buzz of!");
                    }
                })
            }
            else {
                bootbox.alert(response.message, self.comparePhoto);
            }
        })
    }

    self.register = function() {
        var registerParams = {
            username: self.username(),
            password: self.password(),
            email: self.email()
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
