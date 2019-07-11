"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var _reactAccessibleAccor = reactAccessibleAccordion,
    Accordion = _reactAccessibleAccor.Accordion,
    AccordionItem = _reactAccessibleAccor.AccordionItem,
    AccordionItemHeading = _reactAccessibleAccor.AccordionItemHeading,
    AccordionItemPanel = _reactAccessibleAccor.AccordionItemPanel,
    AccordionItemButton = _reactAccessibleAccor.AccordionItemButton;


var teirsData = tiers;

var plansAndFeaturesData = plansAndFeatures;

// used to show offer options in contact form

var OfferOptions = function (_React$Component) {
    _inherits(OfferOptions, _React$Component);

    function OfferOptions(props) {
        _classCallCheck(this, OfferOptions);

        return _possibleConstructorReturn(this, (OfferOptions.__proto__ || Object.getPrototypeOf(OfferOptions)).call(this, props));

        // // console.log("props in OfferOptions", props);
    }

    _createClass(OfferOptions, [{
        key: "render",
        value: function render() {
            var _this2 = this;

            var offerOptions = [];

            this.props.item.offer_options.forEach(function (option) {

                var ref = option.alias;

                // // console.log("this", this, "this[ref]", this[ref]);

                offerOptions.push(React.createElement(
                    React.Fragment,
                    null,
                    _this2.props.requiredFields.indexOf(option.alias) != -1 ? React.createElement(
                        React.Fragment,
                        null,
                        React.createElement("input", { type: option.type, className: "offer-options", ref: _this2[ref], name: option.alias, value: option.value, onChange: function onChange() {
                                return _this2.props.handleInputChange(_this2.props.item, event);
                            }, required: true }),
                        " ",
                        React.createElement(
                            "span",
                            null,
                            option.value,
                            "*"
                        ),
                        React.createElement("br", null)
                    ) : React.createElement(
                        React.Fragment,
                        null,
                        React.createElement("input", { type: option.type, className: "offer-options", ref: ref, name: option.alias, value: option.value, onChange: function onChange() {
                                return _this2.props.handleInputChange(_this2.props.item, event);
                            } }),
                        React.createElement(
                            "span",
                            null,
                            option.value
                        ),
                        React.createElement("br", null)
                    )
                ));
            });

            return React.createElement(
                React.Fragment,
                null,
                offerOptions
            );
        }
    }]);

    return OfferOptions;
}(React.Component);

var SelectTag = function (_React$Component2) {
    _inherits(SelectTag, _React$Component2);

    function SelectTag(props) {
        _classCallCheck(this, SelectTag);

        return _possibleConstructorReturn(this, (SelectTag.__proto__ || Object.getPrototypeOf(SelectTag)).call(this, props));

        // // console.log("props in OfferOptions", props);
    }

    _createClass(SelectTag, [{
        key: "render",
        value: function render() {
            var _this4 = this;

            return React.createElement(
                React.Fragment,
                null,
                this.props.requiredFields.indexOf(this.props.item.alias.label) != -1 ? React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        "span",
                        { className: "form-label" },
                        this.props.item.label,
                        "*"
                    ),
                    React.createElement("br", null),
                    React.createElement(
                        "select",
                        { className: this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", name: this.props.item.alias.label, onChange: function onChange() {
                                return _this4.props.handleInputChange(_this4.props.item, event);
                            }, required: true },
                        React.createElement(
                            "option",
                            { value: "Select", selected: "selected" },
                            this.props.item.selectMsg
                        ),
                        this.props.item.options.map(function (opt) {
                            return React.createElement(
                                "option",
                                { value: opt },
                                opt
                            );
                        })
                    )
                ) : React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        "span",
                        { className: "form-label" },
                        this.props.item.label
                    ),
                    React.createElement("br", null),
                    React.createElement(
                        "select",
                        { className: this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", name: this.props.item.alias.label, onChange: function onChange() {
                                return _this4.props.handleInputChange(_this4.props.item, event);
                            } },
                        React.createElement(
                            "option",
                            { value: "Select", selected: "selected" },
                            this.props.item.selectMsg
                        ),
                        this.props.item.options.map(function (opt) {
                            return React.createElement(
                                "option",
                                { value: opt },
                                opt
                            );
                        })
                    )
                )
            );
        }
    }]);

    return SelectTag;
}(React.Component);

// handles dynamic json to configure contact form input


