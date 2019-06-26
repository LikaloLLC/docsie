'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

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

var Tooltip = function (_React$Component) {
    _inherits(Tooltip, _React$Component);

    function Tooltip(props) {
        _classCallCheck(this, Tooltip);

        var _this = _possibleConstructorReturn(this, (Tooltip.__proto__ || Object.getPrototypeOf(Tooltip)).call(this, props));

        _this.state = {
            displayTooltip: false
        };
        _this.hideTooltip = _this.hideTooltip.bind(_this);
        _this.showTooltip = _this.showTooltip.bind(_this);
        return _this;
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

var ContactForm = function (_React$Component2) {
    _inherits(ContactForm, _React$Component2);

    function ContactForm() {
        _classCallCheck(this, ContactForm);

        return _possibleConstructorReturn(this, (ContactForm.__proto__ || Object.getPrototypeOf(ContactForm)).apply(this, arguments));
    }

    _createClass(ContactForm, [{
        key: 'render',
        value: function render() {
            var _this3 = this;

            var offerOptions = [];

            this.props.contactFormData.offer_options.forEach(function (item) {

                offerOptions.push(React.createElement(
                    React.Fragment,
                    null,
                    React.createElement('input', { type: 'checkbox', style: { marginRight: '10px' }, name: item, value: item }),
                    React.createElement(
                        'span',
                        { style: { fontSize: '14px' } },
                        item
                    ),
                    React.createElement('br', null)
                ));
            });

            return React.createElement(
                React.Fragment,
                null,
                React.createElement(
                    'div',
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
                                    { width: '60px', height: '60px', viewBox: '0 0 20 20', xmlns: 'http://www.w3.org/2000/svg' },
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
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.firstNameLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { className: this.props.accordionView ? "feature-req-email feature-req-email-wdt" : "feature-req-email", type: 'email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    )
                                ),
                                React.createElement('br', null),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.lastNameLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { className: this.props.accordionView ? "feature-req-email feature-req-email-wdt" : "feature-req-email", type: 'email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    )
                                ),
                                React.createElement('br', null),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.companyNameLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { className: this.props.accordionView ? "feature-req-email feature-req-email-wdt" : "feature-req-email", type: 'email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    )
                                ),
                                React.createElement('br', null),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.businessEmailLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { className: this.props.accordionView ? "feature-req-email feature-req-email-wdt" : "feature-req-email", type: 'email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    )
                                ),
                                React.createElement('br', null),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.jobTitleLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { className: this.props.accordionView ? "feature-req-email feature-req-email-wdt" : "feature-req-email", type: 'email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    )
                                ),
                                React.createElement('br', null),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.industryLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { className: this.props.accordionView ? "feature-req-email feature-req-email-wdt" : "feature-req-email", type: 'email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    )
                                ),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.noOfEmployeesLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { className: this.props.accordionView ? "feature-req-email feature-req-email-wdt" : "feature-req-email", type: 'feature-req-email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    )
                                ),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1 offer-options' },
                                        offerOptions
                                    )
                                ),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1 text-area-option' },
                                        React.createElement('textarea', { className: this.props.accordionView ? "feature-req-ta feature-req-ta-wdt" : "feature-req-ta", rows: '6', cols: '50', placeholder: this.props.contactFormData.place_holder })
                                    )
                                )
                            ) : React.createElement(
                                React.Fragment,
                                null,
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1-2 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.firstNameLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { style: { width: '416px', border: '1px solid black' }, type: 'feature-req-email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    ),
                                    React.createElement('br', null),
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1-2 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.lastNameLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { style: { width: '416px', border: '1px solid black' }, type: 'feature-req-email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    ),
                                    React.createElement('br', null)
                                ),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1-2 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.companyNameLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { style: { width: '416px', border: '1px solid black' }, type: 'feature-req-email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    ),
                                    React.createElement('br', null),
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1-2 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.businessEmailLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { style: { width: '416px', border: '1px solid black' }, type: 'feature-req-email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    ),
                                    React.createElement('br', null)
                                ),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1-2 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.jobTitleLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { style: { width: '416px', border: '1px solid black' }, type: 'feature-req-email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    ),
                                    React.createElement('br', null),
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1-2 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.industryLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { style: { width: '416px', border: '1px solid black' }, type: 'feature-req-email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    ),
                                    React.createElement('br', null)
                                ),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label' },
                                            this.props.contactFormData.noOfEmployeesLabel
                                        ),
                                        React.createElement('br', null),
                                        React.createElement('input', { style: { float: 'left', width: '416px', border: '1px solid black' }, type: 'feature-req-email', placeholder: 'enter your email.',
                                            id: 'feature-req-email', name: 'feature-req-email', required: '' })
                                    )
                                ),
                                React.createElement('br', null),
                                React.createElement(
                                    'div',
                                    { className: 'pure-g' },
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1-2 offer-options' },
                                        offerOptions
                                    ),
                                    React.createElement(
                                        'div',
                                        { className: 'pure-u-1-2 text-area-option' },
                                        React.createElement(
                                            'span',
                                            { className: 'form-label-desc' },
                                            this.props.contactFormData.featureDescriptionLabel
                                        ),
                                        React.createElement('textarea', { style: { border: '1px solid black' }, rows: '6', cols: '50', placeholder: this.props.contactFormData.place_holder })
                                    ),
                                    React.createElement('br', null)
                                )
                            )
                        ),
                        React.createElement('br', null),
                        React.createElement(
                            'button',
                            { className: 'contact-us-btn', style: { float: 'right' } },
                            React.createElement(
                                'div',
                                { className: 'contact-action-label' },
                                this.props.contactFormData.submitContactFormText
                            )
                        ),
                        React.createElement(
                            'button',
                            { className: 'contact-us-btn', style: { float: 'left' }, onClick: function onClick() {
                                    return _this3.props.contactFormToggle();
                                } },
                            React.createElement(
                                'div',
                                { className: 'contact-action-label' },
                                this.props.contactFormData.toggleContactFormText
                            )
                        )
                    )
                )
            );
        }
    }]);

    return ContactForm;
}(React.Component);

