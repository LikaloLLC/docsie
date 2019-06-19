"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

// import * as tiers from '../../../../forked-docsie-pricing-table/docsie-pricing-table/src/tiers.json';
// import * as plans_and_features from '../../../../forked-docsie-pricing-table/docsie-pricing-table/src/tiers.json';

// const tiers = require('./tiers.json');

// "Import" the components from Reactstrap
var _Reactstrap = Reactstrap,
    Container = _Reactstrap.Container,
    Button = _Reactstrap.Button,
    Row = _Reactstrap.Row,
    Col = _Reactstrap.Col;
var _reactAccessibleAccor = reactAccessibleAccordion,
    Accordion = _reactAccessibleAccor.Accordion,
    AccordionItem = _reactAccessibleAccor.AccordionItem,
    AccordionItemHeading = _reactAccessibleAccor.AccordionItemHeading,
    AccordionItemPanel = _reactAccessibleAccor.AccordionItemPanel,
    AccordionItemButton = _reactAccessibleAccor.AccordionItemButton;
var MediaQuery = MediaQuery.MediaQuery;


var ReactTooltip = ReactTooltip;

var SimplePlanTier = function (_React$Component) {
    _inherits(SimplePlanTier, _React$Component);

    function SimplePlanTier() {
        _classCallCheck(this, SimplePlanTier);

        return _possibleConstructorReturn(this, (SimplePlanTier.__proto__ || Object.getPrototypeOf(SimplePlanTier)).apply(this, arguments));
    }

    _createClass(SimplePlanTier, [{
        key: "render",
        value: function render() {
            var _this2 = this;

            // console.log("props in SimplePlanTier", this.props);

            var rows = [];

            //   console.log("props in simple plan tier", this.props);

            this.props.tiers.forEach(function (tier) {

                // console.log("found tier is", tier);

                rows.push(
                // <div key={tier.name} className="col-xs-12 col-sm-6 col-md-6 col-lg-6">
                React.createElement(
                    "div",
                    { key: tier.name, className: "pure-u-1-2" },
                    React.createElement(
                        "div",
                        { className: "price-card" },
                        React.createElement(
                            "div",
                            { className: "pricing-panel-wrapper" },
                            React.createElement(
                                "div",
                                { className: "pricing-panel" },
                                React.createElement(
                                    "div",
                                    { className: "pricing-panel-header" },
                                    React.createElement(
                                        "h6",
                                        { className: "pricing-panel-tier" },
                                        tier.name
                                    ),
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
                                            "/mo"
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
                                                "/mo when you ",
                                                React.createElement(
                                                    "a",
                                                    { href: "#", className: "yearly" },
                                                    " pay yearly"
                                                )
                                            )
                                        )
                                    ),
                                    React.createElement("p", null),
                                    React.createElement(
                                        "p",
                                        null,
                                        tier.description
                                    ),
                                    React.createElement("p", null),
                                    React.createElement(
                                        "div",
                                        { className: "pricing-panel-footer" },
                                        React.createElement(
                                            "div",
                                            { className: "cta-wrapper" },
                                            React.createElement(
                                                Button,
                                                { className: "sign-up-btn" },
                                                React.createElement(
                                                    "a",
                                                    { href: tier.call_to_action.url, className: "action-link-lg" },
                                                    tier.call_to_action.text
                                                )
                                            )
                                        ),
                                        React.createElement(
                                            "p",
                                            { className: "compare-plans", onClick: function onClick() {
                                                    return _this2.props.onClick();
                                                } },
                                            "compare plans"
                                        )
                                    )
                                )
                            )
                        )
                    )
                ));
            });

            return (
                // <div className="row">
                //     {rows}
                // </div>

                React.createElement(
                    "div",
                    { className: "pure-g" },
                    rows
                )

                // <div className="pure-g center-grid">
                // <div className="pure-u-1-2"><p>Thirds</p></div>
                // <div className="pure-u-1-2"><p>Thirds</p></div>
                // <div className="pure-u-1-2"><p>Thirds</p></div>
                // </div>

            );
        }
    }]);

    return SimplePlanTier;
}(React.Component);

;

// <FaInfoCircle data-tip={item.info}/></div>

//                                 <ReactTooltip />

