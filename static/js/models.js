app.models.Model = function() {
    // Shared logic for all JS models
};

app.models.Entity = function() {
    var self = this;

    self.id = ko.observable('');
    self.name = ko.observable('');
    self.dateCreated = ko.observable('');
};
app.models.Entity.prototype = new app.models.Model();
