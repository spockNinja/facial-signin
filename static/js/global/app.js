app = {
    models: {},
};

app.openCamera = function(callback) {
    var messageHTML = [
        '<div id="camera" class="center-block" style="width: 320; height: 240px;"></div>',
        'For best results:<ul>',
        '<li>Look straight at the camera</li>',
        '<li>Center your face in the photo</li>',
        '<li>Keep a neutral expression</li>',
        '</ul>'
    ].join('');
    var messageElement = $(messageHTML);
    var cameraDialog = bootbox.dialog({
        title: 'Take a Photo',
        message: messageElement,
        buttons: {
            'Take the photo!': {
                className: 'btn-success',
                callback: function() {
                    Webcam.snap(callback);
                }
            },
            'Cancel': {
                className: 'btn-danger'
            }
        }
    });

    cameraDialog.on('shown.bs.modal', function() {
        Webcam.attach('#camera');
    });
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
