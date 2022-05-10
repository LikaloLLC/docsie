(function() {
    var scriptEl = document.createElement('script');
    scriptEl.type = 'text/javascript';
    scriptEl.async = true;
    scriptEl.src = window.rconfWar + '/editor/scripts/util.js';
    var scriptToAppendBefore = document.getElementsByTagName('script')[0];
    scriptToAppendBefore.parentNode.insertBefore(scriptEl, scriptToAppendBefore);
})();

function showLoadingDots() {
    var loading = jQuery('#editor-loading');
    if (loading.length == 0) {
        loading = jQuery(document.createElement('div'));
        loading.attr('id', 'editor-loading');
        loading.css(
            'background',
            "url(window.rconfWar + '/_dm/s/rt/images/nav-loader.gif') no-repeat center 40px  white"
        );
        loading.css('background-position-x', '138px');
        loading.css('background-position-y', '40px');
        loading.css('z-index', '10000');
        jQuery('body').append(loading);
    }
    loading.css('display', 'block');
    jQuery('body, html').scrollTop(0);
}

function showLoadingDotsNEW() {
    var loading = jQuery('#editor-loading');
    if (loading.length == 0) {
        loading = jQuery(document.createElement('div'));
        loading.attr('id', 'editor-loading');
        loading.css(
            'background',
            "url(window.rconfWar + '/_dm/s/rt/images/nav-loader.gif') no-repeat center 40px  white"
        );
        loading.css('background-position-x', '138px');
        loading.css('background-position-y', '40px');
        loading.css('z-index', '10000');
        loading.css('position', 'absolute');
        loading.css('width', '100%');
        loading.css('height', '1000px');
        loading.css('top', '0px');
        jQuery('body').append(loading);
    }
    loading.css('display', 'block');
    jQuery('body, html').scrollTop(0);
}

function hideLoading() {
    var loading = jQuery('#editor-loading');
    if (loading != null) {
        loading.css('display', 'none');
    }
}

function getElementProperty(elementClassName, property) {
    // get jquery element by class name
    var jQueryObject = jQuery(elementClassName);
    if (jQueryObject.get(0) != null) {
        // get the style property of the DOM element
        return getStyleProp(jQueryObject.get(0), property, window);
    }
}

function getStyleProp(obj, propName, wnd) {
    if (obj.currentStyle) {
        propName = propName.replace(/-(.)/g, uppercaseThis);
        propName = propName.replace(/(-)/g, '');
        return obj.currentStyle[propName];
    } else if (wnd.getComputedStyle) {
        return wnd.getComputedStyle(obj, null).getPropertyValue(propName);
    }

    return null;
}

function replaceAll(Source, stringToFind, stringToReplace) {
    var temp = Source;
    var index = temp.indexOf(stringToFind);
    while (index != -1) {
        temp = temp.replace(stringToFind, stringToReplace);
        index = temp.indexOf(stringToFind);
    }
    return temp;
}

function setTempCss(css) {
    var newStyle = document.createElement('style');
    jQuery(newStyle).html(css);
    jQuery(newStyle).attr('id', 'tempCss');
    jQuery('head').append(newStyle);
}

function isIE() {
    if (navigator.userAgent.indexOf('MSIE') != -1) {
        // Using IE
        return true;
    } else {
        return false;
    }
}

function wpGetStyleSheet() {
    return _dmGetStyleSheet('globalCss');
}

function wpGetThemeStyleSheet() {
    return _dmGetStyleSheet('globalCssTheme');
}

function wpGetHeaderPageStyleSheet() {
    return _dmGetStyleSheet('headerCss');
}

function wpGetHeaderPageDeviceStyleSheet() {
    return _dmGetStyleSheet('headerDeviceCss');
}

function wpGetPageStyleSheet() {
    return _dmGetStyleSheet('pagestyle');
}

function wpGetPageDeviceStyleSheet() {
    return _dmGetStyleSheet('pagestyleDevice');
}