var ContactFormInputs = function (_React$Component3) {
    _inherits(ContactFormInputs, _React$Component3);

    function ContactFormInputs(props) {
        _classCallCheck(this, ContactFormInputs);

        // this.state = contactForm.formState;

        // this.state = Object.assign(this.state, {formInputs: contactForm.formInputs});

        // create a ref to store the textInput DOM element
        var _this5 = _possibleConstructorReturn(this, (ContactFormInputs.__proto__ || Object.getPrototypeOf(ContactFormInputs)).call(this, props));

        _this5.emailInput = React.createRef();

        _this5.taInput = React.createRef();

        _this5.state = {};

        // contactForm.formInputs.forEach((item) => {

        //     // create alias for offer_options
        //     if (item.type=="offer_options") {

        //         this.state = Object.assign(this.state, {"optionsAlias": item.alias.label})

        //         item.offer_options.forEach((opt) => {

        //         let ref = opt.alias;

        //         this[ref] = React.createRef(); 
        //         });
        //     }

        //     // check alias type and set status based on that
        //     if (item.alias) {
        //         if ((item.alias.valueType).toLowerCase() == "string") {
        //             this.state[item.alias.label] = "";
        //         } else if ((item.alias.valueType).toLowerCase() == "array") {
        //             if (item.alias.arrayType == "requiredFields")
        //                 this.state[item.alias.label] = item[item.alias.label];
        //             else 
        //             this.state[item.alias.label] = [];
        //         } else if ((item.alias.valueType).toLowerCase() == "number") {
        //             this.state[item.alias.label] = 0;
        //         }
        //     }
        // });

        // // set endpoint
        // this.state.endPoint = contactForm.endPoint;

        // this.state.disabled = contactForm.disabled;

        // // console.log("props ibn ContactFormInputs", props);

        // // console.log("this.state in contact form", this.state);

        // set contact form initial state
        _this5.setContactFormState(contactForm.formInputs);
        return _this5;
    }

    // sets contact form state


    _createClass(ContactFormInputs, [{
        key: "setContactFormState",
        value: function setContactFormState(data, onSubmitRes, resData) {
            var _this6 = this;

            data.forEach(function (item) {

                // create alias for offer_options
                if (item.type == "offer_options") {

                    _this6.state = Object.assign(_this6.state, { "optionsAlias": item.alias.label });

                    item.offer_options.forEach(function (opt) {

                        var ref = opt.alias;

                        // let refObj = React.createRef();

                        // clear off checkbox
                        if (_this6[ref] && _this6[ref].current && _this6[ref].current.checked == true) {
                            _this6[ref].current.checked = false;
                        } else {

                            _this6[ref] = React.createRef();
                        }
                    });
                }

                // check alias type and set status based on that
                if (item.alias) {
                    if (item.alias.valueType.toLowerCase() == "string") {
                        _this6.state[item.alias.label] = "";
                    } else if (item.alias.valueType.toLowerCase() == "array") {
                        if (item.alias.arrayType == "requiredFields") _this6.state[item.alias.label] = item[item.alias.label];else _this6.state[item.alias.label] = [];
                    } else if (item.alias.valueType.toLowerCase() == "number") {
                        _this6.state[item.alias.label] = 0;
                    }
                }
            });

            // set endpoint
            this.state.endPoint = contactForm.endPoint;

            this.state.disabled = contactForm.disabled;

            this.state.notificationDuration = contactForm.notificationDuration;

            this.state.submit = false;

            if (onSubmitRes) {

                // this is from successful contact api response

                this.state.submitRes = "";
                this.state.submitRes = React.createElement(
                    "li",
                    { id: "notification", className: "pure-notification-message pure-notification-success", style: { animationDuration: '6000ms' } },
                    React.createElement(
                        "svg",
                        { "class": "icon icon--check", viewBox: "0 0 20 20", width: "22", height: "22", xmlns: "http://www.w3.org/2000/svg" },
                        React.createElement("path", { d: "M4 10l4 5 9-11", fill: "none", stroke: "currentColor", "stroke-width": "1.1" })
                    ),
                    React.createElement(
                        "span",
                        null,
                        contactForm.submitRes
                    ),
                    React.createElement("div", { role: "presentation", className: "pure-notification-progress", style: { animationDuration: '6000ms' } })
                );
            } else if (resData) {

                // this is used to show err msg from backend
                // get the keys of resData
                var resDatakeys = Object.keys(resData);

                var errNode = [];

                for (var key in resDatakeys) {

                    errNode.push(React.createElement(
                        "span",
                        null,
                        key,
                        ": ",
                        resDatakeys[key]
                    ));
                }

                this.state.submitRes = React.createElement(
                    "li",
                    { id: "notification", className: "pure-notification-message pure-notification-success", style: { animationDuration: '6000ms' } },
                    React.createElement(
                        "svg",
                        { "class": "icon icon--check", viewBox: "0 0 20 20", width: "22", height: "22", xmlns: "http://www.w3.org/2000/svg" },
                        React.createElement("path", { d: "M4 10l4 5 9-11", fill: "none", stroke: "currentColor", "stroke-width": "1.1" })
                    ),
                    React.createElement(
                        "span",
                        null,
                        errNode
                    ),
                    React.createElement("div", { role: "presentation", className: "pure-notification-progress", style: { animationDuration: '6000ms' } })
                );
            } else {
                this.state.submitRes = "";
            }
            // // console.log("this.state in contact form", this.state);
        }
    }, {
        key: "setButtonDisability",
        value: function setButtonDisability(item, event) {
            var _this7 = this;

            var disabledCount = 0;

            // check if all the required fields are entered and enable submit  button
            this.state.requiredFields.forEach(function (field) {

                // // console.log("checking if value exists to remove disable option on button", this.state[field]);

                // // if value exists, set disabled state to false, else true 
                // // offer_options is an array
                // if (this.state[field] == "" || this.state[field] == undefined || (typeof this.state[field] == "object" && this.state[field].indexOf(field) == -1)) {

                //     disabledCount++;
                // }
                // if value exists, set disabled state to false, else true 
                // offer_options is an array
                if (_this7.state[field] == "" || _this7.state[field] == undefined || _this7.state[field] == "Select" || _this7.state[_this7.state.optionsAlias].length == 0) {

                    disabledCount++;
                }
            });

            if (this.emailInput.current.validity.valid == false) {
                disabledCount++;
            }

            // var emailElem = document.getElementById('email');

            // if (emailElem.validity.valid == false) {
            //     disabledCount++;
            // }

            if (disabledCount > 0) {
                // this.state.disabled = true;
                disabledCount = 0;

                this.setState({
                    disabled: true
                });
            } else {
                // this.state.disabled = false;
                this.setState({
                    disabled: false
                });
            }
        }
    }, {
        key: "handleInputChange",
        value: function handleInputChange(item, event) {

            // // console.log("selected item", item, "value in handleInputChange", event.target.value);

            // // console.log("this.emailInput", this.emailInput);

            // if offer_options are selected, multiple checked fields are pushed and set into state
            if (item.type == "offer_options") {

                var updatedOffrOpts = this.state[item.alias.label];

                // if one of the offer options are checked, push only if index == -1 
                if (event.target.checked == true) {

                    if (updatedOffrOpts.indexOf(event.target.value) == -1) {
                        updatedOffrOpts.push(event.target.value);
                    }
                } else {

                    // remove unchecked element from the array and set it into state
                    if (updatedOffrOpts.indexOf(event.target.value) != -1) {
                        updatedOffrOpts.splice(updatedOffrOpts.indexOf(event.target.value), 1);
                    }
                }

                this.setState(_defineProperty({}, item.alias.label, updatedOffrOpts), function () {

                    // // console.log("state in handleInputChange callback", this.state); 
                    this.setButtonDisability(item, event);
                });
            } else {

                this.setState(_defineProperty({}, item.alias.label, event.target.value), function () {

                    // // console.log("state in handleInputChange callback", this.state); 
                    this.setButtonDisability(item, event);
                });
            }
        }
    }, {
        key: "submitContactForm",
        value: function submitContactForm() {
            var _this8 = this;

            // // console.log("in submitForm func, state is::", this.state);

            var reqBody = Object.assign({}, this.state);

            delete reqBody.requiredFields;

            delete reqBody.endPoint;

            delete reqBody.disabled;

            delete reqBody.formInputs;

            delete reqBody.optionsAlias;

            delete reqBody.notificationDuration;

            delete reqBody.submit;

            delete reqBody.submitRes;

            // // console.log("contact post request body", this.state);

            var submitResNode = React.createElement(
                "li",
                { id: "notification", className: "pure-notification-message pure-notification-success", style: { animationDuration: '6000ms' } },
                React.createElement(
                    "svg",
                    { "class": "icon icon--check", viewBox: "0 0 20 20", width: "22", height: "22", xmlns: "http://www.w3.org/2000/svg" },
                    React.createElement("path", { d: "M4 10l4 5 9-11", fill: "none", stroke: "currentColor", "stroke-width": "1.1" })
                ),
                React.createElement(
                    "span",
                    null,
                    contactForm.loadingMsg
                ),
                React.createElement("div", { role: "presentation", className: "pure-notification-progress", style: { animationDuration: '6000ms' } })
            );

            // show loading msg on cclicking submit
            this.setState({ submitRes: submitResNode });

            fetch(this.state.endPoint, {
                method: 'POST',
                headers: {
                    "Content-type": "application/json;"
                },
                body: JSON.stringify(reqBody)
            }).then(function (response) {
                return response.json();
            }).then(function (result) {

                // if (result.status == "ok") {

                // console.log("result after post request", result);

                // TODO: ADD ERROR HANDLING POPUP AS WELL BASED ON RESPONSE ENDPOINT

                // clear off textarea using ref
                // // console.log("this.taInput", this.taInput);
                _this8.taInput.current.value = "";

                // set contact form initial state
                _this8.setContactFormState(contactForm.formInputs, true);

                // restore form to initial state
                _this8.setState(_this8.state);

                setTimeout(function () {
                    this.setState({ submitRes: "" });
                }.bind(_this8), _this8.state.notificationDuration);
                // } 
                // else {

                //     // this implies there has been an error response from server, do not reset form but rather show err msg
                //     this.setContactFormState(contactForm.formInputs, false, result);
                // }
            }, function (error) {

                console.log("error in submitting contact form", error);
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _this9 = this;

            var contactFormInputs = [];

            this.props.formInputs.forEach(function (item, i) {

                // console.log("item, i", item, i);
                if (item.type == "text" || item.type == "number" || item.type == "radio") {

                    // console.log("item.type is text");

                    contactFormInputs.push(React.createElement(
                        "div",
                        { className: "pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 contact-input" },
                        _this9.state.requiredFields.indexOf(item.alias.label) != -1 ? React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                "span",
                                { className: "form-label" },
                                item.label,
                                "*"
                            ),
                            React.createElement("br", null),
                            React.createElement("input", { className: _this9.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", type: item.type, placeholder: item.placeholder,
                                name: item.alias.label, value: _this9.state[item.alias.label], onChange: function onChange() {
                                    return _this9.handleInputChange(item, event);
                                }, required: true })
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                "span",
                                { className: "form-label" },
                                item.label
                            ),
                            React.createElement("br", null),
                            React.createElement("input", { className: _this9.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", type: item.type, placeholder: item.placeholder,
                                name: item.alias.label, value: _this9.state[item.alias.label], onChange: function onChange() {
                                    return _this9.handleInputChange(item, event);
                                } })
                        )
                    ));
                }

                if (item.type == "email") {

                    // console.log("item.type is text");

                    var emailVal = _this9.state[item.alias.label];

                    contactFormInputs.push(React.createElement(
                        "div",
                        { className: "pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 contact-input" },
                        _this9.state.requiredFields.indexOf(item.alias.label) != -1 ? React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                "span",
                                { className: "form-label" },
                                item.label,
                                "*"
                            ),
                            React.createElement("br", null),
                            React.createElement("input", { className: _this9.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", ref: _this9.emailInput, type: item.type, placeholder: item.placeholder,
                                id: "email", name: item.alias.label, value: emailVal, onChange: function onChange() {
                                    return _this9.handleInputChange(item, event);
                                }, required: true })
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                "span",
                                { className: "form-label" },
                                item.label
                            ),
                            React.createElement("br", null),
                            React.createElement("input", { className: _this9.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", ref: _this9.emailInput, type: item.type, placeholder: item.placeholder,
                                id: "email", name: item.alias, value: emailVal, onChange: function onChange() {
                                    return _this9.handleInputChange(item, event);
                                } })
                        )
                    ));
                }

                // for dropdown
                if (item.type == "dropdown") {
                    contactFormInputs.push(React.createElement(
                        "div",
                        { className: "pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 contact-input" },
                        React.createElement(SelectTag, { item: item, requiredFields: _this9.state.requiredFields, accordionView: _this9.props.accordionView, handleInputChange: function handleInputChange() {
                                return _this9.handleInputChange(item, event);
                            } })
                    ));
                }

                // for checkbox group
                if (item.type == "offer_options") {

                    // console.log("item.type is offer_options");


                    var offerOptions = [];

                    item.offer_options.forEach(function (option) {

                        var ref = option.alias;

                        // console.log("this", this, "this[ref]", this[option.alias]);

                        offerOptions.push(React.createElement(
                            React.Fragment,
                            null,
                            _this9.state.requiredFields.indexOf(option.alias) != -1 ? React.createElement(
                                React.Fragment,
                                null,
                                React.createElement("input", { type: option.type, className: "offer-options", ref: _this9[ref], name: option.alias, value: option.value, onChange: function onChange() {
                                        return _this9.handleInputChange(item, event);
                                    }, required: true }),
                                " ",
                                React.createElement(
                                    "span",
                                    null,
                                    option.value,
                                    "*"
                                ),
                                React.createElement("br", null)
                            ) : React.createElement(
                                React.Fragment,
                                null,
                                React.createElement("input", { type: option.type, className: "offer-options", ref: _this9[ref], name: option.alias, value: option.value, onChange: function onChange() {
                                        return _this9.handleInputChange(item, event);
                                    } }),
                                React.createElement(
                                    "span",
                                    null,
                                    option.value
                                ),
                                React.createElement("br", null)
                            )
                        ));
                    });

                    contactFormInputs.push(React.createElement(
                        "div",
                        { className: "pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 offer-options" },
                        React.createElement(
                            "span",
                            { "class": "optn-rqd-msg" },
                            item.optionsRequiredMsg
                        ),
                        React.createElement("br", null),
                        offerOptions
                    ));
                }

                if (item.type == "text_area") {

                    // console.log("item.type is text_area");

                    contactFormInputs.push(React.createElement(
                        "div",
                        { className: "pure-u-xs-1 pure-u-sm-1-3 pure-u-md-1-3 pure-u-lg-1-3 pure-u-xl-1-3 contact-input" },
                        _this9.state.requiredFields.indexOf(item.alias.label) != -1 ? React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                "span",
                                { className: "form-label-desc" },
                                item.label,
                                "*"
                            ),
                            React.createElement("textarea", { className: "text-area-tg", rows: "5", cols: "50", ref: _this9.taInput, placeholder: item.placeholder, onChange: function onChange() {
                                    return _this9.handleInputChange(item, event);
                                }, required: true })
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                "span",
                                { className: "form-label-desc" },
                                item.label
                            ),
                            React.createElement("textarea", { className: "text-area-tg", rows: "5", cols: "50", ref: _this9.taInput, placeholder: item.placeholder, onChange: function onChange() {
                                    return _this9.handleInputChange(item, event);
                                } })
                        )
                    ));
                }
            });

            return React.createElement(
                React.Fragment,
                null,
                React.createElement(
                    "div",
                    { className: "pure-g-r" },
                    contactFormInputs
                ),
                React.createElement(
                    "div",
                    { className: "contact-input" },
                    React.createElement(
                        "button",
                        { className: "ct-btn back-to-plans-btn-accrd", onClick: function onClick() {
                                return _this9.props.contactFormToggle();
                            } },
                        React.createElement(
                            "div",
                            { className: "back-btn-action-link-lg-dtl" },
                            React.createElement(
                                "svg",
                                { className: "ct-btn-svg", viewBox: "0 0 20 20", xmlns: "http://www.w3.org/2000/svg" },
                                React.createElement("path", { d: "M13 16l-6-6 6-6", fill: "none", stroke: "red", "stroke-width": "1.03" })
                            ),
                            this.props.toggleContactFormText
                        )
                    ),
                    React.createElement(
                        "button",
                        { className: "ct-btn contact-us-btn-xs ct-btn-2", disabled: this.state.disabled, onClick: function onClick() {
                                return _this9.submitContactForm();
                            } },
                        this.props.submitContactFormText
                    )
                ),
                React.createElement(
                    "aside",
                    { className: "pure-notification-container" },
                    React.createElement(
                        "ul",
                        null,
                        this.state.submitRes ? this.state.submitRes : ''
                    )
                )
            );
        }
    }]);

    return ContactFormInputs;
}(React.Component);

