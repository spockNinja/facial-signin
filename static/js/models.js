app.models.Campaign = function() {
    var self = this;

    self.id = ko.observable('');
    self.name = ko.observable('');
    self.date_added = ko.observable('');

    self.editingName = ko.observable(false);
};
app.models.Campaign.prototype = new app.models.Model();