var SimplePlanTier = function (_React$Component3) {
    _inherits(SimplePlanTier, _React$Component3);

    function SimplePlanTier(props) {
        _classCallCheck(this, SimplePlanTier);

        var _this4 = _possibleConstructorReturn(this, (SimplePlanTier.__proto__ || Object.getPrototypeOf(SimplePlanTier)).call(this, props));

        console.log("props in simplePlanTier", props);

        _this4.state = {
            tiers: teirsData.tiers,
            // showMonthlyPlan: true,
            selectedOption: true,
            radio_btn_monthly_opt: teirsData.radio_btn_monthly_opt,
            radio_btn_yearly_opt: teirsData.radio_btn_yearly_opt,
            showContactForm: false,
            contactFormData: contactForm
        };
        return _this4;
    }

    _createClass(SimplePlanTier, [{
        key: 'render',
        value: function render() {
            var _this5 = this;

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
                                    { className: tier.popular == "True" ? "pricing-panel-header popular-header" : "pricing-panel-header" },
                                    React.createElement(
                                        'h6',
                                        { className: 'pricing-panel-tier' },
                                        tier.name
                                    ),
                                    tier.showContact && tier.showContact == "True" ? React.createElement(
                                        React.Fragment,
                                        null,
                                        React.createElement(
                                            'button',
                                            { className: 'contact-us-btn', onClick: function onClick() {
                                                    return _this5.props.contactFormToggle();
                                                } },
                                            React.createElement(
                                                'div',
                                                { className: 'contact-action-label' },
                                                tier.contactFormText
                                            )
                                        )
                                    ) : React.createElement(
                                        React.Fragment,
                                        null,
                                        _this5.props.showMonthlyPlan ? React.createElement(
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
                                                        _this5.state.tiers[0].monthlyText,
                                                        ' ',
                                                        React.createElement(
                                                            'div',
                                                            { className: 'yearly', onClick: function onClick() {
                                                                    return _this5.props.yearlyToggle();
                                                                } },
                                                            ' ',
                                                            _this5.state.tiers[0].payText
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
                                                        _this5.state.tiers[0].yearlyText1,
                                                        React.createElement('br', null),
                                                        ' ',
                                                        _this5.state.tiers[0].yearlyText2,
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
                                    tier.showContact && tier.showContact == "True" ? React.createElement(
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
                                    tier.showContact && tier.showContact == "False" ? React.createElement(
                                        'div',
                                        { className: 'cta-wrapper' },
                                        React.createElement(
                                            'button',
                                            { className: 'sign-up-btn' },
                                            React.createElement(
                                                'a',
                                                { href: tier.call_to_action.url, className: 'action-link-lg' },
                                                tier.call_to_action.text
                                            )
                                        )
                                    ) : '',
                                    React.createElement(
                                        'p',
                                        { className: 'compare-plans', style: { position: 'relative', bottom: '20px' }, onClick: function onClick() {
                                                return _this5.props.onClick();
                                            } },
                                        _this5.state.tiers[0].compareText
                                    )
                                )
                            )
                        )
                    )
                ));
            });

            // let offerOptions= [];

            // this.state.contactFormData.offer_options.forEach((item) => {

            //     offerOptions.push(
            //         <React.Fragment>
            //             <input type="checkbox" name={item} value={item} />{item}<br />
            //         </React.Fragment>
            //     )
            // })


            return React.createElement(
                React.Fragment,
                null,
                this.props.showContactForm ? React.createElement(
                    'div',
                    { className: 'contact-form-container' },
                    React.createElement(ContactForm, { contactFormData: this.state.contactFormData, contactFormToggle: function contactFormToggle() {
                            return _this5.props.contactFormToggle();
                        },
                        showContactForm: this.props.showContactForm })
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

var CategoryFeatures = function (_React$Component4) {
    _inherits(CategoryFeatures, _React$Component4);

    function CategoryFeatures() {
        _classCallCheck(this, CategoryFeatures);

        return _possibleConstructorReturn(this, (CategoryFeatures.__proto__ || Object.getPrototypeOf(CategoryFeatures)).apply(this, arguments));
    }

    _createClass(CategoryFeatures, [{
        key: 'render',
        value: function render() {
            var _this7 = this;

            var categoryFeatures = [];

            var val = void 0;

            this.props.categories.forEach(function (category, i) {

                // get the tier name
                val = _this7.props.plan_name;

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
                                    React.createElement(
                                        Tooltip,
                                        { message: item.info, position: 'top' },
                                        React.createElement(
                                            'span',
                                            null,
                                            React.createElement(
                                                'svg',
                                                { width: '20px', height: '20px', viewBox: '0 0 20 20', xmlns: 'http://www.w3.org/2000/svg' },
                                                React.createElement('path', { d: 'M12.13 11.59c-.16 1.25-1.78 2.53-3.03 2.57-2.93.04.79-4.7-.36-5.79.56-.21 1.88-.54 1.88.44 0 .82-.5 1.74-.74 2.51-1.22 3.84 2.25-.17 2.26-.14.02.03.02.17-.01.41-.05.36.03-.24 0 0zm-.57-5.92c0 1-2.2 1.48-2.2.36 0-1.03 2.2-1.49 2.2-.36z' }),
                                                React.createElement('circle', { cx: '10', cy: '10', r: '9', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.1' })
                                            )
                                        )
                                    )
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

var PlansAccordion = function (_React$Component5) {
    _inherits(PlansAccordion, _React$Component5);

    function PlansAccordion(props) {
        _classCallCheck(this, PlansAccordion);

        var _this8 = _possibleConstructorReturn(this, (PlansAccordion.__proto__ || Object.getPrototypeOf(PlansAccordion)).call(this, props));

        _this8.state = {
            showMonthlyPlan: true,
            tiers: teirsData.tiers,
            accordionPlans: plansAndFeatures,
            contactFormData: contactForm
        };
        return _this8;
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
            var _this9 = this;

            var plansAccordion = [];

            this.props.tiers.forEach(function (tier, i) {

                console.log("this.props.showMonthlyPlan", _this9.props.showMonthlyPlan);

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
                                        tier.showContact && tier.showContact == "True" ? React.createElement(React.Fragment, null) : React.createElement(
                                            React.Fragment,
                                            null,
                                            _this9.props.showMonthlyPlan ? React.createElement(
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
                            tier.showContact && tier.showContact == "True" ? React.createElement(
                                React.Fragment,
                                null,
                                React.createElement(
                                    'button',
                                    { className: 'contact-us-btn-xs', onClick: function onClick() {
                                            return _this9.props.contactFormToggle();
                                        } },
                                    React.createElement(
                                        'div',
                                        { className: 'contact-action-label' },
                                        tier.contactFormText
                                    )
                                )
                            ) : React.createElement(
                                React.Fragment,
                                null,
                                _this9.props.showMonthlyPlan ? React.createElement(
                                    'p',
                                    { className: 'text-light-gray' },
                                    tier.pricing.monthly.currency,
                                    tier.pricing.yearly.price,
                                    ' ',
                                    _this9.props.tiers[0].monthlyText,
                                    ' ',
                                    React.createElement(
                                        'div',
                                        { className: 'yearly', onClick: function onClick() {
                                                return _this9.props.yearlyToggle();
                                            } },
                                        ' ',
                                        _this9.props.tiers[0].payText
                                    )
                                ) : React.createElement(
                                    'p',
                                    { className: 'text-light-gray' },
                                    tier.pricing.monthly.currency,
                                    tier.pricing.yearly.perAnnum,
                                    ' ',
                                    _this9.props.tiers[0].yearlyText1,
                                    React.createElement('br', null),
                                    ' ',
                                    _this9.props.tiers[0].yearlyText2,
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
                                    'button',
                                    { className: 'sign-up-btn-xs' },
                                    React.createElement(
                                        'a',
                                        { href: tier.call_to_action.url, className: 'action-link' },
                                        tier.call_to_action.text
                                    )
                                )
                            ),
                            React.createElement(CategoryFeatures, { categories: _this9.props.accordionPlans.categories, plan_name: tier.name })
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
                        return _this9.props.contactFormToggle();
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

var PricingPage = function (_React$Component6) {
    _inherits(PricingPage, _React$Component6);

    function PricingPage(props) {
        _classCallCheck(this, PricingPage);

        var _this10 = _possibleConstructorReturn(this, (PricingPage.__proto__ || Object.getPrototypeOf(PricingPage)).call(this, props));

        _this10.state = {
            showDetailedPlanOveriew: false,
            tiers: teirsData.tiers,
            categories: plansAndFeaturesData.categories,
            tooltipOpen: false,
            selectedOption: true,
            radio_btn_monthly_opt: teirsData.radio_btn_monthly_opt,
            radio_btn_yearly_opt: teirsData.radio_btn_yearly_opt,
            showMonthlyPlan: true,
            showContactForm: false,
            contactFormData: contactForm,
            accordionPlans: plansAndFeatures
        };
        return _this10;
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

        // get pricing page details from a remote page

    }, {
        key: 'componentDidMount',
        value: function componentDidMount() {

            this.setState({
                tierActions: plansAndFeaturesData.tierActions
            });
        }
    }, {
        key: 'render',
        value: function render() {
            var _this11 = this;

            var detailRows = [];

            var categoryFeatures = [];

            var tierActions = [];

            this.state.tiers.forEach(function (tier) {

                detailRows.push(React.createElement(
                    'div',
                    { key: tier.name, className: 'pure-u-1-4 category-feature-head' },
                    React.createElement(
                        'h4',
                        { className: 'pricing-name' },
                        tier.name
                    ),
                    tier.showContact && tier.showContact == "True" ? React.createElement(
                        React.Fragment,
                        null,
                        React.createElement(
                            'button',
                            { className: 'contact-us-btn-dtl', onClick: function onClick() {
                                    return _this11.contactFormToggle();
                                } },
                            React.createElement(
                                'div',
                                { className: 'contact-action-label' },
                                tier.contactFormText
                            )
                        )
                    ) : React.createElement(
                        React.Fragment,
                        null,
                        _this11.state.showMonthlyPlan ? React.createElement(
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

            var val1 = this.state.tiers[0].name;

            var val2 = this.state.tiers[1].name;

            this.state.categories.forEach(function (category, i) {
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
                                    React.createElement(
                                        Tooltip,
                                        { message: item.info, position: 'top' },
                                        React.createElement(
                                            'span',
                                            null,
                                            React.createElement(
                                                'svg',
                                                { width: '20px', height: '20px', viewBox: '0 0 20 20', xmlns: 'http://www.w3.org/2000/svg' },
                                                React.createElement('path', { d: 'M12.13 11.59c-.16 1.25-1.78 2.53-3.03 2.57-2.93.04.79-4.7-.36-5.79.56-.21 1.88-.54 1.88.44 0 .82-.5 1.74-.74 2.51-1.22 3.84 2.25-.17 2.26-.14.02.03.02.17-.01.41-.05.36.03-.24 0 0zm-.57-5.92c0 1-2.2 1.48-2.2.36 0-1.03 2.2-1.49 2.2-.36z' }),
                                                React.createElement('circle', { cx: '10', cy: '10', r: '9', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.1' })
                                            )
                                        )
                                    )
                                )
                            ),
                            React.createElement(
                                'div',
                                { className: 'pure-u-1-4 card category-feature' },
                                React.createElement(
                                    'div',
                                    null,
                                    item.values[val1]
                                )
                            ),
                            React.createElement(
                                'div',
                                { className: 'pure-u-1-4 card category-feature' },
                                React.createElement(
                                    'div',
                                    null,
                                    item.values[val2]
                                )
                            )
                        )
                    ));
                });
            });

            if (this.state && this.state.tierActions) {
                this.state.tierActions.forEach(function (tierAction) {

                    tierActions.push(React.createElement(
                        'div',
                        { key: tierAction.label.name, className: 'pure-u-1-4', style: { textAlign: 'center' } },
                        React.createElement(
                            'button',
                            { className: 'sign-up-btn', style: { width: '100%', fontSize: '12px !important' } },
                            React.createElement(
                                'a',
                                { href: tierAction.label.url, className: 'action-link-lg-dtl', style: { fontSize: '12px !important' } },
                                tierAction.label.text
                            )
                        )
                    ));
                });
            }

            var offerOptions = [];

            this.state.contactFormData.offer_options.forEach(function (item) {

                offerOptions.push(React.createElement(
                    React.Fragment,
                    null,
                    React.createElement('input', { type: 'checkbox', name: item, value: item }),
                    item,
                    React.createElement('br', null)
                ));
            });

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
                                return _this11.radioChange($event);
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
                                return _this11.radioChange($event);
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
                                return _this11.yearlyToggle();
                            },
                            contactFormToggle: function contactFormToggle() {
                                return _this11.contactFormToggle();
                            },
                            showContactForm: this.state.showContactForm
                        })
                    ),
                    React.createElement(
                        'div',
                        { className: 'simple-plan-container' },
                        React.createElement(SimplePlanTier, { onClick: function onClick() {
                                return _this11.handleClick();
                            },
                            className: 'plan-tier', showMonthlyPlan: this.state.showMonthlyPlan, yearlyToggle: function yearlyToggle() {
                                return _this11.yearlyToggle();
                            }, contactFormToggle: function contactFormToggle() {
                                return _this11.contactFormToggle();
                            }, showContactForm: this.state.showContactForm })
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
                                return _this11.yearlyToggle();
                            },
                            contactFormToggle: function contactFormToggle() {
                                return _this11.contactFormToggle();
                            },
                            showContactForm: this.state.showContactForm
                        })
                    ),
                    React.createElement(
                        React.Fragment,
                        null,
                        this.state.showContactForm ? React.createElement(
                            React.Fragment,
                            null,
                            React.createElement(
                                'div',
                                { className: 'contact-form-container' },
                                React.createElement(ContactForm, { contactFormData: this.state.contactFormData, contactFormToggle: function contactFormToggle() {
                                        return _this11.contactFormToggle();
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
                                        { 'class': 'pure-u-1-4', style: { textAlign: 'center' } },
                                        React.createElement(
                                            'button',
                                            { className: 'back-to-plans-btn', onClick: function onClick() {
                                                    return _this11.handleClick();
                                                } },
                                            React.createElement(
                                                'svg',
                                                { width: '30px', height: '30px', viewBox: '0 0 20 20', xmlns: 'http://www.w3.org/2000/svg' },
                                                React.createElement('path', { d: 'M13 16l-6-6 6-6', fill: 'none', stroke: 'red', 'stroke-width': '1.03' })
                                            ),
                                            React.createElement(
                                                'a',
                                                { href: '#', className: 'back-btn-action-link-lg-dtl' },
                                                this.state.tiers[0].toggleText
                                            )
                                        )
                                    ),
                                    tierActions
                                ),
                                React.createElement('br', null)
                            )
                        )
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