// tooltip class used in detail component


var Tooltip = function (_React$Component4) {
    _inherits(Tooltip, _React$Component4);

    function Tooltip(props) {
        _classCallCheck(this, Tooltip);

        var _this10 = _possibleConstructorReturn(this, (Tooltip.__proto__ || Object.getPrototypeOf(Tooltip)).call(this, props));

        _this10.state = {
            displayTooltip: false
        };
        _this10.hideTooltip = _this10.hideTooltip.bind(_this10);
        _this10.showTooltip = _this10.showTooltip.bind(_this10);
        return _this10;
    }

    _createClass(Tooltip, [{
        key: "hideTooltip",
        value: function hideTooltip() {
            this.setState({ displayTooltip: false });
        }
    }, {
        key: "showTooltip",
        value: function showTooltip() {
            this.setState({ displayTooltip: true });
        }
    }, {
        key: "render",
        value: function render() {
            var message = this.props.message;
            var position = this.props.position;
            return React.createElement(
                "span",
                { className: "tooltip",
                    onMouseLeave: this.hideTooltip
                },
                this.state.displayTooltip && React.createElement(
                    "div",
                    { className: "tooltip-bubble tooltip-" + position },
                    React.createElement(
                        "div",
                        { className: "tooltip-message" },
                        message
                    )
                ),
                React.createElement(
                    "span",
                    {
                        className: "tooltip-trigger",
                        onMouseOver: this.showTooltip
                    },
                    this.props.children
                )
            );
        }
    }]);

    return Tooltip;
}(React.Component);

