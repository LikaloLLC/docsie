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

var SimplePlanTier = function (_React$Component2) {
    _inherits(SimplePlanTier, _React$Component2);

    function SimplePlanTier(props) {
        _classCallCheck(this, SimplePlanTier);

        var _this2 = _possibleConstructorReturn(this, (SimplePlanTier.__proto__ || Object.getPrototypeOf(SimplePlanTier)).call(this, props));

        _this2.state = {
            tiers: teirsData.tiers,
            showMonthlyPlan: true
        };
        return _this2;
    }

    _createClass(SimplePlanTier, [{
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
            var _this3 = this;

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
                            { className: 'pricing-panel-wrapper' },
                            React.createElement(
                                'div',
                                { className: 'pricing-panel' },
                                React.createElement(
                                    'div',
                                    { className: 'pricing-panel-header' },
                                    React.createElement(
                                        'h6',
                                        { className: 'pricing-panel-tier' },
                                        tier.name
                                    ),
                                    _this3.state.showMonthlyPlan ? React.createElement(
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
                                                    _this3.state.tiers[0].monthlyText,
                                                    ' ',
                                                    React.createElement(
                                                        'div',
                                                        { className: 'yearly', onClick: function onClick() {
                                                                return _this3.yearlyToggle();
                                                            } },
                                                        ' ',
                                                        _this3.state.tiers[0].payText
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
                                                    _this3.state.tiers[0].yearlyText1,
                                                    React.createElement('br', null),
                                                    ' ',
                                                    _this3.state.tiers[0].yearlyText2,
                                                    ' ',
                                                    tier.pricing.yearly.currency,
                                                    tier.pricing.yearly.savedAmount,
                                                    tier.pricing.yearly.label
                                                )
                                            )
                                        )
                                    ),
                                    React.createElement('p', null),
                                    React.createElement(
                                        'p',
                                        null,
                                        tier.description
                                    ),
                                    React.createElement('p', null)
                                ),
                                React.createElement(
                                    'div',
                                    { className: 'pricing-panel-footer' },
                                    React.createElement(
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
                                    ),
                                    React.createElement(
                                        'p',
                                        { className: 'compare-plans', onClick: function onClick() {
                                                return _this3.props.onClick();
                                            } },
                                        _this3.state.tiers[0].compareText
                                    )
                                )
                            )
                        )
                    )
                ));
            });

            return React.createElement(
                'div',
                { className: 'pure-g' },
                rows
            );
        }
    }]);

    return SimplePlanTier;
}(React.Component);

;