function wpGetInnerPageStyleSheet() {
    return _dmGetStyleSheet('innerPagesStyle');
}

function wpGetInnerPageDeviceStyleSheet() {
    return _dmGetStyleSheet('innerPagesStyleDevice');
}

function _dmGetStyleSheet(styleSheetID) {
    if (isIE()) {
        return (styleSheet = document.styleSheets[styleSheetID]);
    } else {
        // go over the stylesheets, and get the one inside "globalCss"
        for (var i = 0; i < document.styleSheets.length; i++) {
            // get the owner node
            var node = _getSpecificSheetNode(document.styleSheets, i);
            if (node != null && node !== undefined) {
                // get node id
                var id = node.id;
                if (id != null && id !== undefined) {
                    if (id === styleSheetID) {
                        // we found the stylesheet
                        return document.styleSheets[i];
                    }
                }
            }
        }
        return null;
    }
}

function _getSpecificSheetNode(stylesheets, index) {
    var sheet = null;
    if (stylesheets && index !== undefined) {
        try {
            sheet = stylesheets[index];
            if (!sheet && stylesheets.item) {
                sheet = stylesheets.item(index);
            }
        } catch (e) {
            sheet = null;
        }
    }
    return sheet ? sheet.ownerNode : null;
}

function cleanInlineStyle(selector, attributesToRemove) {
    if (attributesToRemove == null || attributesToRemove == undefined) {
        return;
    }
    var elem = jQuery(selector).get(0);

    for (var j = 0; j < attributesToRemove.length; j++) {
        // get name
        var key = attributesToRemove[j];

        // set attribute
        elem.style[toCamelCase(key)] = '';
    }
}

function updateInlineStyle(selector, attributesArray) {
    if (attributesArray == null || attributesArray == undefined) {
        return;
    }
    var elem = jQuery(selector).get(0);

    for (var j = 0; j < attributesArray.length; j++) {
        // get name
        var key = attributesArray[j].key;
        // get value
        var value = attributesArray[j].value;

        // set attribute
        elem.style[toCamelCase(key)] = value;
    }
}

function getInlineStyleAttribute(selector, attribute) {
    // get element by css selector
    var elem = jQuery(selector).get(0);

    if (elem != null && elem != undefined) {
        return elem.style[toCamelCase(attribute)];
    }
}

function getGlobalCSSToString() {
    var styleSheet = wpGetStyleSheet();
    return _dmCSSToString(styleSheet);
}

function getGlobalThemeCSSToString() {
    var styleSheet = wpGetThemeStyleSheet();
    return _dmCSSToString(styleSheet);
}

function getPageCSSToString() {
    var styleSheet = wpGetPageStyleSheet();
    return _dmCSSToString(styleSheet);
}

function getPageDeviceCSSToString() {
    var styleSheet = wpGetPageDeviceStyleSheet();
    return _dmCSSToString(styleSheet);
}

function getHeaderPageCSSToString() {
    var styleSheet = wpGetHeaderPageStyleSheet();
    return _dmCSSToString(styleSheet);
}

function _dmCSSToString(styleSheet) {
    if (!styleSheet || styleSheet == null) return;
    var result = '';
    if (isIE()) {
        // run the ie version
        for (var i = 0; i < styleSheet.imports.length; i++) {
            // get rule
            var importCss = styleSheet.imports[i];
            result += "@import url('" + importCss.href + "');\n";
        }
        for (var i = 0; i < styleSheet.rules.length; i++) {
            // get rule
            var rule = styleSheet.rules[i];
            result += rule.cssText + '\n';
        }
    } else {
        for (var i = 0; i < styleSheet.cssRules.length; i++) {
            // get rule
            var rule = styleSheet.cssRules[i];
            result += rule.cssText + '\n';
        }
    }
    return result;
}