// use this to show data about each tier in detailed view which also has tooltip for category feature


var DetailCategoryFeatures = function (_React$Component5) {
    _inherits(DetailCategoryFeatures, _React$Component5);

    function DetailCategoryFeatures(props) {
        _classCallCheck(this, DetailCategoryFeatures);

        return _possibleConstructorReturn(this, (DetailCategoryFeatures.__proto__ || Object.getPrototypeOf(DetailCategoryFeatures)).call(this, props));
    }

    _createClass(DetailCategoryFeatures, [{
        key: "render",
        value: function render() {

            var val = void 0;

            var detailCategoryFeatures = [];

            for (var i = 0; i < this.props.tiers.length; i++) {

                val = this.props.tiers[i].name;

                detailCategoryFeatures.push(React.createElement(
                    "div",
                    { className: "pure-u-1-4 category-feature" },
                    this.props.item.values[val].toLowerCase() == "yes" ? React.createElement(
                        "svg",
                        { "class": "c-check", xmlns: "http://www.w3.org/2000/svg", viewBox: "-255 347 100 100" },
                        React.createElement("title", null),
                        React.createElement("path", { d: "M-217.1 431.8c-1 1.2-2.6 2.2-4 2.3-1.4.1-3-.8-4.3-1.9l-27.5-24.5 7.8-8.7 23.2 20.6 54.6-61.7 8.6 7.9-58.4 66z" })
                    ) : React.createElement(
                        "div",
                        { className: "category-name" },
                        this.props.item.values[val]
                    )
                ));
            }

            return React.createElement(
                React.Fragment,
                null,
                detailCategoryFeatures
            );
        }
    }]);

    return DetailCategoryFeatures;
}(React.Component);

// contact form 


var ContactForm = function (_React$Component6) {
    _inherits(ContactForm, _React$Component6);

    function ContactForm(props) {
        _classCallCheck(this, ContactForm);

        var _this12 = _possibleConstructorReturn(this, (ContactForm.__proto__ || Object.getPrototypeOf(ContactForm)).call(this, props));

        _this12.state = contactForm.formState;
        return _this12;
    }

    _createClass(ContactForm, [{
        key: "render",
        value: function render() {
            var _this13 = this;

            return React.createElement(
                React.Fragment,
                null,
                React.createElement(
                    "div",
                    { id: "contact-form", className: "contact-form-container" },
                    React.createElement(
                        "div",
                        { className: this.props.accordionView ? "pricing-contact-form-wdt" : "pricing-contact-form" },
                        React.createElement(
                            "div",
                            { className: "pure-g" },
                            React.createElement(
                                "div",
                                { className: "pure-u-1" },
                                React.createElement(
                                    "svg",
                                    { "class": "ct-frm-svg", viewBox: "0 0 20 20", xmlns: "http://www.w3.org/2000/svg" },
                                    React.createElement("path", { d: "M1.4 6.5L10 11l8.6-4.5", fill: "none", stroke: "currentColor" }),
                                    React.createElement("path", { d: "M1 4v12h18V4H1zm17 11H2V5h16v10z" })
                                ),
                                React.createElement("br", null),
                                this.props.contactFormData.heading
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "pure-g" },
                            React.createElement(
                                "div",
                                { className: "pure-u-1" },
                                this.props.contactFormData.sub_info
                            )
                        ),
                        React.createElement("br", null),
                        React.createElement(
                            React.Fragment,
                            null,
                            this.props.accordionView ? React.createElement(
                                React.Fragment,
                                null,
                                React.createElement(ContactFormInputs, { formInputs: this.props.contactFormData.formInputs,
                                    accordionView: this.props.accordionView,
                                    contactFormToggle: function contactFormToggle() {
                                        return _this13.props.contactFormToggle();
                                    },
                                    toggleContactFormText: this.props.contactFormData.toggleContactFormText,
                                    submitContactFormText: this.props.contactFormData.submitContactFormText })
                            ) : React.createElement(
                                React.Fragment,
                                null,
                                React.createElement(ContactFormInputs, { formInputs: this.props.contactFormData.formInputs,
                                    accordionView: this.props.accordionView,
                                    contactFormToggle: function contactFormToggle() {
                                        return _this13.props.contactFormToggle();
                                    },
                                    toggleContactFormText: this.props.contactFormData.toggleContactFormText,
                                    submitContactFormText: this.props.contactFormData.submitContactFormText })
                            )
                        ),
                        React.createElement("br", null)
                    )
                )
            );
        }
    }]);

    return ContactForm;
}(React.Component);

// simple plan tier


