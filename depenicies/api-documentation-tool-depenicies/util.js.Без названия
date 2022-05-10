function uppercaseThis(str) {
  return str.toUpperCase();
}

function toCamelCase(str) {
  str = str.replace(/-(.)/g, uppercaseThis);
  str = str.replace(/(-)/g, "");
  return str;
}

function displayDeletedMessage(msg) {
  var d = document.getElementById("elementsWereDeleted");
  if(d != null) {
    d.innerHTML = msg;
  }

}

function replaceAll(Source, stringToFind, stringToReplace) {
  var temp = Source;
  var index = temp.indexOf(stringToFind);
  while(index != -1) {
    temp = temp.replace(stringToFind, stringToReplace);
    index = temp.indexOf(stringToFind);
  }
  return temp;
}

// given a class name, style sheet id and attribute, get the attribute value
// from the style sheet
function getAttributeByClassName(selector, attribute, styleSheetId) {

  // get stylesheet
  var styleSheet = getPageStyleSheet(styleSheetId);

  return getAttributeByClassNameFromSheet(selector, attribute, styleSheet);
}

function isIE() {
  if(navigator.userAgent.indexOf('MSIE') != -1) {
    // Using IE
    return true;
  } else {
    return false;
  }

}

function getAttributeByClassNameFromSheetIE(selector, attribute, styleSheet) {
  // look for the selector in the existing rules
  for(i = 0; i < styleSheet.rules.length; i++) {

    // get rule
    var rule = styleSheet.rules[i];

    var ruleSelector = rule.selectorText.toLowerCase();
    ruleSelector = replaceAll(ruleSelector, "*", "");
    var mySelector = selector.toLowerCase();
    mySelector = replaceAll(mySelector, "*", "");

    if(ruleSelector === mySelector) {
      // we found the rule, now get the attribute
      return rule.style.getAttribute(attribute);
    }

  }
  return;

}

function getAttributeByClassNameFromSheet(selector, attribute, styleSheet) {
  if(isIE()) {
    return getAttributeByClassNameFromSheetIE(selector, attribute,
      styleSheet);
  }
  // look for the selector in the existing rules
  for(i = 0; i < styleSheet.cssRules.length; i++) {
    // get rule
    var rule = styleSheet.cssRules[i];
    if(rule.constructor == CSSStyleRule) {
      // this is a style rule

      var ruleSelector = rule.selectorText.toLowerCase();
      ruleSelector = replaceAll(ruleSelector, "*", "");
      var mySelector = selector.toLowerCase();
      mySelector = replaceAll(mySelector, "*", "");

      if(ruleSelector === mySelector) {
        // we found the rule, now get the attribute

        return rule.style.getPropertyValue(attribute);
      }
    }
  }

}

// get the page style sheet as a styleSheet object
function getPageStyleSheet(styleSheetId) {
  {
    // go over the stylesheets, and get the one inside "pageStyle" or
    // "headerStyle"
    for(i = 0; i < document.styleSheets.length; i++) {
      // get the owner node
      var node = document.styleSheets[i].ownerNode;
      if(node != null && (node !== undefined)) {

        // get node parent
        var parent = node.parentNode;

        if(parent != null && (parent !== undefined)) {
          // get parent id
          var id = parent.id;
          if(id != null && (id !== undefined)) {
            if(id === styleSheetId) {
              // we found the stylesheet
              return document.styleSheets[i];
            }
          }

        }
      }
    }
    return null;
  }
}

function validateAccountEmailAddress(address) {
  try {
    var emailRegEx = /(^[_A-Za-z0-9-]+(\.[_A-Za-z0-9-+]+)*@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*(\.[A-Za-z]{2,})$)/;
    return emailRegEx.test(address);
  } catch(e) {}
}

function validateAccountfields(address, password, confirmPassword) {
  try {
    if(password == '' || confirmPassword == '' || address == '') {
      return false;
    } else {
      return true;
    }
  } catch(e) {}
}

function validateAccountPasswords(password, confirmPassword) {
  try {
    if(password == confirmPassword) {
      return true;
    } else {
      return false;
    }
  } catch(e) {}
}