function updateCssInternal(selector, css, attributesArray, styleSheet, priority) {
    var foundRule = false;
    priority = priority || null;
    // look for the selector in the existing rules
    for (var i = 0; i < styleSheet.cssRules.length; i++) {
        // get rule
        var rule = styleSheet.cssRules[i];
        if (rule.constructor == CSSStyleRule) {
            // this is a style rule

            var ruleSelector = rule.selectorText.toLowerCase();
            ruleSelector = replaceAll(ruleSelector, '*', '');
            var mySelector = selector.toLowerCase();
            mySelector = replaceAll(mySelector, '*', '');

            if (ruleSelector === mySelector) {
                // we found the rule, now set its attributes
                for (var j = 0; j < attributesArray.length; j++) {
                    // get name
                    var key = attributesArray[j].key;
                    // get value
                    var value = attributesArray[j].value;

                    // set attribute
                    rule.style.setProperty(key, value, priority);
                }
                foundRule = true;
                //return;
            }
        }
    }
    return foundRule;
}

function updateCss(selector, css, attributesArray, allowTheme, priority, opts) {
    var options = opts || {};

    if (isIE()) {
        // run the ie version
        updateCssIE(selector, css, attributesArray, allowTheme);
        return;
    }

    // get stylesheet
    var styleSheet = wpGetStyleSheet();

    var foundRule = updateCssInternal(selector, css, attributesArray, styleSheet, priority);

    if (allowTheme) {
        styleSheet = wpGetThemeStyleSheet();
        if (styleSheet && styleSheet != null) {
            foundRule = updateCssInternal(selector, css, attributesArray, styleSheet, priority) || foundRule;
        }
    }
    if (!foundRule) {
        // this is a new rule - add it at the end
        styleSheet.insertRule(selector + '{' + prioritizeCss(css, priority) + '}', styleSheet.cssRules.length);
    }
}

function prioritizeCss(css, priority) {
    retCss = css;
    if (priority) {
        retCss = css.replace(/;/g, ' !' + priority + ';');
        if (retCss.indexOf(priority) === -1) {
            retCss = css + ' !' + priority + ';';
        }
    }
    return retCss;
}

function removeCssAttributesFromStyleSheet(selector, attributesArray, ruleValidator, styleSheet) {
    if (styleSheet == null) return;

    // look for the selector in the existing rules
    for (var i = 0; i < styleSheet.cssRules.length; i++) {
        // get rule
        var rule = styleSheet.cssRules[i];

        if (rule.constructor == CSSStyleRule) {
            // this is a style rule

            var ruleSelector = rule.selectorText.toLowerCase();
            ruleSelector = replaceAll(ruleSelector, '*', '');
            var mySelector = selector.toLowerCase();
            mySelector = replaceAll(mySelector, '*', '');

            var isRule = ruleSelector === mySelector || (ruleValidator && ruleValidator(ruleSelector));
            if (isRule) {
                // we found the rule, now set its attributes
                for (var j = 0; j < attributesArray.length; j++) {
                    // get name
                    var key = attributesArray[j];

                    // remove attribute
                    rule.style.removeProperty(key);
                }
            }
        }
    }
    // we didnt find the rule - nothing to do
}

function removeCssAttributes(selector, attributesArray, ruleValidator, stylesheet) {
    if (isIE()) {
        removeCssAttributesIE(selector, attributesArray, ruleValidator);
        return;
    }
    // get stylesheet
    styleSheet = stylesheet || wpGetStyleSheet();
    removeCssAttributesFromStyleSheet(selector, attributesArray, ruleValidator, styleSheet);

    //  styleSheet = wpGetThemeStyleSheet();
    //  if(styleSheet && styleSheet != null) {
    //    removeCssAttributesFromStyleSheet(selector, attributesArray,
    //      ruleValidator, styleSheet);
    //  }
}