var SimplePlanTier = function (_React$Component7) {
    _inherits(SimplePlanTier, _React$Component7);

    function SimplePlanTier(props) {
        _classCallCheck(this, SimplePlanTier);

        // console.log("props in simplePlanTier", props);

        var _this14 = _possibleConstructorReturn(this, (SimplePlanTier.__proto__ || Object.getPrototypeOf(SimplePlanTier)).call(this, props));

        _this14.state = {
            tiers: teirsData.tiers,
            // showMonthlyPlan: true,
            selectedOption: true,
            radio_btn_monthly_opt: teirsData.radio_btn_monthly_opt,
            radio_btn_yearly_opt: teirsData.radio_btn_yearly_opt,
            compareText: teirsData.compareText,
            monthlyText: teirsData.monthlyText,
            yearlyText: teirsData.yearlyText,
            showContactForm: false,
            contactFormData: contactForm
        };
        return _this14;
    }

    _createClass(SimplePlanTier, [{
        key: "render",
        value: function render() {
            var _this15 = this;

            var rows = [];

            this.state.tiers.forEach(function (tier) {

                rows.push(React.createElement(
                    "div",
                    { key: tier.name, className: "pure-u-xs-1 pure-u-sm-1-3 pure-u-md-1-3 pure-u-lg-1-3 pure-u-xl-1-3" },
                    React.createElement(
                        "div",
                        { className: "price-card" },
                        React.createElement(
                            "div",
                            { className: "pricing-panel-wrapper wrp-2" },
                            React.createElement(
                                "div",
                                { className: "pricing-panel" },
                                tier.popular && tier.popular == "True" ? React.createElement(
                                    "div",
                                    { "class": "pricing-panel-ribbon" },
                                    React.createElement(
                                        "h5",
                                        { "class": "featured-title" },
                                        tier.popularInfoText
                                    )
                                ) : React.createElement("div", { className: "wrp-arnd" }),
                                React.createElement(
                                    "div",
                                    { className: "pricing-panel-header" },
                                    React.createElement(
                                        "h6",
                                        { className: "pricing-panel-tier" },
                                        tier.name
                                    ),
                                    tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(
                                        React.Fragment,
                                        null,
                                        tier.call_to_action.type == "contact" ?
                                        // add contact page toggle if type is contact
                                        React.createElement(
                                            "button",
                                            { className: "contact-us-btn", onClick: function onClick() {
                                                    return _this15.props.contactFormToggle();
                                                } },
                                            React.createElement(
                                                "span",
                                                { className: "contact-action-label" },
                                                tier.call_to_action.text
                                            )
                                        ) : React.createElement(
                                            React.Fragment,
                                            null,
                                            tier.call_to_action.type == "link" ? React.createElement(
                                                "a",
                                                { href: tier.call_to_action.url, className: "contact-us-btn" },
                                                React.createElement(
                                                    "span",
                                                    { className: "contact-action-label" },
                                                    tier.call_to_action.text
                                                )
                                            ) : ''
                                        )
                                    ) : React.createElement(
                                        React.Fragment,
                                        null,
                                        _this15.props.showMonthlyPlan ? React.createElement(
                                            React.Fragment,
                                            null,
                                            React.createElement(
                                                "h2",
                                                { className: "product-price product-price-lg" },
                                                React.createElement(
                                                    "span",
                                                    { className: "currency" },
                                                    tier.pricing.monthly.currency
                                                ),
                                                React.createElement(
                                                    "span",
                                                    { className: "price" },
                                                    tier.pricing.monthly.price
                                                ),
                                                React.createElement(
                                                    "span",
                                                    { className: "period" },
                                                    tier.pricing.monthly.label
                                                )
                                            ),
                                            React.createElement(
                                                "div",
                                                { className: "pricing-panel-info" },
                                                React.createElement(
                                                    "div",
                                                    { className: "text-yearly-color" },
                                                    React.createElement(
                                                        "p",
                                                        { "data-alt-text": "$950 billed yearly<br />Save $238/year", className: "year-pricing" },
                                                        tier.pricing.yearly.currency,
                                                        tier.pricing.yearly.price,
                                                        tier.pricing.monthly.label,
                                                        " ",
                                                        React.createElement(
                                                            "div",
                                                            { className: "yearly", onClick: function onClick() {
                                                                    return _this15.props.yearlyToggle();
                                                                } },
                                                            " ",
                                                            _this15.state.monthlyText
                                                        )
                                                    )
                                                )
                                            )
                                        ) : React.createElement(
                                            React.Fragment,
                                            null,
                                            React.createElement(
                                                "h2",
                                                { className: "product-price product-price-lg" },
                                                React.createElement(
                                                    "span",
                                                    { className: "currency" },
                                                    tier.pricing.yearly.currency
                                                ),
                                                React.createElement(
                                                    "span",
                                                    { className: "price" },
                                                    tier.pricing.yearly.price
                                                ),
                                                React.createElement(
                                                    "span",
                                                    { className: "period" },
                                                    tier.pricing.monthly.label
                                                )
                                            ),
                                            React.createElement(
                                                "div",
                                                { className: "pricing-panel-info" },
                                                React.createElement(
                                                    "div",
                                                    { className: "text-yearly-color" },
                                                    React.createElement(
                                                        "p",
                                                        { "data-alt-text": "$950 billed yearly<br />Save $238/year", className: "year-pricing" },
                                                        tier.pricing.yearly.currency,
                                                        tier.pricing.yearly.perAnnum,
                                                        " ",
                                                        _this15.state.yearlyText,
                                                        " ",
                                                        tier.pricing.yearly.currency,
                                                        tier.pricing.yearly.savedAmount,
                                                        tier.pricing.yearly.label
                                                    )
                                                )
                                            )
                                        )
                                    ),
                                    React.createElement("p", null),
                                    tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(
                                        "p",
                                        { className: "desc-text" },
                                        tier.description
                                    ) : React.createElement(
                                        "p",
                                        null,
                                        tier.description
                                    ),
                                    React.createElement("p", null)
                                ),
                                React.createElement(
                                    "div",
                                    { className: "pricing-panel-footer" },
                                    tier.showCallToAction && tier.showCallToAction == "False" ? React.createElement(
                                        "div",
                                        { className: "cta-wrapper" },
                                        React.createElement(
                                            "a",
                                            { href: tier.call_to_action.url, className: "sign-up-btn" },
                                            React.createElement(
                                                "div",
                                                { className: "action-link-lg" },
                                                tier.call_to_action.text
                                            )
                                        )
                                    ) : React.createElement("div", { className: "ftr-wrp" }),
                                    React.createElement(
                                        "a",
                                        { href: "#detail-plan-container", className: "compare-plans pln", onClick: function onClick() {
                                                return _this15.props.onClick();
                                            } },
                                        _this15.state.compareText
                                    )
                                )
                            )
                        )
                    )
                ));
            });

            return React.createElement(
                React.Fragment,
                null,
                this.props.showContactForm ? React.createElement(
                    "div",
                    { className: "contact-form-container-smpl" },
                    React.createElement(ContactForm, { contactFormData: this.state.contactFormData, contactFormToggle: function contactFormToggle() {
                            return _this15.props.contactFormToggle();
                        },
                        showContactForm: this.props.showContactForm, submitContactForm: function submitContactForm() {
                            return _this15.props.submitContactForm();
                        } })
                ) : React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        "div",
                        { className: "simple-plans-container" },
                        React.createElement(
                            "div",
                            { className: "pure-g-r" },
                            rows
                        )
                    )
                )
            );
        }
    }]);

    return SimplePlanTier;
}(React.Component);

;