var CategoryFeatures = function (_React$Component3) {
    _inherits(CategoryFeatures, _React$Component3);

    function CategoryFeatures() {
        _classCallCheck(this, CategoryFeatures);

        return _possibleConstructorReturn(this, (CategoryFeatures.__proto__ || Object.getPrototypeOf(CategoryFeatures)).apply(this, arguments));
    }

    _createClass(CategoryFeatures, [{
        key: 'render',
        value: function render() {
            var _this5 = this;

            var categoryFeatures = [];

            var val = void 0;

            this.props.categories.forEach(function (category, i) {

                // get the tier name
                val = _this5.props.plan_name;

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

var PlansAccordion = function (_React$Component4) {
    _inherits(PlansAccordion, _React$Component4);

    function PlansAccordion(props) {
        _classCallCheck(this, PlansAccordion);

        var _this6 = _possibleConstructorReturn(this, (PlansAccordion.__proto__ || Object.getPrototypeOf(PlansAccordion)).call(this, props));

        _this6.state = {
            showMonthlyPlan: true,
            tiers: teirsData.tiers,
            accordionPlans: plansAndFeatures
        };
        return _this6;
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
            var _this7 = this;

            var plansAccordion = [];

            this.state.tiers.forEach(function (tier, i) {

                plansAccordion.push(React.createElement(
                    AccordionItem,
                    { key: tier.name },
                    _this7.state.showMonthlyPlan ? React.createElement(
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
                                )
                            )
                        ),
                        React.createElement(
                            AccordionItemPanel,
                            { style: { background: '#f5505017', textAlign: 'center' } },
                            React.createElement(
                                'p',
                                { className: 'text-light-gray' },
                                tier.pricing.monthly.currency,
                                tier.pricing.yearly.price,
                                ' ',
                                _this7.state.tiers[0].monthlyText,
                                ' ',
                                React.createElement(
                                    'div',
                                    { className: 'yearly', onClick: function onClick() {
                                            return _this7.yearlyToggle();
                                        } },
                                    ' ',
                                    _this7.state.tiers[0].payText
                                )
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
                            ),
                            React.createElement(CategoryFeatures, { categories: _this7.state.accordionPlans.categories, plan_name: tier.name })
                        )
                    ) : React.createElement(
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
                        ),
                        React.createElement(
                            AccordionItemPanel,
                            { style: { background: '#f5505017', textAlign: 'center' } },
                            React.createElement(
                                'p',
                                { className: 'text-light-gray' },
                                tier.pricing.monthly.currency,
                                tier.pricing.yearly.perAnnum,
                                ' ',
                                _this7.state.tiers[0].yearlyText1,
                                React.createElement('br', null),
                                ' ',
                                _this7.state.tiers[0].yearlyText2,
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
                            ),
                            React.createElement(CategoryFeatures, { categories: _this7.state.accordionPlans.categories, plan_name: tier.name })
                        )
                    ),
                    React.createElement('br', null)
                ));
            });

            return React.createElement(
                'div',
                null,
                React.createElement(
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

var PricingPage = function (_React$Component5) {
    _inherits(PricingPage, _React$Component5);

    function PricingPage(props) {
        _classCallCheck(this, PricingPage);

        var _this8 = _possibleConstructorReturn(this, (PricingPage.__proto__ || Object.getPrototypeOf(PricingPage)).call(this, props));

        _this8.state = {
            showDetailedPlanOveriew: false,
            tiers: teirsData.tiers,
            categories: plansAndFeaturesData.categories,
            tooltipOpen: false
        };
        return _this8;
    }

    _createClass(PricingPage, [{
        key: 'handleClick',
        value: function handleClick() {

            this.setState({ showDetailedPlanOveriew: !this.state.showDetailedPlanOveriew });
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
            var _this9 = this;

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

            return React.createElement(
                'div',
                { className: 'simple-detail-plan-tier-sm-md-lg' },
                !this.state.showDetailedPlanOveriew ? React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        'div',
                        { className: 'accrd-view' },
                        React.createElement(PlansAccordion, { className: 'accordion-plan-tier' })
                    ),
                    React.createElement(
                        'div',
                        { className: 'simple-plan-container' },
                        React.createElement(
                            'div',
                            { className: 'container', style: { maxWidth: '80%' } },
                            React.createElement(SimplePlanTier, { onClick: function onClick() {
                                    return _this9.handleClick();
                                },
                                className: 'plan-tier' })
                        )
                    )
                ) : React.createElement(
                    React.Fragment,
                    null,
                    React.createElement(
                        'div',
                        { className: 'accrd-view' },
                        React.createElement(PlansAccordion, { className: 'accordion-plan-tier' })
                    ),
                    React.createElement(
                        'div',
                        { className: 'detail-plan-container' },
                        React.createElement(
                            'div',
                            { style: { background: '#fff', width: '80%' } },
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
                                    '\xA0'
                                ),
                                tierActions
                            ),
                            React.createElement('br', null),
                            React.createElement(
                                'button',
                                { className: 'sign-up-btn view-simple-tier-btn', onClick: function onClick() {
                                        return _this9.handleClick();
                                    } },
                                React.createElement(
                                    'div',
                                    { className: 'action-link-lg view-simple-tier' },
                                    this.state.tiers[0].toggleText
                                )
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