function updateCssIEInternal(selector, css, attributesArray, styleSheet) {
    var foundRule = false;
    for (var i = 0; i < styleSheet.rules.length; i++) {
        // get rule
        var rule = styleSheet.rules[i];

        var ruleSelector = rule.selectorText.toLowerCase();
        ruleSelector = replaceAll(ruleSelector, '*', '');
        var mySelector = selector.toLowerCase();
        mySelector = replaceAll(mySelector, '*', '');

        if (ruleSelector === mySelector) {
            // we found the rule, now set its attributes
            for (var j = 0; j < attributesArray.length; j++) {
                // get name
                var key = attributesArray[j].key;

                // to camelcase
                // key = key.replace(/\-(.)/g, function(m, l){return
                // l.toUpperCase()});
                key = toCamelCase(key);

                // get value
                var value = attributesArray[j].value;
                // set attribute
                rule.style.setAttribute(key, value);
            }
            foundRule = true;
            // return;
        }
    }
    return foundRule;
}

function updateCssIE(selector, css, attributesArray, allowTheme) {
    // get stylesheet
    var styleSheet = wpGetStyleSheet();

    var foundRule = updateCssIEInternal(selector, css, attributesArray, styleSheet);
    // look for the selector in the existing rules
    if (allowTheme) {
        styleSheet = wpGetThemeStyleSheet();
        if (styleSheet && styleSheet != null) {
            foundRule = updateCssIEInternal(selector, css, attributesArray, styleSheet) || foundRule;
        }
    }

    if (!foundRule) {
        if (css != '') {
            // this is a new rule - add it at the end
            styleSheet.addRule(selector, css);
        }
    }
}

function removeCssAttributesIEInternal(selector, attributesArray, styleSheet, ruleValidator) {
    // look for the selector in the existing rules
    for (var i = 0; i < styleSheet.rules.length; i++) {
        // get rule
        var rule = styleSheet.rules[i];

        var ruleSelector = rule.selectorText.toLowerCase();
        ruleSelector = replaceAll(ruleSelector, '*', '');
        var mySelector = selector.toLowerCase();
        mySelector = replaceAll(mySelector, '*', '');

        var isRule = ruleSelector === mySelector || (ruleValidator && ruleValidator(ruleSelector));
        if (isRule) {
            // we found the rule, now set its attributes
            for (var j = 0; j < attributesArray.length; j++) {
                // get name
                var key = attributesArray[j];
                // to camelcase
                //    			key = key.replace(/\-(.)/g, function(m, l){return l.toUpperCase()});
                key = toCamelCase(key);

                // remove attribute
                rule.style.removeAttribute(key);
            }
            //    		return;
        }
    }
}

function removeCssAttributesIE(selector, attributesArray, ruleValidator) {
    // get stylesheet
    var styleSheet = wpGetStyleSheet();
    removeCssAttributesIEInternal(selector, attributesArray, styleSheet, ruleValidator);

    styleSheet = wpGetThemeStyleSheet();
    if (styleSheet && styleSheet != null) {
        removeCssAttributesIEInternal(selector, attributesArray, styleSheet, ruleValidator);
    }
}

function refreshGlobalCss(css, timeout) {
    if (isIE()) {
        refreshGlobalCssInternalIE(css, timeout, false);
    } else {
        refreshGlobalCssInternal(css, timeout, false);
    }
}

function refreshGlobalAndThemeCssInternal(themeCss, globalCss, timeout) {
    if (themeCss) {
        var newThemeStyle = document.createElement('style');
        //		setTimeout(function(){
        newThemeStyle.type = 'text/css';
        //			if(newThemeStyle.styleSheet)
        //				newThemeStyle.styleSheet.cssText = themeCss;
        //	    },0);
        jQuery(newThemeStyle).attr('id', 'newGlobalCssTheme');
        jQuery('head').append(newThemeStyle);
        jQuery(newThemeStyle).html(themeCss);
    }

    globalCss = globalCss || '';
    var newStyle = document.createElement('style');
    //	    setTimeout(function(){
    newStyle.type = 'text/css';
    if (newStyle.styleSheet) newStyle.styleSheet.cssText = globalCss;
    //	    },0);
    jQuery(newStyle).attr('id', 'newGlobalCss');
    jQuery('head').append(newStyle);
    jQuery(newStyle).html(globalCss);

    if (timeout == null) {
        timeout = 10;
    }
    if (timeout == 0) {
        removeOldCss();
        initComponents();
        return Promise.resolve();
    }
    return new Promise(function(resolve) {
        setTimeout(function() {
            removeOldCss();
            initComponents();
            resolve();
        }, timeout);
    });
}