var DetailedPlanTier = function (_React$Component8) {
    _inherits(DetailedPlanTier, _React$Component8);

    function DetailedPlanTier(props) {
        _classCallCheck(this, DetailedPlanTier);

        var _this16 = _possibleConstructorReturn(this, (DetailedPlanTier.__proto__ || Object.getPrototypeOf(DetailedPlanTier)).call(this, props));

        _this16.state = {
            plansAndFeaturesInfo: plansAndFeaturesData.plansAndFeaturesInfo
        };
        return _this16;
    }

    _createClass(DetailedPlanTier, [{
        key: "render",
        value: function render() {
            var _this17 = this;

            var detailRows = [];

            var categoryFeatures = [];

            var tierActions = [];

            this.props.tiers.forEach(function (tier) {

                detailRows.push(React.createElement(
                    "div",
                    { key: tier.name, className: "pure-u-1-4 category-feature-head" },
                    React.createElement(
                        "h4",
                        { className: "pricing-name" },
                        tier.name
                    ),
                    tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(
                        React.Fragment,
                        null,
                        tier.call_to_action.type == "contact" ?
                        // add contact page toggle if type is contact
                        React.createElement(
                            "button",
                            { className: "contact-us-btn-dtl", onClick: function onClick() {
                                    return _this17.props.contactFormToggle();
                                } },
                            React.createElement(
                                "span",
                                { className: "contact-action-label" },
                                tier.call_to_action.text
                            )
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            tier.call_to_action.type == "link" ? React.createElement(
                                "a",
                                { href: tier.call_to_action.url, className: "contact-us-btn-dtl" },
                                React.createElement(
                                    "span",
                                    { className: "contact-action-label" },
                                    tier.call_to_action.text
                                )
                            ) : ''
                        )
                    ) : React.createElement(
                        React.Fragment,
                        null,
                        _this17.props.showMonthlyPlan ? React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                "h2",
                                { className: "product-price product-price-md" },
                                React.createElement(
                                    "span",
                                    { className: "currency" },
                                    tier.pricing.monthly.currency
                                ),
                                React.createElement(
                                    "span",
                                    { className: "price" },
                                    tier.pricing.monthly.price
                                ),
                                React.createElement(
                                    "span",
                                    { className: "period" },
                                    tier.pricing.monthly.label
                                )
                            )
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                "h2",
                                { className: "product-price product-price-md" },
                                React.createElement(
                                    "span",
                                    { className: "currency" },
                                    tier.pricing.yearly.currency
                                ),
                                React.createElement(
                                    "span",
                                    { className: "price" },
                                    tier.pricing.yearly.price
                                ),
                                React.createElement(
                                    "span",
                                    { className: "period" },
                                    tier.pricing.monthly.label
                                )
                            )
                        )
                    )
                ));
            });

            this.props.categories.forEach(function (category, i) {
                category.features.forEach(function (item, j) {

                    categoryFeatures.push(React.createElement(
                        React.Fragment,
                        null,
                        j == 0 ? React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                "div",
                                { className: "category-name-hdr" },
                                React.createElement(
                                    "h4",
                                    null,
                                    category.name
                                )
                            )
                        ) : '',
                        React.createElement(
                            "div",
                            { className: "pure-g", key: item.name },
                            React.createElement(
                                "div",
                                { className: "pure-u-1-4 card category-feature-name ctg-wrp" },
                                React.createElement(
                                    "div",
                                    { className: "category-name" },
                                    item.name,
                                    "\xA0",
                                    item.info ? React.createElement(
                                        Tooltip,
                                        { message: item.info, position: 'top' },
                                        React.createElement(
                                            "span",
                                            null,
                                            React.createElement(
                                                "svg",
                                                { "class": "ttp-svg", viewBox: "0 0 20 20", xmlns: "http://www.w3.org/2000/svg" },
                                                React.createElement("path", { d: "M12.13 11.59c-.16 1.25-1.78 2.53-3.03 2.57-2.93.04.79-4.7-.36-5.79.56-.21 1.88-.54 1.88.44 0 .82-.5 1.74-.74 2.51-1.22 3.84 2.25-.17 2.26-.14.02.03.02.17-.01.41-.05.36.03-.24 0 0zm-.57-5.92c0 1-2.2 1.48-2.2.36 0-1.03 2.2-1.49 2.2-.36z" }),
                                                React.createElement("circle", { cx: "10", cy: "10", r: "9", fill: "none", stroke: "currentColor", "stroke-width": "1.1" })
                                            )
                                        )
                                    ) : ''
                                )
                            ),
                            React.createElement(DetailCategoryFeatures, { tiers: _this17.props.tiers, item: item })
                        )
                    ));
                });
            });

            // if (this.props && this.props.tierActions) {
            //     this.props.tierActions.forEach((tierAction) => {

            //         tierActions.push(
            //             // <div key={tierAction.label.name} className="pure-u-1-4 card category-feature" style={{ textAlign: 'center' }}>
            //             //     <button className="sign-up-btn" style={{ width: '100%', fontSize: '12px !important' }}>
            //             //         <a href={tierAction.label.url} className="action-link-lg-dtl" style={{fontSize: '12px !important'}}>{tierAction.label.text}</a>
            //             //     </button>
            //             // </div>
            //             <a href={tierAction.label.url} className="pure-u-1-4 card-actn category-feature-actn">
            //                 <div className="tier-actn">
            //                     {tierAction.label.text}
            //                 </div>
            //             </a>
            //         )
            //     });
            // }

            this.props.tiers.forEach(function (tier) {

                tierActions.push(React.createElement(
                    React.Fragment,
                    null,
                    tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(
                        React.Fragment,
                        null,
                        tier.call_to_action.type == "contact" ?
                        // add contact page toggle if type is contact
                        React.createElement(
                            "a",
                            { href: "#contact-form", className: "pure-u-1-4 card-actn category-feature-actn cta-dtl-wrp", onClick: function onClick() {
                                    return _this17.props.contactFormToggle();
                                } },
                            React.createElement(
                                "span",
                                { className: "tier-actn" },
                                tier.call_to_action.text
                            )
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            tier.call_to_action.type == "link" ? React.createElement(
                                "a",
                                { href: tier.call_to_action.url, className: "pure-u-1-4 card-actn category-feature-actn" },
                                React.createElement(
                                    "span",
                                    { className: "tier-actn" },
                                    tier.call_to_action.text
                                )
                            ) : ''
                        )
                    ) : ''
                ));
            });

            return React.createElement(
                React.Fragment,
                null,
                this.props.showContactForm ? React.createElement(React.Fragment, null) : React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        "div",
                        { id: "detail-plan-container", className: "detail-plan-container" },
                        React.createElement(
                            "div",
                            { className: "detail-cmp-info" },
                            this.state.plansAndFeaturesInfo ? React.createElement(
                                "h1",
                                null,
                                this.state.plansAndFeaturesInfo
                            ) : React.createElement(
                                React.Fragment,
                                null,
                                React.createElement(
                                    "h1",
                                    null,
                                    "\xA0"
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            { className: "pure-g dtl-wrp" },
                            React.createElement(
                                "div",
                                { "class": "pure-u-1-4 card category-feature-name ctg-wrp dtl-hdr" },
                                "\xA0"
                            ),
                            detailRows
                        ),
                        categoryFeatures,
                        React.createElement("br", null),
                        React.createElement(
                            "div",
                            { className: "pure-g" },
                            React.createElement(
                                "div",
                                { "class": "pure-u-1-4 card category-feature-name ctg-wrp dtl-hdr" },
                                "\xA0"
                            ),
                            tierActions
                        ),
                        React.createElement("br", null)
                    )
                )
            );
        }
    }]);

    return DetailedPlanTier;
}(React.Component);

// used in accordion description for category