var CategoryFeatures = function (_React$Component2) {
    _inherits(CategoryFeatures, _React$Component2);

    function CategoryFeatures() {
        _classCallCheck(this, CategoryFeatures);

        return _possibleConstructorReturn(this, (CategoryFeatures.__proto__ || Object.getPrototypeOf(CategoryFeatures)).apply(this, arguments));
    }

    _createClass(CategoryFeatures, [{
        key: "render",
        value: function render() {

            var categoryFeatures = [];

            var val = void 0;

            this.props.categories.forEach(function (category, i) {

                val = category.plan_name;

                category.features.forEach(function (item, j) {

                    categoryFeatures.push(React.createElement(
                        "div",
                        { key: item.values[val], className: "plan-desc" },
                        j == 0 ? React.createElement(
                            "span",
                            { style: { color: '#b50000bf', marginTop: '10px', fontWeight: 'bold' } },
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
                                    item.values[val],
                                    "\xA0",
                                    item.name,
                                    "\xA0",
                                    React.createElement(
                                        "span",
                                        { className: "tooltip-info" },
                                        React.createElement("i", { className: "fa fa-info-circle", "aria-hidden": "true", "data-tip": item.info }),
                                        React.createElement(
                                            "span",
                                            { className: "tooltiptext-info" },
                                            item.info
                                        )
                                    )
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

var PlansAccordion = function (_React$Component3) {
    _inherits(PlansAccordion, _React$Component3);

    function PlansAccordion() {
        _classCallCheck(this, PlansAccordion);

        return _possibleConstructorReturn(this, (PlansAccordion.__proto__ || Object.getPrototypeOf(PlansAccordion)).apply(this, arguments));
    }

    _createClass(PlansAccordion, [{
        key: "render",
        value: function render() {

            var plansAccordion = [];

            this.props.plans.forEach(function (plan) {

                plansAccordion.push(React.createElement(
                    AccordionItem,
                    { key: plan.name },
                    React.createElement(
                        AccordionItemHeading,
                        null,
                        React.createElement(
                            AccordionItemButton,
                            null,
                            React.createElement(
                                "span",
                                { className: "plan-name" },
                                plan.name
                            ),
                            React.createElement(
                                "h2",
                                { className: "product-price product-price-sm" },
                                React.createElement(
                                    "span",
                                    { className: "currency", "data-alt-text": "$" },
                                    "$"
                                ),
                                React.createElement(
                                    "span",
                                    { className: "price", "data-alt-text": "79" },
                                    "99"
                                ),
                                React.createElement(
                                    "span",
                                    { className: "period" },
                                    "/mo"
                                )
                            )
                        )
                    ),
                    React.createElement(
                        AccordionItemPanel,
                        { style: { background: '#f5505017', textAlign: 'center' } },
                        React.createElement(
                            "p",
                            { className: "text-light-gray" },
                            plan.yearly_price,
                            " when you pay yearly"
                        ),
                        React.createElement(
                            "p",
                            null,
                            plan.description
                        ),
                        React.createElement(
                            Button,
                            { className: "sign-up-btn-xs" },
                            React.createElement(
                                "a",
                                { href: plan.call_to_action.url, className: "action-link" },
                                plan.call_to_action.text
                            )
                        ),
                        React.createElement(CategoryFeatures, { categories: plan.categories })
                    ),
                    React.createElement("br", null)
                ));
            });

            return React.createElement(
                "div",
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

var PricingPage = function (_React$Component4) {
    _inherits(PricingPage, _React$Component4);

    function PricingPage(props) {
        _classCallCheck(this, PricingPage);

        var _this5 = _possibleConstructorReturn(this, (PricingPage.__proto__ || Object.getPrototypeOf(PricingPage)).call(this, props));

        _this5.state = {
            showDetailedPlanOveriew: false,
            tiers: [],
            categories: [],
            plans: [],
            tooltipOpen: false
        };
        return _this5;
    }

    _createClass(PricingPage, [{
        key: "handleClick",
        value: function handleClick() {

            // console.log("about to hide simple plan tier and show detailed plan view");
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
        key: "componentDidMount",
        value: function componentDidMount() {

            var mydata = data;
            // console.log("./tiers.json mydata", mydata);    

            var mydata2 = data2;
            // console.log("./plans_and/-features.json mydata2", mydata2);

            // get this json for mobile responsive data
            var mydata3 = plans;
            // console.log("plans in mydata3", mydata3);

            this.setState({
                tiers: mydata.tiers,
                categories: mydata2.categories,
                plans: mydata3.plans
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _this6 = this;

            var detailRows = [];

            var categoryFeatures = [];

            this.state.tiers.forEach(function (tier) {

                detailRows.push(
                //   <Col sm="2" key={tier.name} style={{ textAlign: 'center' }}>
                React.createElement(
                    "div",
                    { key: tier.name, className: "col-xs-12 col-sm-4 col-md-4 col-lg-4" },
                    React.createElement(
                        "h4",
                        { className: "pricing-name" },
                        tier.name
                    ),
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
                            "/mo"
                        )
                    )
                ));
            });

            // <FaInfoCircle data-tip={item.info}/>
            //                             <ReactTooltip />

            // <div className="tooltip-info">Hover over me
            //                                 <span className="tooltiptext-info">Tooltip text</span>
            //                             </div>

            this.state.categories.forEach(function (category, i) {
                category.features.forEach(function (item, j) {

                    categoryFeatures.push(
                    //   <Container key={item.name}>

                    //       { i!= 0 && j == 0 ?
                    //       <h4 className="category-type-1">{category.name}</h4>
                    //        : ''}

                    //       <Row style={{ textAlign: 'center', textAlign: 'center', margin: 'auto' }}>
                    //           <Col sm="2" className="category-feature">

                    //               <div style={{display: 'inline-block'}}>{item.name}&nbsp;
                    //                   <span className="tooltip-info"><i className="fa fa-info-circle" aria-hidden="true" data-tip={item.info}></i>
                    //                       <span className="tooltiptext-info">{item.info}</span>
                    //                   </span>
                    //               </div>

                    //           </Col>
                    //           <Col sm="2" className="category-feature">
                    //               <div>{item.values.Standard}</div>
                    //           </Col>
                    //           <Col sm="2" className="category-feature">
                    //               <div>{item.values.Medium}</div>
                    //           </Col>
                    //           <Col sm="2" className="category-feature">
                    //               <div>{item.values.Large}</div>
                    //           </Col>
                    //           <Col sm="2" className="category-feature">
                    //               <div>{item.values.Premium}</div>
                    //           </Col>
                    //       </Row>
                    //   </Container>
                    React.createElement(
                        "div",
                        { key: item.name },
                        i != 0 && j == 0 ? React.createElement(
                            "div",
                            { className: "row" },
                            React.createElement(
                                "div",
                                { className: "col-xs-12 col-sm-4 col-md-4 col-lg-4" },
                                React.createElement(
                                    "h4",
                                    { style: { textAlign: 'center' } },
                                    category.name
                                )
                            )
                        ) : '',
                        React.createElement(
                            "div",
                            { className: "row" },
                            React.createElement(
                                "div",
                                { className: "col-xs-12 col-sm-4 col-md-4 col-lg-4 category-feature", style: { textAlign: 'center', margin: 'auto' } },
                                React.createElement(
                                    "div",
                                    { style: { display: 'inline-block' } },
                                    item.name,
                                    "\xA0",
                                    React.createElement(
                                        "span",
                                        { className: "tooltip-info-dsk" },
                                        React.createElement("i", { className: "fa fa-info-circle", "aria-hidden": "true", "data-tip": item.info }),
                                        React.createElement(
                                            "span",
                                            { className: "tooltiptext-info-dsk" },
                                            item.info
                                        )
                                    )
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "col-xs-12 col-sm-4 col-md-4 col-lg-4 category-feature" },
                                React.createElement(
                                    "div",
                                    null,
                                    item.values.Standard
                                )
                            ),
                            React.createElement(
                                "div",
                                { className: "col-xs-12 col-sm-4 col-md-4 col-lg-4 category-feature" },
                                React.createElement(
                                    "div",
                                    null,
                                    item.values.Medium
                                )
                            )
                        )
                    ));
                });
            });

            return React.createElement(
                "div",
                { className: "simple-detail-plan-tier-sm-md-lg" },
                !this.state.showDetailedPlanOveriew ? React.createElement(
                    "div",
                    null,
                    React.createElement(
                        "div",
                        { className: "accrd-view" },
                        React.createElement(PlansAccordion, { plans: this.state.plans, className: "accordion-plan-tier" })
                    ),
                    React.createElement(
                        "div",
                        { className: "simple-plan-container" },
                        React.createElement(
                            "div",
                            { className: "container", style: { maxWidth: '50%' } },
                            React.createElement(SimplePlanTier, { tiers: this.state.tiers, onClick: function onClick() {
                                    return _this6.handleClick();
                                },
                                className: "plan-tier" })
                        )
                    )
                ) : React.createElement(
                    "div",
                    null,
                    React.createElement(
                        "div",
                        { className: "accrd-view" },
                        React.createElement(PlansAccordion, { plans: this.state.plans, className: "accordion-plan-tier" })
                    ),
                    React.createElement(
                        "div",
                        { className: "detail-plan-container" },
                        React.createElement(
                            "div",
                            { className: "container", style: { background: '#f5505017' } },
                            React.createElement(
                                "div",
                                { className: "row" },
                                React.createElement(
                                    "div",
                                    { className: "col-xs-12 col-sm-4 col-md-4 col-lg-4" },
                                    React.createElement(
                                        "h4",
                                        { className: "category-type-main" },
                                        this.state.categories[0].name
                                    )
                                ),
                                detailRows
                            ),
                            categoryFeatures,
                            React.createElement("br", null),
                            React.createElement(
                                Button,
                                { className: "sign-up-btn view-simple-tier-btn", onClick: function onClick() {
                                        return _this6.handleClick();
                                    } },
                                React.createElement(
                                    "div",
                                    { className: "action-link-lg view-simple-tier" },
                                    "View Simple Plan Tier"
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
    "div",
    null,
    React.createElement(PricingPage, null)
), document.getElementById('root'));