function refreshGlobalCssInternal(css, timeout, nonThemeOnly, cssObject) {
    var firstIndex = -1;
    var endIndex = -1;
    if (nonThemeOnly == false && jQuery('#globalCssTheme').length > 0) {
        firstIndex = css.indexOf('/*SITE_THEME_BEGIN*/');
        endIndex = css.indexOf('/*SITE_THEME_END*/');
    }
    var theme = '';
    var nonTheme = css;
    if (firstIndex != -1 && endIndex != -1) {
        var prefix = css.substring(0, firstIndex);
        var suffix = css.substring(endIndex + '/*DUDAMOBILE_THEME_END*/'.length);
        nonTheme = prefix + suffix;
        theme = css.substring(firstIndex, endIndex + '/*DUDAMOBILE_THEME_END*/'.length);

        var newThemeStyle = document.createElement('style');
        jQuery(newThemeStyle).html(theme);
        jQuery(newThemeStyle).attr('id', 'newGlobalCssTheme');
        jQuery('head').append(newThemeStyle);
    }

    var newStyle = document.createElement('style');
    jQuery(newStyle).html(nonTheme);
    jQuery(newStyle).attr('id', 'newGlobalCss');
    jQuery('head').append(newStyle);

    if (timeout == null) {
        timeout = 10;
    }
    if (timeout == 0) {
        removeOldCss();
        initComponents();
    } else {
        setTimeout(function() {
            removeOldCss();
            initComponents();
        }, timeout);
    }

    //Refreshing Generated CSS if it is a style tag
    refreshGeneratedCss();
}

function refreshGeneratedCss() {
    var $generatedCssToRemove = $('link[href^="/_dm/s/rt/generate_css"]');
    if ($generatedCssToRemove.length > 0) {
        var newTimeStampSuffix = '&timestamp=' + new Date().getTime();
        var generatedCssHref = $generatedCssToRemove.attr('href');
        var timeStampIndex = generatedCssHref.indexOf('&timestamp');
        if (timeStampIndex !== -1) {
            generatedCssHref = generatedCssHref.substr(0, timeStampIndex) + '&timestamp=' + newTimeStampSuffix;
        } else {
            generatedCssHref = generatedCssHref + '&timestamp=' + newTimeStampSuffix;
        }
        var $newCss = $('<link type="text/css" rel="stylesheet" href="' + generatedCssHref + '"/>');

        $newCss.one('load', function() {
            $generatedCssToRemove.remove();
        });
        $generatedCssToRemove.after($newCss);
    }
}

function refreshGlobalCssInternalIE(css, timeout, nonThemeOnly) {
    var firstIndex = -1;
    var endIndex = -1;
    if (nonThemeOnly == false && jQuery('#globalCssTheme').length > 0) {
        firstIndex = css.indexOf('/*DUDAMOBILE_THEME_BEGIN*/');
        endIndex = css.indexOf('/*DUDAMOBILE_THEME_END*/');
    }
    var theme = '';
    var nonTheme = css;
    if (firstIndex != -1 && endIndex != -1) {
        var prefix = css.substring(0, firstIndex);
        var suffix = css.substring(endIndex + '/*DUDAMOBILE_THEME_END*/'.length);
        nonTheme = prefix + suffix;
        theme = css.substring(firstIndex, endIndex + '/*DUDAMOBILE_THEME_END*/'.length);

        var newThemeStyle = document.createElement('style');

        setTimeout(function() {
            newThemeStyle.type = 'text/css';
            newThemeStyle.styleSheet.cssText = theme;
        }, 0);

        jQuery(newThemeStyle).attr('id', 'newGlobalCssTheme');
        jQuery('head').append(newThemeStyle);
    }

    var newStyle = document.createElement('style');

    setTimeout(function() {
        newStyle.type = 'text/css';
        newStyle.styleSheet.cssText = nonTheme;
    }, 0);

    jQuery(newStyle).attr('id', 'newGlobalCss');
    jQuery('head').append(newStyle);

    if (timeout == null) {
        timeout = 10;
    }
    if (timeout == 0) {
        removeOldCss();
        initComponents();
    } else {
        setTimeout(function() {
            removeOldCss();
            initComponents();
        }, timeout);
    }
}