var CategoryFeatures = function (_React$Component9) {
    _inherits(CategoryFeatures, _React$Component9);

    function CategoryFeatures() {
        _classCallCheck(this, CategoryFeatures);

        return _possibleConstructorReturn(this, (CategoryFeatures.__proto__ || Object.getPrototypeOf(CategoryFeatures)).apply(this, arguments));
    }

    _createClass(CategoryFeatures, [{
        key: "render",
        value: function render() {
            var _this19 = this;

            var categoryFeatures = [];

            var val = void 0;

            this.props.categories.forEach(function (category, i) {

                // get the tier name
                val = _this19.props.plan_name;

                category.features.forEach(function (item, j) {

                    categoryFeatures.push(React.createElement(
                        "div",
                        { key: item.values[val], className: "plan-desc" },
                        j == 0 && item.values[val] ? React.createElement(
                            "span",
                            { className: "ctg-name-wrp" },
                            category.name
                        ) : '',
                        React.createElement(
                            "div",
                            { className: "plan-desc-feature" },
                            React.createElement(
                                "div",
                                { sm: "2", className: "category-feature-xs" },
                                React.createElement(
                                    "div",
                                    null,
                                    item.values[val] && item.values[val].toLowerCase() != "yes" ? React.createElement(
                                        "span",
                                        null,
                                        item.values[val],
                                        "\xA0",
                                        item.name,
                                        "\xA0"
                                    ) : item.values[val] && item.values[val].toLowerCase() == "yes" ? React.createElement(
                                        "span",
                                        null,
                                        item.name,
                                        "\xA0"
                                    ) :
                                    // <span>&nbsp;</span>    
                                    '',
                                    item.values[val] && item.info ? React.createElement(
                                        Tooltip,
                                        { message: item.info, position: 'top' },
                                        React.createElement(
                                            "span",
                                            null,
                                            React.createElement(
                                                "svg",
                                                { "class": "accrdn-ttp-svg", viewBox: "0 0 20 20", xmlns: "http://www.w3.org/2000/svg" },
                                                React.createElement("path", { d: "M12.13 11.59c-.16 1.25-1.78 2.53-3.03 2.57-2.93.04.79-4.7-.36-5.79.56-.21 1.88-.54 1.88.44 0 .82-.5 1.74-.74 2.51-1.22 3.84 2.25-.17 2.26-.14.02.03.02.17-.01.41-.05.36.03-.24 0 0zm-.57-5.92c0 1-2.2 1.48-2.2.36 0-1.03 2.2-1.49 2.2-.36z" }),
                                                React.createElement("circle", { cx: "10", cy: "10", r: "9", fill: "none", stroke: "currentColor", "stroke-width": "1.1" })
                                            )
                                        )
                                    ) : ''
                                )
                            )
                        )
                    ));
                });
            });

            return React.createElement(
                "div",
                null,
                categoryFeatures
            );
        }
    }]);

    return CategoryFeatures;
}(React.Component);

;

