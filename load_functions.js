// this function is triggered by onload on body tag
// updates url params
function updateParams() {

    let hrefLinks = [];
    // update href
    // if window.location.search != "", update this page's a href links with current params
    if (window.location.search != "") {

        hrefLinks = document.getElementsByClassName("pure-menu-link");

        // iterate over hrefLinks and append current params
        for (let i = 0; i < hrefLinks.length; i++) {

            // append params
            hrefLinks[i].href = hrefLinks[i].href + window.location.search;
        }
    } else {
        // console.log("no additional params exist");
    }
}

// <!-- Get current params, if any, at the docsie home page to append to signup-widget query params -->


// for appending existing params, if any
function updateReqParams(formId) {
    // if there exists any query params in docsie home page
    // append it form action url
    if (window.location.search != "" && window.location.search != undefined && window.location.search != null) {

        var existingParamsArray = [], multipleParamsArray = [];

        // get current url get-params
        if (window.location.search.indexOf("&") != -1) {
            multipleParamsArray = window.location.search.split("?")[1].split("&");
            multipleParamsArray.forEach(function (item) {
                var splitItem = item.split("=");
                existingParamsArray.push(splitItem[0]);
                existingParamsArray.push(splitItem[1]);
            });
        } else {
            existingParamsArray = window.location.search.split("?")[1].split("=");
        }

        // create hidden input tags to append to form params
        for (let i = 0; i < existingParamsArray.length; i++) {

            // continue at odd i value
            if (i != 0 && i % 2 != 0)
                continue;

            // break at existingParamsArray.length
            if (i == existingParamsArray.length - 1)
                break;

            var input = document.createElement("input");
            input.setAttribute("type", "hidden");
            input.setAttribute("name", existingParamsArray[i]);
            input.setAttribute("value", existingParamsArray[i + 1]);
            document.getElementById(formId).appendChild(input);
        }
    }
}

// for checking validity of email and enabling/disabling 'triangle' button
function setSubmit(id1, id2) {

    if (document.getElementById(id1).validity.valid == true) {
        document.getElementById(id2).disabled = false;
    } else {
        document.getElementById(id2).disabled = true;
    }
}






var bannerElement = document.getElementById("cookies-use-agreement");

// check and set cookies for GDPR banner
function setCookie(cname, cvalue) {
    // var d = new Date();
    // d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    // var expires = "expires="+d.toUTCString();
    var expires = "expires=" + "Fri, 31 Dec 9999 23:59:59 GMT"
    document.cookie = cname + "=" + cvalue + ";" + expires;

    // hide banner upon accepting cookies agreement
    if (bannerElement)
    bannerElement.style.display = 'none';
}

// get cookie for a given name
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

// check if 'ViewedCookiesUseAgreement' cookie has been set, if not, show banner, else hide
let bannerSet = getCookie('ViewedCookiesUseAgreement');

if (bannerSet) {

    if (bannerElement)
    bannerElement.style.display = 'none';
} else {

    if (bannerElement)
    bannerElement.style.display = 'block';
}

(function() {
window._pa = window._pa || {};

var pa = document.createElement('script'); pa.type = 'text/javascript'; pa.async = true;
pa.src = ('https:' == document.location.protocol ? 'https:' : 'http:') + "//tag.marinsm.com/serve/5d54ce3419019cfe13000021.js";
var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(pa, s);
})();
 
