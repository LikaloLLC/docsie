'use strict';

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

        var _this = _possibleConstructorReturn(this, (OfferOptions.__proto__ || Object.getPrototypeOf(OfferOptions)).call(this, props));

        console.log("props in OfferOptions", props);
        return _this;
    }

    _createClass(OfferOptions, [{
        key: 'render',
        value: function render() {
            var _this2 = this;

            var offerOptions = [];

            this.props.item.offer_options.forEach(function (option) {

                offerOptions.push(React.createElement(
                    React.Fragment,
                    null,
                    _this2.props.requiredFields.indexOf(option.alias) != -1 ? React.createElement(
                        React.Fragment,
                        null,
                        React.createElement('input', { type: option.type, style: { marginRight: '10px' }, name: option.value, value: option.value, onChange: function onChange() {
                                return _this2.props.handleInputChange(_this2.props.item, event);
                            }, required: true }),
                        ' ',
                        React.createElement(
                            'span',
                            null,
                            option.value,
                            '*'
                        ),
                        React.createElement('br', null)
                    ) : React.createElement(
                        React.Fragment,
                        null,
                        React.createElement('input', { type: option.type, style: { marginRight: '10px' }, name: option.value, value: option.value, onChange: function onChange() {
                                return _this2.props.handleInputChange(_this2.props.item, event);
                            } }),
                        React.createElement(
                            'span',
                            null,
                            option.value
                        ),
                        React.createElement('br', null)
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

        var _this3 = _possibleConstructorReturn(this, (SelectTag.__proto__ || Object.getPrototypeOf(SelectTag)).call(this, props));

        console.log("props in OfferOptions", props);
        return _this3;
    }

    _createClass(SelectTag, [{
        key: 'render',
        value: function render() {
            var _this4 = this;

            return React.createElement(
                React.Fragment,
                null,
                this.props.requiredFields.indexOf(this.props.item.alias) != -1 ? React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        'span',
                        { className: 'form-label' },
                        this.props.item.label,
                        '*'
                    ),
                    React.createElement('br', null),
                    React.createElement(
                        'select',
                        { className: this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", onChange: function onChange() {
                                return _this4.props.handleInputChange(_this4.props.item, event);
                            }, required: true },
                        this.props.item.options.map(function (opt) {
                            return React.createElement(
                                'option',
                                null,
                                opt
                            );
                        })
                    )
                ) : React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        'span',
                        { className: 'form-label' },
                        this.props.item.label
                    ),
                    React.createElement('br', null),
                    React.createElement(
                        'select',
                        { className: this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", onChange: function onChange() {
                                return _this4.props.handleInputChange(_this4.props.item, event);
                            } },
                        this.props.item.options.map(function (opt) {
                            return React.createElement(
                                'option',
                                null,
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

        var _this5 = _possibleConstructorReturn(this, (ContactFormInputs.__proto__ || Object.getPrototypeOf(ContactFormInputs)).call(this, props));

        _this5.state = contactForm.formState;

        // use this to show email validation err msg
        // this.state = Object.assign(this.state, {
        //     emailValidity: false
        // })

        console.log("props ibn ContactFormInputs", props);

        console.log("this.state in contact form", _this5.state);
        return _this5;
    }

    _createClass(ContactFormInputs, [{
        key: 'setButtonDisability',
        value: function setButtonDisability(item, event) {
            var _this6 = this;

            var disabledCount = 0;

            // check if all the required fields are entered and enable submit  button
            this.state.requiredFields.forEach(function (field) {

                console.log("checking if value exists to remove disable option on button", _this6.state[field]);

                // if value exists, set disabled state to false, else true 
                // offer_options is an array
                if (_this6.state[field] == "" || _this6.state[field] == undefined && _this6.state.offer_options.indexOf(field) == -1) {

                    disabledCount++;
                }
            });

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
        key: 'handleInputChange',
        value: function handleInputChange(item, event) {

            console.log("selected item", item, "value in handleInputChange", event.target.value);

            // if offer_options are selected, multiple checked fields are pushed and set into state
            if (item.type == "offer_options") {

                var updatedOffrOpts = this.state[item.alias];

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

                this.setState(_defineProperty({}, item.alias, updatedOffrOpts), function () {

                    console.log("state in handleInputChange callback", this.state);
                    this.setButtonDisability(item, event);
                });
            } else {

                this.setState(_defineProperty({}, item.alias, event.target.value), function () {

                    console.log("state in handleInputChange callback", this.state);
                    this.setButtonDisability(item, event);
                });
            }
        }
    }, {
        key: 'submitContactForm',
        value: function submitContactForm() {

            console.log("in submitForm func, state is::", this.state);

            var reqBody = Object.assign({}, this.state);

            delete reqBody.requiredFields;

            delete reqBody.endPoint;

            delete reqBody.disabled;

            console.log("contact post request body", this.state);

            fetch(this.state.endPoint, {
                method: 'POST',
                body: JSON.stringify(reqBody),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            }).then(function (response) {
                return response.json();
            }).then(function (result) {

                console.log("result after post request", result);
            }, function (error) {

                console.log("error in submitting contact form", error);
            });
        }
    }, {
        key: 'render',
        value: function render() {
            var _this7 = this;

            var contactFormInputs = [];

            this.props.formInputs.forEach(function (item, i) {

                console.log("item, i", item, i);
                if (item.type == "text" || item.type == "number" || item.type == "radio") {

                    console.log("item.type is text");

                    contactFormInputs.push(React.createElement(
                        'div',
                        { className: 'pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 contact-input' },
                        _this7.state.requiredFields.indexOf(item.alias) != -1 ? React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                'span',
                                { className: 'form-label' },
                                item.label,
                                '*'
                            ),
                            React.createElement('br', null),
                            React.createElement('input', { className: _this7.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", type: item.type, placeholder: item.placeholder,
                                name: 'contact-attr', value: _this7.state[item.alias], onChange: function onChange() {
                                    return _this7.handleInputChange(item, event);
                                }, required: true })
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                'span',
                                { className: 'form-label' },
                                item.label
                            ),
                            React.createElement('br', null),
                            React.createElement('input', { className: _this7.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", type: item.type, placeholder: item.placeholder,
                                name: 'contact-attr', value: _this7.state[item.alias], onChange: function onChange() {
                                    return _this7.handleInputChange(item, event);
                                } })
                        )
                    ));
                }

                if (item.type == "email") {

                    console.log("item.type is text");

                    contactFormInputs.push(React.createElement(
                        'div',
                        { className: 'pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 contact-input' },
                        _this7.state.requiredFields.indexOf(item.alias) != -1 ? React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                'span',
                                { className: 'form-label' },
                                item.label,
                                '*'
                            ),
                            React.createElement('br', null),
                            React.createElement('input', { className: _this7.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", type: item.type, placeholder: item.placeholder,
                                id: 'email', name: 'contact-attr', value: _this7.state[item.alias], onChange: function onChange() {
                                    return _this7.handleInputChange(item, event);
                                }, required: true })
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                'span',
                                { className: 'form-label' },
                                item.label
                            ),
                            React.createElement('br', null),
                            React.createElement('input', { className: _this7.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr", type: item.type, placeholder: item.placeholder,
                                id: 'email', name: 'contact-attr', value: _this7.state[item.alias], onChange: function onChange() {
                                    return _this7.handleInputChange(item, event);
                                } })
                        )
                    ));
                }

                // for dropdown
                if (item.type == "dropdown") {
                    contactFormInputs.push(React.createElement(
                        'div',
                        { className: 'pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 contact-input' },
                        React.createElement(SelectTag, { item: item, requiredFields: _this7.state.requiredFields, accordionView: _this7.props.accordionView, handleInputChange: function handleInputChange() {
                                return _this7.handleInputChange(item, event);
                            } })
                    ));
                }

                // for checkbox group
                if (item.type == "offer_options") {

                    console.log("item.type is offer_options");

                    contactFormInputs.push(React.createElement(
                        'div',
                        { className: 'pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 offer-options' },
                        React.createElement(
                            'span',
                            { style: { color: 'red' } },
                            item.optionsRequiredMsg
                        ),
                        React.createElement('br', null),
                        React.createElement(OfferOptions, { item: item, requiredFields: _this7.state.requiredFields, handleInputChange: function handleInputChange() {
                                return _this7.handleInputChange(item, event);
                            } })
                    ));
                }

                if (item.type == "text_area") {

                    console.log("item.type is text_area");

                    contactFormInputs.push(React.createElement(
                        'div',
                        { className: 'pure-u-xs-1 pure-u-sm-1-3 pure-u-md-1-3 pure-u-lg-1-3 pure-u-xl-1-3 contact-input' },
                        _this7.state.requiredFields.indexOf(item.alias) != -1 ? React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                'span',
                                { className: 'form-label-desc' },
                                item.label,
                                '*'
                            ),
                            React.createElement('textarea', { style: { border: '1px solid #ddd', width: '89.5%', float: 'left' }, rows: '5', cols: '50', placeholder: item.placeholder, onChange: function onChange() {
                                    return _this7.handleInputChange(item, event);
                                }, required: true })
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                'span',
                                { className: 'form-label-desc' },
                                item.label
                            ),
                            React.createElement('textarea', { style: { border: '1px solid #ddd', width: '89.5%', float: 'left' }, rows: '5', cols: '50', placeholder: item.placeholder, onChange: function onChange() {
                                    return _this7.handleInputChange(item, event);
                                } })
                        )
                    ));
                }
            });

            return React.createElement(
                React.Fragment,
                null,
                React.createElement(
                    'div',
                    { className: 'pure-g-r' },
                    contactFormInputs
                ),
                React.createElement(
                    'div',
                    { className: 'contact-input' },
                    React.createElement(
                        'button',
                        { className: 'ct-btn back-to-plans-btn-accrd', onClick: function onClick() {
                                return _this7.props.contactFormToggle();
                            } },
                        React.createElement(
                            'div',
                            { className: 'back-btn-action-link-lg-dtl' },
                            React.createElement(
                                'svg',
                                { className: 'ct-btn-svg', viewBox: '0 0 20 20', xmlns: 'http://www.w3.org/2000/svg' },
                                React.createElement('path', { d: 'M13 16l-6-6 6-6', fill: 'none', stroke: 'red', 'stroke-width': '1.03' })
                            ),
                            this.props.toggleContactFormText
                        )
                    ),
                    React.createElement(
                        'button',
                        { className: 'ct-btn contact-us-btn-xs', style: { color: '#fff', fontSize: '18px', fontWeight: '700' }, disabled: this.state.disabled, onClick: function onClick() {
                                return _this7.submitContactForm();
                            } },
                        this.props.submitContactFormText
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

        var _this8 = _possibleConstructorReturn(this, (Tooltip.__proto__ || Object.getPrototypeOf(Tooltip)).call(this, props));

        _this8.state = {
            displayTooltip: false
        };
        _this8.hideTooltip = _this8.hideTooltip.bind(_this8);
        _this8.showTooltip = _this8.showTooltip.bind(_this8);
        return _this8;
    }

    _createClass(Tooltip, [{
        key: 'hideTooltip',
        value: function hideTooltip() {
            this.setState({ displayTooltip: false });
        }
    }, {
        key: 'showTooltip',
        value: function showTooltip() {
            this.setState({ displayTooltip: true });
        }
    }, {
        key: 'render',
        value: function render() {
            var message = this.props.message;
            var position = this.props.position;
            return React.createElement(
                'span',
                { className: 'tooltip',
                    onMouseLeave: this.hideTooltip
                },
                this.state.displayTooltip && React.createElement(
                    'div',
                    { className: 'tooltip-bubble tooltip-' + position },
                    React.createElement(
                        'div',
                        { className: 'tooltip-message' },
                        message
                    )
                ),
                React.createElement(
                    'span',
                    {
                        className: 'tooltip-trigger',
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
        key: 'render',
        value: function render() {

            var val = void 0;

            var detailCategoryFeatures = [];

            for (var i = 0; i < this.props.tiers.length; i++) {

                val = this.props.tiers[i].name;

                detailCategoryFeatures.push(React.createElement(
                    'div',
                    { className: 'pure-u-1-4 category-feature' },
                    this.props.item.values[val] ? React.createElement(
                        'svg',
                        { 'class': 'c-check', xmlns: 'http://www.w3.org/2000/svg', viewBox: '-255 347 100 100' },
                        React.createElement('title', null),
                        React.createElement('path', { d: 'M-217.1 431.8c-1 1.2-2.6 2.2-4 2.3-1.4.1-3-.8-4.3-1.9l-27.5-24.5 7.8-8.7 23.2 20.6 54.6-61.7 8.6 7.9-58.4 66z' })
                    ) : ''
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

    function ContactForm() {
        _classCallCheck(this, ContactForm);

        return _possibleConstructorReturn(this, (ContactForm.__proto__ || Object.getPrototypeOf(ContactForm)).apply(this, arguments));
    }

    _createClass(ContactForm, [{
        key: 'render',
        value: function render() {
            var _this11 = this;

            return React.createElement(
                React.Fragment,
                null,
                React.createElement(
                    'form',
                    { className: 'contact-form-container' },
                    React.createElement(
                        'div',
                        { className: this.props.accordionView ? "pricing-contact-form-wdt" : "pricing-contact-form" },
                        React.createElement(
                            'div',
                            { className: 'pure-g' },
                            React.createElement(
                                'div',
                                { className: 'pure-u-1' },
                                React.createElement(
                                    'svg',
                                    { 'class': 'ct-frm-svg', viewBox: '0 0 20 20', xmlns: 'http://www.w3.org/2000/svg' },
                                    React.createElement('path', { d: 'M1.4 6.5L10 11l8.6-4.5', fill: 'none', stroke: 'currentColor' }),
                                    React.createElement('path', { d: 'M1 4v12h18V4H1zm17 11H2V5h16v10z' })
                                ),
                                React.createElement('br', null),
                                this.props.contactFormData.heading
                            )
                        ),
                        React.createElement(
                            'div',
                            { className: 'pure-g' },
                            React.createElement(
                                'div',
                                { className: 'pure-u-1' },
                                this.props.contactFormData.sub_info
                            )
                        ),
                        React.createElement('br', null),
                        React.createElement(
                            React.Fragment,
                            null,
                            this.props.accordionView ? React.createElement(
                                React.Fragment,
                                null,
                                React.createElement(ContactFormInputs, { formInputs: this.props.contactFormData.formInputs,
                                    accordionView: this.props.accordionView,
                                    contactFormToggle: function contactFormToggle() {
                                        return _this11.props.contactFormToggle();
                                    },
                                    toggleContactFormText: this.props.contactFormData.toggleContactFormText,
                                    submitContactFormText: this.props.contactFormData.submitContactFormText })
                            ) : React.createElement(
                                React.Fragment,
                                null,
                                React.createElement(ContactFormInputs, { formInputs: this.props.contactFormData.formInputs,
                                    accordionView: this.props.accordionView,
                                    contactFormToggle: function contactFormToggle() {
                                        return _this11.props.contactFormToggle();
                                    },
                                    toggleContactFormText: this.props.contactFormData.toggleContactFormText,
                                    submitContactFormText: this.props.contactFormData.submitContactFormText })
                            )
                        ),
                        React.createElement('br', null)
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

        var _this12 = _possibleConstructorReturn(this, (SimplePlanTier.__proto__ || Object.getPrototypeOf(SimplePlanTier)).call(this, props));

        console.log("props in simplePlanTier", props);

        _this12.state = {
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
        return _this12;
    }

    _createClass(SimplePlanTier, [{
        key: 'render',
        value: function render() {
            var _this13 = this;

            var rows = [];

            this.state.tiers.forEach(function (tier) {

                rows.push(React.createElement(
                    'div',
                    { key: tier.name, className: 'pure-u-1-2' },
                    React.createElement(
                        'div',
                        { className: 'price-card' },
                        React.createElement(
                            'div',
                            { className: 'pricing-panel-wrapper', style: { border: '3px solid #ffb5b3' } },
                            React.createElement(
                                'div',
                                { className: 'pricing-panel' },
                                tier.popular && tier.popular == "True" ? React.createElement(
                                    'div',
                                    { 'class': 'pricing-panel-ribbon' },
                                    React.createElement(
                                        'h5',
                                        { 'class': 'featured-title' },
                                        tier.popularInfoText
                                    )
                                ) : React.createElement('div', { style: { marginTop: '10%' } }),
                                React.createElement(
                                    'div',
                                    { className: 'pricing-panel-header' },
                                    React.createElement(
                                        'h6',
                                        { className: 'pricing-panel-tier' },
                                        tier.name
                                    ),
                                    tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(
                                        React.Fragment,
                                        null,
                                        tier.call_to_action.type == "contact" ?
                                        // add contact page toggle if type is contact
                                        React.createElement(
                                            'button',
                                            { className: 'contact-us-btn', onClick: function onClick() {
                                                    return _this13.props.contactFormToggle();
                                                } },
                                            React.createElement(
                                                'span',
                                                { className: 'contact-action-label' },
                                                tier.call_to_action.text
                                            )
                                        ) : React.createElement(
                                            React.Fragment,
                                            null,
                                            tier.call_to_action.type == "link" ? React.createElement(
                                                'a',
                                                { href: tier.call_to_action.url, className: 'contact-us-btn' },
                                                React.createElement(
                                                    'span',
                                                    { className: 'contact-action-label' },
                                                    tier.call_to_action.text
                                                )
                                            ) : ''
                                        )
                                    ) : React.createElement(
                                        React.Fragment,
                                        null,
                                        _this13.props.showMonthlyPlan ? React.createElement(
                                            React.Fragment,
                                            null,
                                            React.createElement(
                                                'h2',
                                                { className: 'product-price product-price-lg' },
                                                React.createElement(
                                                    'span',
                                                    { className: 'currency' },
                                                    tier.pricing.monthly.currency
                                                ),
                                                React.createElement(
                                                    'span',
                                                    { className: 'price' },
                                                    tier.pricing.monthly.price
                                                ),
                                                React.createElement(
                                                    'span',
                                                    { className: 'period' },
                                                    tier.pricing.monthly.label
                                                )
                                            ),
                                            React.createElement(
                                                'div',
                                                { className: 'pricing-panel-info' },
                                                React.createElement(
                                                    'div',
                                                    { className: 'text-yearly-color' },
                                                    React.createElement(
                                                        'p',
                                                        { 'data-alt-text': '$950 billed yearly<br />Save $238/year', className: 'year-pricing' },
                                                        tier.pricing.yearly.currency,
                                                        tier.pricing.yearly.price,
                                                        tier.pricing.monthly.label,
                                                        ' ',
                                                        React.createElement(
                                                            'div',
                                                            { className: 'yearly', onClick: function onClick() {
                                                                    return _this13.props.yearlyToggle();
                                                                } },
                                                            ' ',
                                                            _this13.state.monthlyText
                                                        )
                                                    )
                                                )
                                            )
                                        ) : React.createElement(
                                            React.Fragment,
                                            null,
                                            React.createElement(
                                                'h2',
                                                { className: 'product-price product-price-lg' },
                                                React.createElement(
                                                    'span',
                                                    { className: 'currency' },
                                                    tier.pricing.yearly.currency
                                                ),
                                                React.createElement(
                                                    'span',
                                                    { className: 'price' },
                                                    tier.pricing.yearly.price
                                                ),
                                                React.createElement(
                                                    'span',
                                                    { className: 'period' },
                                                    tier.pricing.monthly.label
                                                )
                                            ),
                                            React.createElement(
                                                'div',
                                                { className: 'pricing-panel-info' },
                                                React.createElement(
                                                    'div',
                                                    { className: 'text-yearly-color' },
                                                    React.createElement(
                                                        'p',
                                                        { 'data-alt-text': '$950 billed yearly<br />Save $238/year', className: 'year-pricing' },
                                                        tier.pricing.yearly.currency,
                                                        tier.pricing.yearly.perAnnum,
                                                        ' ',
                                                        _this13.state.yearlyText,
                                                        ' ',
                                                        tier.pricing.yearly.currency,
                                                        tier.pricing.yearly.savedAmount,
                                                        tier.pricing.yearly.label
                                                    )
                                                )
                                            )
                                        )
                                    ),
                                    React.createElement('p', null),
                                    tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(
                                        'p',
                                        { style: { marginTop: '29.5%' } },
                                        tier.description
                                    ) : React.createElement(
                                        'p',
                                        null,
                                        tier.description
                                    ),
                                    React.createElement('p', null)
                                ),
                                React.createElement(
                                    'div',
                                    { className: 'pricing-panel-footer' },
                                    tier.showCallToAction && tier.showCallToAction == "False" ? React.createElement(
                                        'div',
                                        { className: 'cta-wrapper' },
                                        React.createElement(
                                            'a',
                                            { href: tier.call_to_action.url, className: 'sign-up-btn' },
                                            React.createElement(
                                                'div',
                                                { className: 'action-link-lg' },
                                                tier.call_to_action.text
                                            )
                                        )
                                    ) : React.createElement('div', { style: { marginTop: '60px' } }),
                                    React.createElement(
                                        'p',
                                        { className: 'compare-plans', style: { position: 'relative', bottom: '20px' }, onClick: function onClick() {
                                                return _this13.props.onClick();
                                            } },
                                        _this13.state.compareText
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
                    'div',
                    { className: 'contact-form-container-smpl' },
                    React.createElement(ContactForm, { contactFormData: this.state.contactFormData, contactFormToggle: function contactFormToggle() {
                            return _this13.props.contactFormToggle();
                        },
                        showContactForm: this.props.showContactForm, submitContactForm: function submitContactForm() {
                            return _this13.props.submitContactForm();
                        } })
                ) : React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        'div',
                        { style: { maxWidth: '80%' } },
                        React.createElement(
                            'div',
                            { className: 'pure-g' },
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

        return _possibleConstructorReturn(this, (DetailedPlanTier.__proto__ || Object.getPrototypeOf(DetailedPlanTier)).call(this, props));
    }

    _createClass(DetailedPlanTier, [{
        key: 'render',
        value: function render() {
            var _this15 = this;

            var detailRows = [];

            var categoryFeatures = [];

            var tierActions = [];

            this.props.tiers.forEach(function (tier) {

                detailRows.push(React.createElement(
                    'div',
                    { key: tier.name, className: 'pure-u-1-4 category-feature-head' },
                    React.createElement(
                        'h4',
                        { className: 'pricing-name' },
                        tier.name
                    ),
                    tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(
                        React.Fragment,
                        null,
                        tier.call_to_action.type == "contact" ?
                        // add contact page toggle if type is contact
                        React.createElement(
                            'button',
                            { className: 'contact-us-btn-dtl', onClick: function onClick() {
                                    return _this15.props.contactFormToggle();
                                } },
                            React.createElement(
                                'span',
                                { className: 'contact-action-label' },
                                tier.call_to_action.text
                            )
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            tier.call_to_action.type == "link" ? React.createElement(
                                'a',
                                { href: tier.call_to_action.url, className: 'contact-us-btn-dtl' },
                                React.createElement(
                                    'span',
                                    { className: 'contact-action-label' },
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
                                'h2',
                                { className: 'product-price product-price-md' },
                                React.createElement(
                                    'span',
                                    { className: 'currency' },
                                    tier.pricing.monthly.currency
                                ),
                                React.createElement(
                                    'span',
                                    { className: 'price' },
                                    tier.pricing.monthly.price
                                ),
                                React.createElement(
                                    'span',
                                    { className: 'period' },
                                    tier.pricing.monthly.label
                                )
                            )
                        ) : React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                'h2',
                                { className: 'product-price product-price-md' },
                                React.createElement(
                                    'span',
                                    { className: 'currency' },
                                    tier.pricing.yearly.currency
                                ),
                                React.createElement(
                                    'span',
                                    { className: 'price' },
                                    tier.pricing.yearly.price
                                ),
                                React.createElement(
                                    'span',
                                    { className: 'period' },
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
                                'h4',
                                null,
                                category.name
                            )
                        ) : '',
                        React.createElement(
                            'div',
                            { className: 'pure-g', key: item.name },
                            React.createElement(
                                'div',
                                { className: 'pure-u-1-4 card category-feature-name', style: { textAlign: 'center' } },
                                React.createElement(
                                    'div',
                                    { className: 'category-name' },
                                    item.name,
                                    '\xA0',
                                    item.info ? React.createElement(
                                        Tooltip,
                                        { message: item.info, position: 'top' },
                                        React.createElement(
                                            'span',
                                            null,
                                            React.createElement(
                                                'svg',
                                                { 'class': 'ttp-svg', viewBox: '0 0 20 20', xmlns: 'http://www.w3.org/2000/svg' },
                                                React.createElement('path', { d: 'M12.13 11.59c-.16 1.25-1.78 2.53-3.03 2.57-2.93.04.79-4.7-.36-5.79.56-.21 1.88-.54 1.88.44 0 .82-.5 1.74-.74 2.51-1.22 3.84 2.25-.17 2.26-.14.02.03.02.17-.01.41-.05.36.03-.24 0 0zm-.57-5.92c0 1-2.2 1.48-2.2.36 0-1.03 2.2-1.49 2.2-.36z' }),
                                                React.createElement('circle', { cx: '10', cy: '10', r: '9', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.1' })
                                            )
                                        )
                                    ) : ''
                                )
                            ),
                            React.createElement(DetailCategoryFeatures, { tiers: _this15.props.tiers, item: item })
                        )
                    ));
                });
            });

            if (this.props && this.props.tierActions) {
                this.props.tierActions.forEach(function (tierAction) {

                    tierActions.push(
                    // <div key={tierAction.label.name} className="pure-u-1-4 card category-feature" style={{ textAlign: 'center' }}>
                    //     <button className="sign-up-btn" style={{ width: '100%', fontSize: '12px !important' }}>
                    //         <a href={tierAction.label.url} className="action-link-lg-dtl" style={{fontSize: '12px !important'}}>{tierAction.label.text}</a>
                    //     </button>
                    // </div>
                    React.createElement(
                        'a',
                        { href: tierAction.label.url, className: 'pure-u-1-4 card-actn category-feature-actn' },
                        React.createElement(
                            'div',
                            { className: 'tier-actn' },
                            tierAction.label.text
                        )
                    ));
                });
            }

            return React.createElement(
                React.Fragment,
                null,
                this.props.showContactForm ? React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        'div',
                        { className: 'contact-form-container-smpl contact-form-container-dtl' },
                        React.createElement(ContactForm, { contactFormData: this.props.contactFormData,
                            contactFormToggle: function contactFormToggle() {
                                return _this15.props.contactFormToggle();
                            },
                            submitContactForm: function submitContactForm() {
                                return _this15.props.submitContactForm();
                            } })
                    )
                ) : React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        'div',
                        { className: 'detail-plan-container' },
                        React.createElement(
                            'div',
                            { className: 'pure-g', style: { marginBottom: '-60px' } },
                            React.createElement(
                                'div',
                                { 'class': 'pure-u-1-4' },
                                '\xA0'
                            ),
                            detailRows
                        ),
                        categoryFeatures,
                        React.createElement('br', null),
                        React.createElement(
                            'div',
                            { className: 'pure-g' },
                            React.createElement(
                                'div',
                                { 'class': 'pure-u-1-4 card-actn category-feature-actn', style: { textAlign: 'center' } },
                                React.createElement(
                                    'button',
                                    { className: 'tier-actn-bck', onClick: function onClick() {
                                            return _this15.props.handleClick();
                                        } },
                                    React.createElement(
                                        'span',
                                        { className: 'tier-actn-link' },
                                        React.createElement(
                                            'svg',
                                            { 'class': 'bck-svg', viewBox: '0 0 20 20', xmlns: 'http://www.w3.org/2000/svg' },
                                            React.createElement('path', { d: 'M13 16l-6-6 6-6', fill: 'none', stroke: 'red', 'stroke-width': '1.03' })
                                        ),
                                        this.props.toggleText
                                    )
                                )
                            ),
                            tierActions
                        ),
                        React.createElement('br', null)
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
        key: 'render',
        value: function render() {
            var _this17 = this;

            var categoryFeatures = [];

            var val = void 0;

            this.props.categories.forEach(function (category, i) {

                // get the tier name
                val = _this17.props.plan_name;

                category.features.forEach(function (item, j) {

                    categoryFeatures.push(React.createElement(
                        'div',
                        { key: item.values[val], className: 'plan-desc' },
                        j == 0 ? React.createElement(
                            'span',
                            { style: { color: '#b50000bf', marginTop: '10px', fontWeight: 'bold' } },
                            category.name
                        ) : '',
                        React.createElement(
                            'div',
                            { className: 'plan-desc-feature' },
                            React.createElement(
                                'div',
                                { sm: '2', className: 'category-feature-xs' },
                                React.createElement(
                                    'div',
                                    null,
                                    item.values[val],
                                    '\xA0',
                                    item.name,
                                    '\xA0',
                                    item.info ? React.createElement(
                                        Tooltip,
                                        { message: item.info, position: 'top' },
                                        React.createElement(
                                            'span',
                                            null,
                                            React.createElement(
                                                'svg',
                                                { 'class': 'accrdn-ttp-svg', viewBox: '0 0 20 20', xmlns: 'http://www.w3.org/2000/svg' },
                                                React.createElement('path', { d: 'M12.13 11.59c-.16 1.25-1.78 2.53-3.03 2.57-2.93.04.79-4.7-.36-5.79.56-.21 1.88-.54 1.88.44 0 .82-.5 1.74-.74 2.51-1.22 3.84 2.25-.17 2.26-.14.02.03.02.17-.01.41-.05.36.03-.24 0 0zm-.57-5.92c0 1-2.2 1.48-2.2.36 0-1.03 2.2-1.49 2.2-.36z' }),
                                                React.createElement('circle', { cx: '10', cy: '10', r: '9', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.1' })
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
                'div',
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

        var _this18 = _possibleConstructorReturn(this, (PlansAccordion.__proto__ || Object.getPrototypeOf(PlansAccordion)).call(this, props));

        _this18.state = {
            showMonthlyPlan: true,
            tiers: teirsData.tiers,
            accordionPlans: plansAndFeatures,
            contactFormData: contactForm
        };
        return _this18;
    }

    _createClass(PlansAccordion, [{
        key: 'yearlyToggle',
        value: function yearlyToggle() {
            console.log("in yearlyToggle func, this.state", this.state);
            this.setState({
                showMonthlyPlan: !this.state.showMonthlyPlan
            });
        }
    }, {
        key: 'render',
        value: function render() {
            var _this19 = this;

            var plansAccordion = [];

            this.props.tiers.forEach(function (tier, i) {

                console.log("this.props.showMonthlyPlan", _this19.props.showMonthlyPlan);

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
                                    'span',
                                    { className: 'plan-name' },
                                    tier.name
                                ),
                                React.createElement(
                                    'h2',
                                    { className: 'product-price product-price-sm' },
                                    React.createElement(
                                        React.Fragment,
                                        null,
                                        tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(React.Fragment, null) : React.createElement(
                                            React.Fragment,
                                            null,
                                            _this19.props.showMonthlyPlan ? React.createElement(
                                                React.Fragment,
                                                null,
                                                React.createElement(
                                                    'span',
                                                    { className: 'currency', 'data-alt-text': '$' },
                                                    tier.pricing.monthly.currency
                                                ),
                                                React.createElement(
                                                    'span',
                                                    { className: 'price', 'data-alt-text': '79' },
                                                    tier.pricing.monthly.price
                                                ),
                                                React.createElement(
                                                    'span',
                                                    { className: 'period' },
                                                    tier.pricing.monthly.label
                                                )
                                            ) : React.createElement(
                                                React.Fragment,
                                                null,
                                                React.createElement(
                                                    'span',
                                                    { className: 'currency', 'data-alt-text': '$' },
                                                    tier.pricing.yearly.currency
                                                ),
                                                React.createElement(
                                                    'span',
                                                    { className: 'price', 'data-alt-text': '79' },
                                                    tier.pricing.yearly.price
                                                ),
                                                React.createElement(
                                                    'span',
                                                    { className: 'period' },
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
                            { style: { background: '#fff', textAlign: 'center' } },
                            tier.showCallToAction && tier.showCallToAction == "True" ? React.createElement(
                                React.Fragment,
                                null,
                                tier.call_to_action.type == "contact" ?
                                // add contact page toggle if type is contact
                                React.createElement(
                                    'button',
                                    { className: 'contact-us-btn', onClick: function onClick() {
                                            return _this19.props.contactFormToggle();
                                        } },
                                    React.createElement(
                                        'span',
                                        { className: 'contact-action-label' },
                                        tier.call_to_action.text
                                    )
                                ) : React.createElement(
                                    React.Fragment,
                                    null,
                                    tier.call_to_action.type == "link" ? React.createElement(
                                        'a',
                                        { href: tier.call_to_action.url, className: 'contact-us-btn' },
                                        React.createElement(
                                            'span',
                                            { className: 'contact-action-label' },
                                            tier.call_to_action.text
                                        )
                                    ) : ''
                                )
                            ) : React.createElement(
                                React.Fragment,
                                null,
                                _this19.props.showMonthlyPlan ? React.createElement(
                                    'p',
                                    { className: 'text-light-gray' },
                                    tier.pricing.monthly.currency,
                                    tier.pricing.yearly.price,
                                    ' ',
                                    _this19.props.tiers.monthlyText,
                                    ' ',
                                    React.createElement(
                                        'div',
                                        { className: 'yearly', onClick: function onClick() {
                                                return _this19.props.yearlyToggle();
                                            } },
                                        ' ',
                                        _this19.props.tiers.payText
                                    )
                                ) : React.createElement(
                                    'p',
                                    { className: 'text-light-gray' },
                                    tier.pricing.monthly.currency,
                                    tier.pricing.yearly.perAnnum,
                                    ' ',
                                    _this19.props.tiers.yearlyText1,
                                    React.createElement('br', null),
                                    ' ',
                                    _this19.props.tiers.yearlyText2,
                                    ' ',
                                    tier.pricing.monthly.currency,
                                    tier.pricing.yearly.savedAmount,
                                    tier.pricing.yearly.label
                                ),
                                React.createElement(
                                    'p',
                                    null,
                                    tier.description
                                ),
                                React.createElement(
                                    'a',
                                    { href: tier.call_to_action.url, className: 'sign-up-btn-xs' },
                                    React.createElement(
                                        'span',
                                        { className: 'action-link' },
                                        tier.call_to_action.text
                                    )
                                )
                            ),
                            React.createElement(CategoryFeatures, { categories: _this19.props.accordionPlans.categories, plan_name: tier.name })
                        )
                    ),
                    React.createElement('br', null)
                ));
            });

            return React.createElement(
                React.Fragment,
                null,
                this.props.showContactForm ?
                // <div className="contact-form-container">
                React.createElement(ContactForm, { contactFormData: this.state.contactFormData, contactFormToggle: function contactFormToggle() {
                        return _this19.props.contactFormToggle();
                    },
                    submitContactForm: function submitContactForm() {
                        return _this19.props.submitContactForm();
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

        var _this20 = _possibleConstructorReturn(this, (PricingPage.__proto__ || Object.getPrototypeOf(PricingPage)).call(this, props));

        _this20.state = {
            showDetailedPlanOveriew: false,
            tiers: teirsData.tiers,
            tierActions: teirsData.tierActions,
            categories: plansAndFeaturesData.categories,
            tooltipOpen: false,
            selectedOption: true,
            radio_btn_monthly_opt: teirsData.radio_btn_monthly_opt,
            radio_btn_yearly_opt: teirsData.radio_btn_yearly_opt,
            toggleText: teirsData.toggleText,
            showMonthlyPlan: true,
            showContactForm: false,
            contactFormData: contactForm,
            accordionPlans: plansAndFeatures
        };
        return _this20;
    }

    _createClass(PricingPage, [{
        key: 'handleClick',
        value: function handleClick() {

            this.setState({ showDetailedPlanOveriew: !this.state.showDetailedPlanOveriew });
        }
    }, {
        key: 'radioChange',
        value: function radioChange(e) {
            this.setState({
                // selectedOption: e.currentTarget.value,
                selectedOption: !this.state.selectedOption,
                showMonthlyPlan: !this.state.showMonthlyPlan
            });
        }
    }, {
        key: 'yearlyToggle',
        value: function yearlyToggle() {
            console.log("in yearlyToggle func, this.state", this.state);
            this.setState({
                selectedOption: !this.state.selectedOption,
                showMonthlyPlan: !this.state.showMonthlyPlan
            });
        }
    }, {
        key: 'contactFormToggle',
        value: function contactFormToggle() {
            console.log("in contactFormToggle func, this.state", this.state);
            this.setState({
                showContactForm: !this.state.showContactForm
            });
        }
    }, {
        key: 'submitContactForm',
        value: function submitContactForm() {
            console.log("submit form clicked");
        }

        // get pricing page details from a remote page
        // componentDidMount() {
        //     fetch("https://www.docsie.io/pricing/plans.json")
        //         .then(res => res.json())
        //         .then(
        //             (result) => {

        //                 // console.log("result response for plans.json from docsie endpoint", result);

        //                 // this.setState({
        //                 //     // tiers: tiers.default.tiers,
        //                 //     categories: plans_and_features.default.categories
        //                 //     // categories: result.categories
        //                 // });

        //                 // console.log("result from fetch API in pricing page", result)
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

        //                 // console.log("result response for tiers.json from docsie endpoint", result);

        //                 // this.setState({
        //                 //     tiers: tiers.default.tiers,
        //                 //     // categories: plans_and_features.default.categories
        //                 //     // tiers: result.tiers
        //                 // });

        //                 // console.log("result from fetch API in pricing page", result);


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
        key: 'render',
        value: function render() {
            var _this21 = this;

            return React.createElement(
                'div',
                { className: 'simple-detail-plan-tier-sm-md-lg' },
                !this.state.showContactForm ? React.createElement(
                    'div',
                    { className: 'pure-g' },
                    React.createElement(
                        'div',
                        { className: 'pure-u-1-2 input-radio-plan input-radio-plan-monthly' },
                        React.createElement('input', { type: 'radio',
                            value: true,
                            checked: this.state.selectedOption == true,
                            onChange: function onChange($event) {
                                return _this21.radioChange($event);
                            } }),
                        '\xA0',
                        React.createElement(
                            'span',
                            null,
                            this.state.radio_btn_monthly_opt
                        )
                    ),
                    React.createElement(
                        'div',
                        { className: 'pure-u-1-2 input-radio-plan input-radio-plan-yearly' },
                        React.createElement('input', { type: 'radio',
                            value: false,
                            checked: this.state.selectedOption == false,
                            onChange: function onChange($event) {
                                return _this21.radioChange($event);
                            } }),
                        '\xA0',
                        React.createElement(
                            'span',
                            { style: { marginLeft: '5px' } },
                            this.state.radio_btn_yearly_opt
                        )
                    )
                ) : '',
                React.createElement('br', null),
                !this.state.showDetailedPlanOveriew ? React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        'div',
                        { className: 'accrd-view' },
                        React.createElement(PlansAccordion, { className: 'accordion-plan-tier', accordionPlans: this.state.accordionPlans,
                            showMonthlyPlan: this.state.showMonthlyPlan,
                            tiers: this.state.tiers,
                            yearlyToggle: function yearlyToggle() {
                                return _this21.yearlyToggle();
                            },
                            contactFormToggle: function contactFormToggle() {
                                return _this21.contactFormToggle();
                            },
                            showContactForm: this.state.showContactForm,
                            submitContactForm: function submitContactForm() {
                                return _this21.submitContactForm();
                            }
                        })
                    ),
                    React.createElement(
                        'div',
                        { className: 'simple-plan-container' },
                        React.createElement(SimplePlanTier, { onClick: function onClick() {
                                return _this21.handleClick();
                            },
                            className: 'plan-tier',
                            showMonthlyPlan: this.state.showMonthlyPlan,
                            yearlyToggle: function yearlyToggle() {
                                return _this21.yearlyToggle();
                            },
                            contactFormToggle: function contactFormToggle() {
                                return _this21.contactFormToggle();
                            },
                            showContactForm: this.state.showContactForm,
                            submitContactForm: function submitContactForm() {
                                return _this21.submitContactForm();
                            } })
                    )
                ) : React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        'div',
                        { className: 'accrd-view' },
                        React.createElement(PlansAccordion, { className: 'accordion-plan-tier', accordionPlans: this.state.accordionPlans,
                            showMonthlyPlan: this.state.showMonthlyPlan,
                            tiers: this.state.tiers,
                            yearlyToggle: function yearlyToggle() {
                                return _this21.yearlyToggle();
                            },
                            contactFormToggle: function contactFormToggle() {
                                return _this21.contactFormToggle();
                            },
                            showContactForm: this.state.showContactForm,
                            submitContactForm: function submitContactForm() {
                                return _this21.submitContactForm();
                            }
                        })
                    ),
                    React.createElement(
                        'div',
                        { className: 'simple-plan-container' },
                        React.createElement(DetailedPlanTier, {
                            showMonthlyPlan: this.state.showMonthlyPlan,
                            showContactForm: this.state.showContactForm,
                            toggleText: this.state.toggleText,
                            tiers: this.state.tiers,
                            categories: this.state.categories,
                            tierActions: this.state.tierActions,
                            yearlyToggle: function yearlyToggle() {
                                return _this21.yearlyToggle();
                            },
                            contactFormToggle: function contactFormToggle() {
                                return _this21.contactFormToggle();
                            },
                            submitContactForm: function submitContactForm() {
                                return _this21.submitContactForm();
                            },
                            handleClick: function handleClick() {
                                return _this21.handleClick();
                            },
                            contactFormData: this.state.contactFormData })
                    )
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