var PlansAccordion = function (_React$Component10) {
    _inherits(PlansAccordion, _React$Component10);

    function PlansAccordion(props) {
        _classCallCheck(this, PlansAccordion);

        var _this20 = _possibleConstructorReturn(this, (PlansAccordion.__proto__ || Object.getPrototypeOf(PlansAccordion)).call(this, props));

        _this20.state = {
            showMonthlyPlan: true,
            tiers: teirsData.tiers,
            accordionPlans: plansAndFeatures,
            contactFormData: contactForm
        };
        return _this20;
    }

    _createClass(PlansAccordion, [{
        key: "yearlyToggle",
        value: function yearlyToggle() {
            // console.log("in yearlyToggle func, this.state", this.state);
            this.setState({
                showMonthlyPlan: !this.state.showMonthlyPlan
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _this21 = this;

            var plansAccordion = [];

            this.props.tiers.forEach(function (tier, i) {

                // console.log("this.props.showMonthlyPlan", this.props.showMonthlyPlan);

                plansAccordion.push(React.createElement(
                    AccordionItem,
                    { key: tier.name },
                    React.createElement(
                        React.Fragment,
                        null,
                        React.createElement(
                            AccordionItemHeading,
                            null,
                            React.createElement(
                                AccordionItemButton,
                                null,
                                React.createElement(
                                    "span",
                                    { className: "plan-name" },
                                    tier.name
                                ),
                                React.createElement(
                                    "h2",
                                    { className: "product-price product-price-sm" },
                                    React.createElement(
                                        React.Fragment,
                                        null,
                                        tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(React.Fragment, null) : React.createElement(
                                            React.Fragment,
                                            null,
                                            _this21.props.showMonthlyPlan ? React.createElement(
                                                React.Fragment,
                                                null,
                                                React.createElement(
                                                    "span",
                                                    { className: "currency", "data-alt-text": "$" },
                                                    tier.pricing.monthly.currency
                                                ),
                                                React.createElement(
                                                    "span",
                                                    { className: "price", "data-alt-text": "79" },
                                                    tier.pricing.monthly.price
                                                ),
                                                React.createElement(
                                                    "span",
                                                    { className: "period" },
                                                    tier.pricing.monthly.label
                                                )
                                            ) : React.createElement(
                                                React.Fragment,
                                                null,
                                                React.createElement(
                                                    "span",
                                                    { className: "currency", "data-alt-text": "$" },
                                                    tier.pricing.yearly.currency
                                                ),
                                                React.createElement(
                                                    "span",
                                                    { className: "price", "data-alt-text": "79" },
                                                    tier.pricing.yearly.price
                                                ),
                                                React.createElement(
                                                    "span",
                                                    { className: "period" },
                                                    tier.pricing.monthly.label
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        ),
                        React.createElement(
                            AccordionItemPanel,
                            { className: "accrd-panel-wrp" },
                            tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(
                                React.Fragment,
                                null,
                                tier.call_to_action.type == "contact" ?
                                // add contact page toggle if type is contact
                                React.createElement(
                                    "button",
                                    { className: "contact-us-btn", onClick: function onClick() {
                                            return _this21.props.contactFormToggle();
                                        } },
                                    React.createElement(
                                        "span",
                                        { className: "contact-action-label" },
                                        tier.call_to_action.text
                                    )
                                ) : React.createElement(
                                    React.Fragment,
                                    null,
                                    tier.call_to_action.type == "link" ? React.createElement(
                                        "a",
                                        { href: tier.call_to_action.url, className: "contact-us-btn" },
                                        React.createElement(
                                            "span",
                                            { className: "contact-action-label" },
                                            tier.call_to_action.text
                                        )
                                    ) : ''
                                )
                            ) : React.createElement(
                                React.Fragment,
                                null,
                                _this21.props.showMonthlyPlan ? React.createElement(
                                    "p",
                                    { className: "text-light-gray" },
                                    tier.pricing.monthly.currency,
                                    tier.pricing.yearly.price,
                                    " ",
                                    _this21.props.tiers.monthlyText,
                                    " ",
                                    React.createElement(
                                        "div",
                                        { className: "yearly", onClick: function onClick() {
                                                return _this21.props.yearlyToggle();
                                            } },
                                        " ",
                                        _this21.props.tiers.payText
                                    )
                                ) : React.createElement(
                                    "p",
                                    { className: "text-light-gray" },
                                    tier.pricing.monthly.currency,
                                    tier.pricing.yearly.perAnnum,
                                    " ",
                                    _this21.props.tiers.yearlyText1,
                                    React.createElement("br", null),
                                    " ",
                                    _this21.props.tiers.yearlyText2,
                                    " ",
                                    tier.pricing.monthly.currency,
                                    tier.pricing.yearly.savedAmount,
                                    tier.pricing.yearly.label
                                ),
                                React.createElement(
                                    "p",
                                    null,
                                    tier.description
                                ),
                                React.createElement(
                                    "a",
                                    { href: tier.call_to_action.url, className: "sign-up-btn-xs" },
                                    React.createElement(
                                        "span",
                                        { className: "action-link" },
                                        tier.call_to_action.text
                                    )
                                )
                            ),
                            React.createElement(CategoryFeatures, { categories: _this21.props.accordionPlans.categories, plan_name: tier.name })
                        )
                    ),
                    React.createElement("br", null)
                ));
            });

            return React.createElement(
                React.Fragment,
                null,
                this.props.showContactForm ?
                // <div className="contact-form-container">
                React.createElement(ContactForm, { contactFormData: this.state.contactFormData, contactFormToggle: function contactFormToggle() {
                        return _this21.props.contactFormToggle();
                    },
                    submitContactForm: function submitContactForm() {
                        return _this21.props.submitContactForm();
                    }, accordionView: true })
                // {/* </div> */}
                : React.createElement(
                    Accordion,
                    { allowZeroExpanded: true },
                    plansAccordion
                )
            );
        }
    }]);

    return PlansAccordion;
}(React.Component);

;

var PricingPage = function (_React$Component11) {
    _inherits(PricingPage, _React$Component11);

    function PricingPage(props) {
        _classCallCheck(this, PricingPage);

        var _this22 = _possibleConstructorReturn(this, (PricingPage.__proto__ || Object.getPrototypeOf(PricingPage)).call(this, props));

        _this22.state = {
            // showDetailedPlanOveriew: false,
            tiers: teirsData.tiers,
            tierActions: teirsData.tierActions,
            categories: plansAndFeaturesData.categories,
            tooltipOpen: false,
            selectedOption: true,
            showRadioOptions: teirsData.show_radio_options,
            radio_btn_monthly_opt: teirsData.radio_btn_monthly_opt,
            radio_btn_yearly_opt: teirsData.radio_btn_yearly_opt,
            showMonthlyPlan: true,
            showContactForm: false,
            contactFormData: contactForm,
            accordionPlans: plansAndFeatures
        };
        return _this22;
    }

    _createClass(PricingPage, [{
        key: "handleClick",
        value: function handleClick() {

            // this.setState({ showDetailedPlanOveriew: !this.state.showDetailedPlanOveriew });
        }
    }, {
        key: "radioChange",
        value: function radioChange(e) {
            this.setState({
                // selectedOption: e.currentTarget.value,
                selectedOption: !this.state.selectedOption,
                showMonthlyPlan: !this.state.showMonthlyPlan
            });
        }
    }, {
        key: "yearlyToggle",
        value: function yearlyToggle() {
            // console.log("in yearlyToggle func, this.state", this.state);
            this.setState({
                selectedOption: !this.state.selectedOption,
                showMonthlyPlan: !this.state.showMonthlyPlan
            });
        }
    }, {
        key: "contactFormToggle",
        value: function contactFormToggle() {
            // console.log("in contactFormToggle func, this.state", this.state);
            window.scrollTo(180, 180);
            this.setState({
                showContactForm: !this.state.showContactForm
            });
        }
    }, {
        key: "submitContactForm",
        value: function submitContactForm() {}
        // console.log("submit form clicked");


        // get pricing page details from a remote page
        // componentDidMount() {
        //     fetch("https://www.docsie.io/pricing/plans.json")
        //         .then(res => res.json())
        //         .then(
        //             (result) => {

        //                 // // console.log("result response for plans.json from docsie endpoint", result);

        //                 // this.setState({
        //                 //     // tiers: tiers.default.tiers,
        //                 //     categories: plans_and_features.default.categories
        //                 //     // categories: result.categories
        //                 // });

        //                 // // console.log("result from fetch API in pricing page", result)
        //             },
        //             // Note: it's important to handle errors here
        //             // instead of a catch() block so that we don't swallow
        //             // exceptions from actual bugs in components.
        //             (error) => {
        //                 //   this.setState({
        //                 //     isLoaded: true,
        //                 //     error
        //                 //   });
        //             }
        //         )

        //     fetch("https://www.docsie.io/pricing/tiers.json")
        //         .then(res => res.json())
        //         .then(
        //             (result) => {

        //                 // // console.log("result response for tiers.json from docsie endpoint", result);

        //                 // this.setState({
        //                 //     tiers: tiers.default.tiers,
        //                 //     // categories: plans_and_features.default.categories
        //                 //     // tiers: result.tiers
        //                 // });

        //                 // // console.log("result from fetch API in pricing page", result);


        //             },
        //             // Note: it's important to handle errors here
        //             // instead of a catch() block so that we don't swallow
        //             // exceptions from actual bugs in components.
        //             (error) => {
        //                 //   this.setState({
        //                 //     isLoaded: true,
        //                 //     error
        //                 //   });
        //             }
        //         )
        // }


    }, {
        key: "render",
        value: function render() {
            var _this23 = this;

            return React.createElement(
                "div",
                { className: "simple-detail-plan-tier-sm-md-lg" },
                !this.state.showContactForm && this.state.showRadioOptions ? React.createElement(
                    "div",
                    { className: "pure-g" },
                    React.createElement(
                        "div",
                        { className: "pure-u-1-2 input-radio-plan input-radio-plan-monthly" },
                        React.createElement("input", { type: "radio",
                            value: true,
                            checked: this.state.selectedOption == true,
                            onChange: function onChange($event) {
                                return _this23.radioChange($event);
                            } }),
                        "\xA0",
                        React.createElement(
                            "span",
                            null,
                            this.state.radio_btn_monthly_opt
                        )
                    ),
                    React.createElement(
                        "div",
                        { className: "pure-u-1-2 input-radio-plan input-radio-plan-yearly" },
                        React.createElement("input", { type: "radio",
                            value: false,
                            checked: this.state.selectedOption == false,
                            onChange: function onChange($event) {
                                return _this23.radioChange($event);
                            } }),
                        "\xA0",
                        React.createElement(
                            "span",
                            { className: "radio-btn-wrp" },
                            this.state.radio_btn_yearly_opt
                        )
                    )
                ) : '',
                React.createElement("br", null),
                React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        "div",
                        { className: "accrd-view" },
                        React.createElement(PlansAccordion, { className: "accordion-plan-tier", accordionPlans: this.state.accordionPlans,
                            showMonthlyPlan: this.state.showMonthlyPlan,
                            tiers: this.state.tiers,
                            yearlyToggle: function yearlyToggle() {
                                return _this23.yearlyToggle();
                            },
                            contactFormToggle: function contactFormToggle() {
                                return _this23.contactFormToggle();
                            },
                            showContactForm: this.state.showContactForm,
                            submitContactForm: function submitContactForm() {
                                return _this23.submitContactForm();
                            }
                        })
                    ),
                    React.createElement(SimplePlanTier, { onClick: function onClick() {
                            return _this23.handleClick();
                        },
                        className: "plan-tier",
                        showMonthlyPlan: this.state.showMonthlyPlan,
                        yearlyToggle: function yearlyToggle() {
                            return _this23.yearlyToggle();
                        },
                        contactFormToggle: function contactFormToggle() {
                            return _this23.contactFormToggle();
                        },
                        showContactForm: this.state.showContactForm,
                        submitContactForm: function submitContactForm() {
                            return _this23.submitContactForm();
                        } }),
                    React.createElement(DetailedPlanTier, {
                        showMonthlyPlan: this.state.showMonthlyPlan,
                        showContactForm: this.state.showContactForm,
                        tiers: this.state.tiers,
                        categories: this.state.categories,
                        tierActions: this.state.tierActions,
                        yearlyToggle: function yearlyToggle() {
                            return _this23.yearlyToggle();
                        },
                        contactFormToggle: function contactFormToggle() {
                            return _this23.contactFormToggle();
                        },
                        submitContactForm: function submitContactForm() {
                            return _this23.submitContactForm();
                        },
                        handleClick: function handleClick() {
                            return _this23.handleClick();
                        },
                        contactFormData: this.state.contactFormData })
                )
            );
        }
    }]);

    return PricingPage;
}(React.Component);

// Render a Reactstrap Button element onto root
// <Button color="danger">Hello, world!</Button>
//     <LikeButton />


ReactDOM.render(React.createElement(
    React.Fragment,
    null,
    React.createElement(PricingPage, null)
), document.getElementById('root'));