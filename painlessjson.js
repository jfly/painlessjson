painlessjson = function(url) {
    //TODO - make this not rely upon mootools?
    url = url || "http://jfly.algnex.us/painlessjson/painlessjson.py";
    this.get = function(user, domain, callback) {
        var jsonp = new Request.JSONP({
            url: url,
            data: {
                user: user,
                domain: domain,
            },
            onComplete: callback
        }).send();
    };
    this.put = function(user, domain, val, callback) {
        var jsonp = new Request.JSONP({
            url: url,
            data: {
                user: user,
                domain: domain,
                val: val
            },
            onComplete: callback
        }).send();
    };
};