function refreshCss(css, timeout, isHeader, options) {
    options = options || {};
    var funcName = options.funcName;
    var newId = options.newId;

    isHeader = isHeader || false;
    var newStyle = document.createElement('style');

    jQuery(newStyle).html(css);
    jQuery(newStyle).attr('id', newId);
    jQuery('head').append(newStyle);
    if (timeout == null) {
        timeout = 10;
    }
    if (timeout == 0) {
        window[funcName](isHeader);
        initComponents();
    } else {
        setTimeout(funcName + '(' + isHeader + '); initComponents();', timeout);
    }
}

function refreshPageStyleCss(css, timeout, isHeader, isInner) {
    if (isInner) {
        return refreshInnerPageStyleCss(css, timeout, isHeader);
    }
    var newId = isHeader ? 'newheaderCss' : 'newpagestyle';
    var funcName = 'removeOldPageStyle';
    refreshCss(css, timeout, isHeader, { funcName: funcName, newId: newId });
}

function refreshPageStyleDeviceCss(css, timeout, isHeader, isInner) {
    if (isInner) {
        return refreshInnerPageStyleDeviceCss(css, timeout, isHeader);
    }
    var newId = isHeader ? 'newheaderDeviceCss' : 'newpagestyleDevice';
    var funcName = 'removeOldDevicePageStyle';
    refreshCss(css, timeout, isHeader, { funcName: funcName, newId: newId });
}

function refreshInnerPageStyleCss(css, timeout, isHeader) {
    var newId = 'newinnerPagesStyle';
    var funcName = 'removeOldInnerPageStyle';
    refreshCss(css, timeout, isHeader, { funcName: funcName, newId: newId });
}

function refreshInnerPageStyleDeviceCss(css, timeout, isHeader) {
    var newId = 'newinnerPagesStyleDevice';
    var funcName = 'removeOldDeviceInnerPageStyle';
    refreshCss(css, timeout, isHeader, { funcName: funcName, newId: newId });
}

function refreshGlobalCssAndShowLoading(css) {
    showLoadingDots();
    refreshGlobalCss(css, 3000);
}

function refreshGlobalCssAndShowLoadingNEW(css, timeout) {
    if (!timeout || timeout == null) timeout = 3000;
    showLoadingDotsNEW();
    refreshGlobalCss(css, timeout);
}

/**
 * @description: Initiate general components after the theme has changed
 */
function initComponents(dontCollapse) {
    if (!dontCollapse) {
        jQuery.DM.collapseNavigation();
    }
    jQuery.DM.restoreDefaultNavigationStyles();
    jQuery.DM.initNavbar(true);
}

_findCurrentNavText = function() {
    var hiddenNavElement = $("[id='hiddenNavPlaceHolder'] ul li:first").closest('#hiddenNavPlaceHolder');
    if (hiddenNavElement.size() > 0) {
        var currentLI = hiddenNavElement.find('li').filter(function() {
            return 'true' == $(this).attr('dmle_is_current_element');
        });
        if (currentLI.size() > 0) {
            return $(currentLI.get(0))
                .find('.navText:first')
                .text();
        }
    }
    return '';
};
_findCurrentNavId = function() {
    var hiddenNavElement = $("[id='hiddenNavPlaceHolder'] ul li:first").closest('#hiddenNavPlaceHolder');
    if (hiddenNavElement.size() > 0) {
        var currentLI = hiddenNavElement.find('li').filter(function() {
            return 'true' == $(this).attr('dmle_is_current_element');
        });
        if (currentLI.size() > 0) {
            return $(currentLI.get(0)).attr('id');
        }
    }
    return '';
};

