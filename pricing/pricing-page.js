const {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton } = reactAccessibleAccordion;

    class Tooltip extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
        displayTooltip: false
        }
        this.hideTooltip = this.hideTooltip.bind(this)
        this.showTooltip = this.showTooltip.bind(this)
    }

    hideTooltip () {
        this.setState({displayTooltip: false})
        
    }
    showTooltip () {
        this.setState({displayTooltip: true})
    }

    render() {
        let message = this.props.message
        let position = this.props.position
        return (
        <span className='tooltip'
            onMouseLeave={this.hideTooltip}
            >
            {this.state.displayTooltip &&
            <div className={`tooltip-bubble tooltip-${position}`}>
            <div className='tooltip-message'>{message}</div>
            </div>
            }
            <span 
            className='tooltip-trigger'
            onMouseOver={this.showTooltip}
            >
            {this.props.children}
            </span>
        </span>
        )
    }
    }

class SimplePlanTier extends React.Component {


    render() {

        const rows = [];

        this.props.tiers.forEach((tier) => {

            rows.push(
                <div key={tier.name} className="pure-u-1-2">
                    <div className="price-card">
                        <div className="pricing-panel-wrapper">
                            <div className="pricing-panel">
                                <div className="pricing-panel-header">
                                    <h6 className="pricing-panel-tier">{tier.name}</h6>
                                    <h2 className="product-price product-price-lg">
                                        <span className="currency">{tier.pricing.monthly.currency}</span>
                                        <span className="price">{tier.pricing.monthly.price}</span>
                                        <span className="period">/mo</span>
                                    </h2>
                                    <div className="pricing-panel-info">
                                        <div className="text-yearly-color">
                                            <p data-alt-text="$950 billed yearly<br />Save $238/year" className="year-pricing">
                                                {tier.pricing.yearly.currency}{tier.pricing.yearly.price}/mo when you <a href="#" className="yearly"> pay yearly</a>
                                            </p>
                                        </div>
                                    </div>
                                    <p></p>
                                    <p>{tier.description}</p>
                                    <p></p>
                                </div>
                                <div className="pricing-panel-footer">
                                    <div className="cta-wrapper">
                                        <button className="sign-up-btn">
                                            <a href={tier.call_to_action.url} className="action-link-lg">{tier.call_to_action.text}</a>
                                        </button>
                                    </div>
                                    <p className="compare-plans" onClick={() => this.props.onClick()}>compare plans</p>
                                    {/* <p>Here is a <Tooltip message={'Hello, I am a super cool tooltip'} position={'top'}>tooltip</Tooltip> on top.</p> */}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );

        });

        return (

            <div className="pure-g">
                {rows}
            </div>
        );
    }
};

class CategoryFeatures extends React.Component {
    render() {

        let categoryFeatures = [];

        let val;

        this.props.categories.forEach((category, i) => {

            val = category.plan_name;

            category.features.forEach((item, j) => {

                categoryFeatures.push(
                    <div key={item.values[val]} className="plan-desc">

                        {j == 0 ?
                            <span style={{ color: '#b50000bf', marginTop: '10px', fontWeight: 'bold' }}>{category.name}</span>
                            : ''}
                        <div className="plan-desc-feature">
                            <div sm="2" className="category-feature-xs">
                                <div>{item.values[val]}&nbsp;{item.name}&nbsp;
                                    <Tooltip message={item.info} position={'top'}>
                                        <span className="custom-info-icon-xs" aria-hidden="true" data-tip={item.info}>
                                            <p style={{position: 'relative', bottom: '15px'}}>i</p>
                                        </span>
                                    </Tooltip>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            })
        })

        return (
            <div>
                {categoryFeatures}
            </div>
        );
    }
};

class PlansAccordion extends React.Component {
    render() {

        let plansAccordion = [];

        this.props.plans.forEach((plan) => {

            plansAccordion.push(
                <AccordionItem key={plan.name}>
                    <AccordionItemHeading>
                        <AccordionItemButton>
                            <span className="plan-name">{plan.name}</span>
                            {/* <span>{plan.monthly_price}</span> */}
                            <h2 className="product-price product-price-sm">
                                <span className="currency" data-alt-text="$">$</span>
                                <span className="price" data-alt-text="79">99</span>
                                <span className="period">/mo</span>
                            </h2>
                        </AccordionItemButton>
                    </AccordionItemHeading>
                    <AccordionItemPanel style={{ background: '#f5505017', textAlign: 'center' }}>
                        <p className="text-light-gray">{plan.yearly_price} when you pay yearly</p>
                        <p>{plan.description}</p>
                        <button className="sign-up-btn-xs">
                            <a href={plan.call_to_action.url} className="action-link">{plan.call_to_action.text}</a>
                        </button>
                        <CategoryFeatures categories={plan.categories} />
                    </AccordionItemPanel>
                    <br />
                </AccordionItem>
            );
        })

        return (
            <div>
                <Accordion allowZeroExpanded={true}>
                    {plansAccordion}
                </Accordion>
            </div>
        );
    }
};

class PricingPage extends React.Component {

    constructor (props) {
        super(props);

        this.state = {
            showDetailedPlanOveriew: false,
            tiers: [],
            categories: [],
            plans: [],
            tooltipOpen: false
        };
    }

