painlessjson = function(url) {
    // copied from tnoodletimer
    tnoodle = {};
    tnoodle.jsonpcount = 1;
    tnoodle.jsonp = function(callback, url, data) {
        var callbackname = "tnoodle.jsonp.callback" + this.jsonpcount++;
        eval(callbackname + "=callback");
        if (url.indexOf("?") > -1) {
            url += "&callback=";
        } else {
            url += "?callback=";
        }

        url += callbackname + "&" + tnoodle.toQueryString(data);
        url += "&" + new Date().getTime().toString(); // prevent caching

        var script = document.createElement("script");
        script.setAttribute("src",url);
        script.setAttribute("type","text/javascript");
        document.body.appendChild(script); //TODO - doesn't work until body is loaded
    };
    tnoodle.toQueryString = function(data) {
        var url = "";
        for(var key in data) {
            if(data.hasOwnProperty(key)) {
                url += "&" + encodeURIComponent(key) + "=" + encodeURIComponent(data[key]);
            }
        }
        if(url.length === 0) {
            return url;
        }

        return url.substring(1);
    };

    url = url || "http://jfly.algnex.us/painlessjson/painlessjson.py";
    this.get = function(user, domain, callback) {
        data = {
            user: user,
            domain: domain
        };
        tnoodle.jsonp(callback, url, data);
    };
    this.put = function(user, domain, value, callback) {
        data = {
            user: user,
            domain: domain,
            value: value
        };
        tnoodle.jsonp(callback, url, data);
    };
};