function removeOldCss() {
    var oldStyle = $('#globalCss');
    var newStyle = $('#newGlobalCss');
    if (newStyle) {
        oldStyle.remove();
        newStyle.attr('id', 'globalCss');
    }
    var oldThemeStyle = document.getElementById('globalCssTheme');
    var newThemeStyle = document.getElementById('newGlobalCssTheme');
    if (newThemeStyle) {
        oldThemeStyle.parentNode.removeChild(oldThemeStyle);
        newThemeStyle.setAttribute('id', 'globalCssTheme');
    }
    hideLoading();

    var tempStyle = document.getElementById('tempCss');
    if (tempStyle && tempStyle != null) {
        tempStyle.parentNode.removeChild(tempStyle);
    }
}

function removeStyleAndReplace(oldStyleId, newStyleId) {
    var styleId = oldStyleId;
    var oldStyle = document.getElementById(styleId);
    var newStyle = document.getElementById(newStyleId);

    var refStyle = oldStyle || document.getElementById('customWidgetStyle');
    refStyle.parentNode.insertBefore(newStyle, refStyle.nextElementSibling);
    if (oldStyle) {
        oldStyle.parentNode.removeChild(oldStyle);
    }
    newStyle.setAttribute('id', styleId);

    hideLoading();

    var tempStyle = document.getElementById('tempCss');
    if (tempStyle != null) {
        tempStyle.parentNode.removeChild(tempStyle);
    }
}

function removeOldPageStyle(isHeader) {
    removeStyleAndReplace(isHeader ? 'headerCss' : 'pagestyle', isHeader ? 'newheaderCss' : 'newpagestyle');
}

function removeOldDevicePageStyle(isHeader) {
    removeStyleAndReplace(
        isHeader ? 'headerDeviceCss' : 'pagestyleDevice',
        isHeader ? 'newheaderDeviceCss' : 'newpagestyleDevice'
    );
}

function removeOldInnerPageStyle(isHeader) {
    isHeader = false;
    removeStyleAndReplace(isHeader ? 'headerCss' : 'innerPagesStyle', isHeader ? 'newheaderCss' : 'newinnerPagesStyle');
}

function removeOldDeviceInnerPageStyle(isHeader) {
    isHeader = false;
    removeStyleAndReplace(
        isHeader ? 'headerDeviceCss' : 'innerPagesStyleDevice',
        isHeader ? 'newheaderDeviceCss' : 'newinnerPagesStyleDevice'
    );
}

function updateLogoImage(src) {
    var div = document.getElementById('logo-div');

    if (div.style != null) {
        div.style.backgroundImage = 'none';
    }
    // div.setAttribute("style" , "background-image:none");
    jQuery('#logo-div').css('background-image', 'none');
    div.getElementsByTagName('img')[0].setAttribute('src', src);
}

function getLogoImageUrl() {
    try {
        var div = document.getElementById('logo-div');
        return div.getElementsByTagName('img')[0].src;
    } catch (e) {
        return '';
    }
}

function getLogoImage() {
    try {
        var div = document.getElementById('logo-div');
        return div.getElementsByTagName('img')[0];
    } catch (e) {
        return document.createElement('img');
    }
}

function getElementByID(targetID) {
    return document.getElementById(targetID);
}