    handleClick() {

        this.setState({ showDetailedPlanOveriew: !this.state.showDetailedPlanOveriew });
    }

    mouseOver() {
        console.log("Mouse over!!!");
        // this.setState({flipped: true});
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
    componentDidMount() {

        var teirsData = tiers;
        // console.log("./tiers.json mydata", mydata);    

        var plansAndFeaturesData = plansAndFeatures;
        // console.log("./plans_and/-features.json mydata2", mydata2);

        // get this json for mobile responsive data
        var plansData = plans;
        // console.log("plans in mydata3", mydata3);

        this.setState({
            tiers: teirsData.tiers,
            categories: plansAndFeaturesData.categories,
            plans: plansData.plans,
            tierActions: plansAndFeaturesData.tierActions
        });
    }

    render() {

        let detailRows = [];

        let categoryFeatures = [];

        let tierActions = []; 

        this.state.tiers.forEach((tier) => {

            detailRows.push(
                <div key={tier.name} className="pure-u-1-4 category-feature-head">
                    <h4 className="pricing-name">{tier.name}</h4>
                    <h2 className="product-price product-price-md">
                        <span className="currency">{tier.pricing.monthly.currency}</span>
                        <span className="price">{tier.pricing.monthly.price}</span>
                        <span className="period">/mo</span>
                    </h2>
                </div>
            )
        });

        this.state.categories.forEach((category, i) => {
            category.features.forEach((item, j) => {

                categoryFeatures.push(

                    <React.Fragment>

                        {/* {i != 0 && j == 0 ? */}
                        {j == 0 ?
                            <React.Fragment>

                                    <h4>{category.name}</h4>
                                    
                            </React.Fragment>
                            : ''}
                            <div className="pure-g" key={item.name}>
                                <div className="pure-u-1-4 card category-feature-name" style={{ textAlign: 'center' }}>

                                    <div  className="category-name">{item.name}&nbsp; 
                                    <Tooltip message={item.info} position={'top'}>
                                        <span className="custom-info-icon" aria-hidden="true" data-tip={item.info}>
                                            <p style={{position: 'relative', bottom: '7px'}}>i</p>
                                        </span>
                                    </Tooltip>
                                    </div>
                                </div>
                                <div className="pure-u-1-4 card category-feature">
                                    <div>{item.values.Standard}</div>
                                </div>
                                <div className="pure-u-1-4 card category-feature">
                                    <div>{item.values.Medium}</div>
                                </div>


                            </div>
                    </React.Fragment>
                )
            })
        })

        if (this.state && this.state.tierActions) {
        this.state.tierActions.forEach((tierAction) => {

            tierActions.push(
                <div key={tierAction.label.name} className="pure-u-1-4"  style={{textAlign: 'center'}}>
                    <button className="sign-up-btn">
                        <a href={tierAction.label.url} className="action-link-lg">{tierAction.label.text}</a>
                    </button>
                </div>
            )
        });
    }

        return (
            <div className="simple-detail-plan-tier-sm-md-lg">
                {!this.state.showDetailedPlanOveriew
                    ?
                    <React.Fragment>

                        <div className="accrd-view">
                            <PlansAccordion plans={this.state.plans} className="accordion-plan-tier" />
                        </div>

                        <div className="simple-plan-container">
                            <div className="container" style={{ maxWidth: '80%' }}>
                                <SimplePlanTier tiers={this.state.tiers} onClick={() => this.handleClick()}
                                    className="plan-tier" />
                            </div>
                        </div>

                    </React.Fragment>
                    :
                    <React.Fragment>

                        <div className="accrd-view">
                            <PlansAccordion plans={this.state.plans} className="accordion-plan-tier" />
                        </div>
                        <div className="detail-plan-container">

                            {/* <h4 className="category-type-main">{this.state.categories[0].name}</h4> */}

                            <div style={{ background: '#fff', width: '80%' }}>

                                {/* <div className="row">
                                    <div className="col-xs-12 col-sm-4 col-md-4 col-lg-4">
                                        <h4 className="category-type-main">{this.state.categories[0].name}</h4>
                                    </div>
                                    {detailRows}
                                </div> */}

                                <div className="pure-g" style={{marginBottom: '-60px'}}>
                                    
                                    <div class="pure-u-1-4">&nbsp;</div>
                                    
                                    {detailRows}
                                    
                                    {/* <div className="pure-u-1-4"> */}

                                    {/* <h4 className="category-type-main">{this.state.categories[0].name}</h4> */}
                                    {/* </div> */}

                                </div>

                                {categoryFeatures}

                                <br />
                                <div className="pure-g">
                                    
                                    <div class="pure-u-1-4" style={{textAlign: 'center'}}>&nbsp;</div>
                                    
                                    {tierActions}
                                </div>

                                <br />

                                <button className="sign-up-btn view-simple-tier-btn" onClick={() => this.handleClick()}>
                                    <div className="action-link-lg view-simple-tier">View Simple Plan Tier</div>
                                </button>
                            </div>
                        </div>
                    </React.Fragment>
                }
            </div>


        );
    }
}

// Render a Reactstrap Button element onto root
// <Button color="danger">Hello, world!</Button>
//     <LikeButton />
ReactDOM.render(
    <React.Fragment>
        <PricingPage />
    </React.Fragment>,
    document.getElementById('root')
);