function validateAccountMsg(msgID) {
  try {
    switch(msgID) {
      case 'NO_EMAIL_ERROR':
        return dmStr["ui.login.validation.1"];

      case 'NO_PASSWORD_ERROR':
        return dmStr["ui.login.validation.2"];

      case 'NO_CONFIRM_ERROR':
        return dmStr["ui.login.validation.3"];

      case 'DIFFER_PASSWORDS_ERROR':
        return dmStr["ui.login.validation.4"];

      case 'INVALID_EMAIL_ERROR':
        return dmStr["ui.login.validation.5"];

      case 'SHORT_PASSWORDS_ERROR':
        return dmStr["ui.login.validation.6"];

      case 'TAKEN_EMAIL_ERROR':
        return dmStr["ui.login.validation.7"];

      case 'NO_USER_TYPE_ERROR':
        return dmStr["ui.login.validation.8"];
    }
  } catch(e) {
    return '';
  }
}

function alignImages() {
  try {
    jQuery(".dmBody img").filter(function() {
      return(jQuery(this).css("display") != "none") && (jQuery(this).width() <= 140);
    }).css("display", "inline").css("margin-right", "5px");
    jQuery(".dmBody img").filter(function() {
      return(jQuery(this).css("display") != "none") && (jQuery(this).width() > 140);
    }).css("display", "block").css("margin-right", "auto").css("margin-left", "auto");
    jQuery(".dmContent img").css("margin-top", "5px").css("margin-bottom", "5px");
  } catch(e) {}
}

function disableLinks() {
  try {
    var js = "return false;";
    jQuery(".dmBody a, .dmBody input[type='submit'] ,.dmBody input[type='image'], .dmBody button").attr("onclick", js);
    jQuery(".dmHeader a, .dmBody input[type='submit'] ,.dmHeader input[type='image'], .dmHeader button").attr("onclick", js);
    jQuery(".dmFooter a, .dmFooter input[type='submit'] ,.dmFooter input[type='image'], .dmFooter button").attr("onclick", js);

  } catch(e) {}
}

function designTimeActions() {
  alignImages();
  disableLinks();
}

/**
 * use javascript to create the plus one element (otherwise it doesn't work on IE8)
 * @param url - the url to publish to world
 * @param id - the wrapper to build the plus one inside
 */
function generateGooglePlusOneButton(url, id) {
  var d = document.createElement("div");
  d.innerHTML = "<g:plusone size=\"tall\" href=\"" + url + "\"></g:plusone>";
  jQuery('#' + id).html("");
  jQuery('#' + id).append($(d));
  gapi.plusone.go();
}

/**
 * set a cursor position on element
 * @param selector - the element jquery selector
 * @param pos - the target position
 */
function setSelectionRange(id, selectionStart, selectionEnd) {
  var input = document.getElementById(id);
  // IE 
  if(input.createTextRange) {
    var range = input.createTextRange();
    range.collapse(true);
    range.moveEnd('character', selectionEnd);
    range.moveStart('character', selectionStart);
    range.select();
    // real browsers
  } else if(input.setSelectionRange) {
    input.focus();
    input.setSelectionRange(selectionStart, selectionEnd);
  }
}

function animateElement(id, show) {
  if(show) {
    $('#' + id).slideDown('slow', function() {
      // Animation complete.
    });
  } else {
    $('#' + id).slideUp('slow', function() {
      // Animation complete.
    });
  }
}

function fadeWindow(id, show) {
  if(show) {
    $('#' + id).fadeIn(500);
  } else {
    $('#' + id).fadeOut(500);
  }
}

$.fn.dmCss = function(key, value) {
  if(!value) {
    return $(this).css(key);
  }
  if(value == "") {
    return $(this).css(key, "");
  } else {
    var isImportant = value.indexOf("!important") != -1;
    if(isImportant) {
      value = value.replace("!important", "");
      $(this).css(key, "");
      $(this).each(function() {
        var style = $(this).attr("style");
        $(this).attr("style", (style ? style + ';' : '') + key + ': ' + value + ' !important');
      });
      return $(this);
    } else {
      return $(this).css(key, value);
    }
  }
};