app = {
    models: {},
};

ko.validation.init({
    decorateInputElement: true,
    errorAsTitle: false,
    messageTemplate: 'customValidationMessage'
});

ko.validation.rules.checkExists = {
    async: true,
    validator: function (val, url, callback) { // yes, you get a 'callback'
        var checkUrl = url+val;
        $.post(checkUrl, function(response) {
            callback({isValid: response.success, message: response.message});
        });
    },
    message: 'Already exists'
};
ko.validation.registerExtenders();
