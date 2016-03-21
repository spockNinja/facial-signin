app = {
    models: {},
};

ko.validation.init({
    decorateInputElement: true,
    errorAsTitle: false,
    messageTemplate: 'customValidationMessage'
});

ko.bindingHandlers.hidden = {
    update: function(element, valueAccessor, allBindings, viewModel, bindingContext) {
        ko.bindingHandlers.visible.update(element, function() {
            return !ko.utils.unwrapObservable(valueAccessor());
        }, allBindings, viewModel, bindingContext);
    }
};

ko.bindingHandlers.toggle = {
    init: function (element, valueAccessor) {
        var value = valueAccessor();
        ko.applyBindingsToNode(element, {
            click: function () {
                value(!value());
            }
        });
    }
};

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

// Auto close flashed messages after 10 seconds
window.setTimeout(function() {
    $(".flashed-alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 10000);