function getHeader() {
    return document.getElementById('fw-head');
}
// check if the logo image from the theme is hidden
function isThemeLogoImageHidden(target) {
    var styleHidden;
    var bgHidden;
    var div = document.getElementById('logo-div');
    if (div != null && div.style != null && div.style.backgroundImage == 'none') {
        styleHidden = true;
    }

    //var bg = getElementProperty("#dm div.fw-head .fw-logo","background-image");

    var bg = getElementProperty(target, 'background-image');
    if (bg != null && bg.indexOf('editor/images/w/transparent.gif') != -1) {
        bgHidden = true;
    }

    if (bgHidden || styleHidden) {
        return true;
    } else {
        return false;
    }
}

function resetLogOImage(target) {
    var div = document.getElementById('logo-div');
    if (div != null) {
        // remove the inline style (in case we added it to change the image)
        div.getAttribute('style');
        div.removeAttribute('style');
        //console.log(div.getAttribute("style"));
        // remove the rule hiding the original bg image (in case its in the global css, after refresh for example)

        var attributesToRemove = ['background-image'];
        //	removeCssAttributes("#dm div.fw-head .fw-logo",attributesToRemove);
        removeCssAttributes(target, attributesToRemove);
        var img = div.getElementsByTagName('img')[0];
        if (img != null) {
            img.setAttribute('src', '/editor/images/w/transparent.gif');
        }
    }
}

/**
 * sets the new 'more options' text parameter
 * @param newText - the new text
 * @returns {void}
 */
function setDMAjaxMoreNavigationParameter(newText) {
    Parameters.NavigationAreaParams.MoreButtonText = newText;
}

function setDMAjaxNavSize(newSize) {
    Parameters.NavigationAreaParams.NavbarSize = newSize;
    if (Parameters.NavigationAreaParams.NavbarSize == -1 || $.browser.opera) {
        Parameters.NavigationAreaParams.NavbarSize = Number.MAX_VALUE;
    }
}

/**
 * sets the new 'less options' text parameter
 * @param newText - the new text
 * @returns {void}
 */
function setDMAjaxLessNavigationParameter(newText) {
    Parameters.NavigationAreaParams.LessButtonText = newText;
}

/**
 * sets the new 'back to home' text parameter
 * @param newText - the new text
 * @returns {void}
 */
function setDMAjaxBackToHomeParameter(newText) {
    Parameters.HomeLinkText = newText;
}

function getDMAjaxBackToHomeParameter() {
    return Parameters.HomeLinkText;
}

/**
 * return true if this theme supports 'back to home' text
 * @returns {boolean}
 */
function isBackToHomeTextVisible() {
    // create a dummy element with the same selector of the "back to home" text element
    var dummy = jQuery('<div id="dm"><a class="dmHome"><span class="text">home</span></a></div>');
    jQuery('body').append(dummy);
    // get the element display value
    var displayValue = jQuery('#dm .dmHome .text').css('display');
    dummy.remove();
    return displayValue != 'none';
}

/**
 * return true if this site has more/less buttons
 * @returns {boolean}
 */
function isSiteHasMoreLessButtons() {
    return jQuery.DM.hasMoreLessButtons();
}

function loadStoreScript(storeId) {
    window.ecwid_script_defer = true;
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = window.rtCommonProps['ecommerce.ecwid.script'] + '?' + storeId;
    $(script).appendTo($('body'));
}

var documentStyles = {
    queryCommandState: function(command) {
        try {
            return document.queryCommandState(command);
        } catch (e) {
            return false;
        }
    },
    queryCommandValue: function(command) {
        try {
            return document.queryCommandValue(command);
        } catch (e) {
            return null;
        }
    },
    dmCss: function(el, key, value) {
        if (value != '' && !value) {
            return el.css(key);
        }
        if (value == '') {
            return el.css(key, '');
        } else {
            var isImportant = value.indexOf('!important') != -1;
            if (isImportant) {
                value = value.replace('!important', '');
                el.css(key, '');
                el.each(function() {
                    var style = el.attr('style');
                    el.attr('style', (style ? style + ';' : '') + key + ': ' + value + ' !important');
                });
                return el;
            } else {
                return el.css(key, value);
            }
        }
    }
};
