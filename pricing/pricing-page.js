const {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton } = reactAccessibleAccordion;

var teirsData = tiers;

var plansAndFeaturesData = plansAndFeatures;

class Tooltip extends React.Component {
    constructor (props) {
        super(props)

        this.state = {
            displayTooltip: false
        }
        this.hideTooltip = this.hideTooltip.bind(this)
        this.showTooltip = this.showTooltip.bind(this)
    }

    hideTooltip() {
        this.setState({ displayTooltip: false })

    }
    showTooltip() {
        this.setState({ displayTooltip: true })
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

    constructor (props) {
        super(props);

        this.state = {
            tiers: teirsData.tiers,
            showMonthlyPlan: true,
            selectedOption: true,
            radio_btn_monthly_opt: teirsData.radio_btn_monthly_opt,
            radio_btn_yearly_opt: teirsData.radio_btn_yearly_opt,
            showContactForm: false,
            contactFormData: contactForm
        };
    }

    yearlyToggle() {
        console.log("in yearlyToggle func, this.state", this.state);
        this.setState({
            selectedOption: !this.state.selectedOption,
            showMonthlyPlan: !this.state.showMonthlyPlan
        })
    }

    contactFormToggle() {
        console.log("in contactFormToggle func, this.state", this.state);
        this.setState({
            showContactForm: !this.state.showContactForm
        })
    }

    radioChange(e) {
        this.setState({
            // selectedOption: e.currentTarget.value,
            selectedOption: !this.state.selectedOption,
            showMonthlyPlan: !this.state.showMonthlyPlan
        });
    }

    render() {

        const rows = [];

        this.state.tiers.forEach((tier) => {

            rows.push(
                <div key={tier.name} className="pure-u-1-2">
                    <div className="price-card">
                        <div className="pricing-panel-wrapper">
                            <div className="pricing-panel">
                                { (tier.popular && tier.popular == "True") ?
                                <div class="pricing-panel-ribbon">
                                    <h5 class="featured-title">
                                        {tier.popularInfoText}
                                    </h5>
                                </div> : 
                                <div style={{marginTop: '10%'}}></div>}
                                <div className="pricing-panel-header" style={{border: '3px solid #ffb5b3', borderBottom: '0'}}>
                                    <h6 className="pricing-panel-tier" >{tier.name}</h6>
                                    {(tier.showContact && tier.showContact == "True") ? 
                                    <React.Fragment>
                                        <button className="contact-us-btn" onClick={() => this.contactFormToggle()}>
                                            <div className="contact-action-label">{tier.contactFormText}</div>
                                        </button>
                                    </React.Fragment>: 
                                    <React.Fragment>
                                        {this.state.showMonthlyPlan ?
                                            <React.Fragment>
                                                <h2 className="product-price product-price-lg">
                                                    <span className="currency">{tier.pricing.monthly.currency}</span>
                                                    <span className="price">{tier.pricing.monthly.price}</span>
                                                    <span className="period">{tier.pricing.monthly.label}</span>
                                                </h2>
                                                <div className="pricing-panel-info">
                                                    <div className="text-yearly-color">
                                                        <p data-alt-text="$950 billed yearly<br />Save $238/year" className="year-pricing">
                                                            {tier.pricing.yearly.currency}{tier.pricing.yearly.price}{tier.pricing.monthly.label} {this.state.tiers[0].monthlyText} <div className="yearly" onClick={() => this.yearlyToggle()}> {this.state.tiers[0].payText}</div>
                                                        </p>
                                                    </div>
                                                </div>
                                            </React.Fragment>
                                            :
                                            <React.Fragment>
                                                <h2 className="product-price product-price-lg">
                                                    <span className="currency">{tier.pricing.yearly.currency}</span>
                                                    <span className="price">{tier.pricing.yearly.price}</span>
                                                    <span className="period">{tier.pricing.monthly.label}</span>
                                                </h2>
                                                <div className="pricing-panel-info">
                                                    <div className="text-yearly-color">
                                                        <p data-alt-text="$950 billed yearly<br />Save $238/year" className="year-pricing">
                                                            {tier.pricing.yearly.currency}{tier.pricing.yearly.perAnnum} {this.state.tiers[0].yearlyText1}<br /> {this.state.tiers[0].yearlyText2} {tier.pricing.yearly.currency}{tier.pricing.yearly.savedAmount}{tier.pricing.yearly.label}
                                                        </p>
                                                    </div>
                                                </div>
                                            </React.Fragment>
                                        }
                                    </React.Fragment>
                                    }
                                    <p></p>
                                    <p>{tier.description}</p>
                                    <p></p>
                                </div>
                                <div className="pricing-panel-footer" style={{border: '3px solid #ffb5b3', borderTop: '0'}}>
                                    <div className="cta-wrapper">
                                        <button className="sign-up-btn">
                                            <a href={tier.call_to_action.url} className="action-link-lg">{tier.call_to_action.text}</a>
                                        </button>
                                    </div>
                                    <p className="compare-plans" onClick={() => this.props.onClick()}>{this.state.tiers[0].compareText}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );

        });

        let offerOptions= [];

        this.state.contactFormData.offer_options.forEach((item) => {

            offerOptions.push(
                <React.Fragment>
                    <input type="checkbox" name={item} value={item} />{item}<br />
                </React.Fragment>
            )
        })
    

        return (
            <React.Fragment>
                { this.state.showContactForm ? 

                    <React.Fragment>
                        <div style={{ width: '920px' }}>
                            <div  className="contact-form">
                                <div className="pure-g">
                                    <div className="pure-u-1">

                                        <svg width="60px" height="60px" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M1.4 6.5L10 11l8.6-4.5" fill="none" stroke="currentColor" />
                                            <path d="M1 4v12h18V4H1zm17 11H2V5h16v10z" />   
                                        </svg>
                                        <br />
                                        {this.state.contactFormData.heading}
                                    </div>
                                </div>
                                <div className="pure-g">
                                    <div  className="pure-u-1">
                                        {this.state.contactFormData.sub_info}
                                    </div>
                                </div>
                                <br />
                                <div className="pure-g">

                                    <div className="pure-u-1-2 offer-options">
                                        {offerOptions}
                                    </div>

                                    <div className="pure-u-1-2 text-area-option">
                                    <input style={{width: '416px', border: '1px solid black'}} type="feature-req-email" placeholder="enter your email."
                                        id="feature-req-email" name="feature-req-email" required="" />
                                    <br />
                                    <textarea style={{marginTop: '20px', border: '1px solid black'}} rows="6" cols="50" placeholder={this.state.contactFormData.place_holder}></textarea>
                                    </div>
                                </div>
                                
                                <br />

                                <button className="contact-us-btn" style={{float: 'right'}}>
                                {/* onClick={() => this.contactFormToggle()} */}
                                    <div className="contact-action-label">{this.state.contactFormData.submitContactFormText}</div>
                                </button>

                                <button className="contact-us-btn" style={{float: 'left'}} onClick={() => this.contactFormToggle()}>
                                    <div className="contact-action-label">{this.state.contactFormData.toggleContactFormText}</div>
                                </button>
                            </div>
                        </div>
                    </React.Fragment>
                     : 
                    <React.Fragment>
                        <div style={{ maxWidth: '80%' }}>
                            <div className="pure-g">
                                <div className="pure-u-2-4 input-radio-plan">
                                    <input type="radio"
                                        value={true}
                                        checked={this.state.selectedOption == true}
                                        onChange={($event) => this.radioChange($event)} />&nbsp;<span>{this.state.radio_btn_monthly_opt}</span>
                                </div>
                                <div className="pure-u-2-4 input-radio-plan">
                                    <input type="radio"
                                        value={false}
                                        checked={this.state.selectedOption == false}
                                        onChange={($event) => this.radioChange($event)}/>&nbsp;<span style={{marginLeft: '5px'}}>{this.state.radio_btn_yearly_opt}</span>
                                </div>
                            </div>
                            <br />
                            <div className="pure-g">
                                {rows}
                            </div>
                        </div>
                    </React.Fragment>
                }
            </React.Fragment>   
        );
    }
};

class CategoryFeatures extends React.Component {
    render() {

        let categoryFeatures = [];

        let val;

        this.props.categories.forEach((category, i) => {

            // get the tier name
            val = this.props.plan_name;

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
                                        <span>
                                            <svg width="20px" height="20px" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">

                                                <path d="M12.13 11.59c-.16 1.25-1.78 2.53-3.03 2.57-2.93.04.79-4.7-.36-5.79.56-.21 1.88-.54 1.88.44 0 .82-.5 1.74-.74 2.51-1.22 3.84 2.25-.17 2.26-.14.02.03.02.17-.01.41-.05.36.03-.24 0 0zm-.57-5.92c0 1-2.2 1.48-2.2.36 0-1.03 2.2-1.49 2.2-.36z" />
                                                <circle cx="10" cy="10" r="9" fill="none" stroke="currentColor" stroke-width="1.1" />
                                            </svg>
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

    constructor (props) {
        super(props);

        this.state = {
            showMonthlyPlan: true,
            tiers: teirsData.tiers,
            accordionPlans: plansAndFeatures
        };
    }

    yearlyToggle() {
        console.log("in yearlyToggle func, this.state", this.state);
        this.setState({
            showMonthlyPlan: !this.state.showMonthlyPlan
        })
    }

    render() {

        let plansAccordion = [];

        this.state.tiers.forEach((tier, i) => {

            plansAccordion.push(
                <AccordionItem key={tier.name}>
                    {this.state.showMonthlyPlan ?
                        <React.Fragment>
                            <AccordionItemHeading>
                                <AccordionItemButton>
                                    {/* get this data from tiers uusing index reference whilst iterating over plans_and_features */}
                                    <span className="plan-name">{tier.name}</span>
                                    <h2 className="product-price product-price-sm">
                                        <span className="currency" data-alt-text="$">{tier.pricing.monthly.currency}</span>
                                        <span className="price" data-alt-text="79">{tier.pricing.monthly.price}</span>
                                        <span className="period">{tier.pricing.monthly.label}</span>
                                    </h2>
                                </AccordionItemButton>
                            </AccordionItemHeading>
                            <AccordionItemPanel style={{ background: '#f5505017', textAlign: 'center' }}>
                                {/* get this from tiers as well */}
                                <p className="text-light-gray">{tier.pricing.monthly.currency}{tier.pricing.yearly.price} {this.state.tiers[0].monthlyText} <div className="yearly" onClick={() => this.yearlyToggle()}> {this.state.tiers[0].payText}</div></p>
                                <p>{tier.description}</p>
                                <button className="sign-up-btn-xs">
                                    <a href={tier.call_to_action.url} className="action-link">{tier.call_to_action.text}</a>
                                </button>
                                {/* get this from plans_and_features.js */}
                                <CategoryFeatures categories={this.state.accordionPlans.categories} plan_name={tier.name} />
                            </AccordionItemPanel>
                        </React.Fragment>
                        :
                        <React.Fragment>
                            <AccordionItemHeading>
                                <AccordionItemButton>
                                    {/* get this data from tiers uusing index reference whilst iterating over plans_and_features */}
                                    <span className="plan-name">{tier.name}</span>
                                    <h2 className="product-price product-price-sm">
                                        <span className="currency" data-alt-text="$">{tier.pricing.yearly.currency}</span>
                                        <span className="price" data-alt-text="79">{tier.pricing.yearly.price}</span>
                                        <span className="period">{tier.pricing.monthly.label}</span>
                                    </h2>
                                </AccordionItemButton>
                            </AccordionItemHeading>
                            <AccordionItemPanel style={{ background: '#f5505017', textAlign: 'center' }}>
                                <p className="text-light-gray">{tier.pricing.monthly.currency}{tier.pricing.yearly.perAnnum} {this.state.tiers[0].yearlyText1}<br /> {this.state.tiers[0].yearlyText2} {tier.pricing.monthly.currency}{tier.pricing.yearly.savedAmount}{tier.pricing.yearly.label}</p>
                                <p>{tier.description}</p>
                                <button className="sign-up-btn-xs">
                                    <a href={tier.call_to_action.url} className="action-link">{tier.call_to_action.text}</a>
                                </button>
                                <CategoryFeatures categories={this.state.accordionPlans.categories} plan_name={tier.name} />
                            </AccordionItemPanel>
                        </React.Fragment> 
                    }
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
            tiers: teirsData.tiers,
            categories: plansAndFeaturesData.categories,
            tooltipOpen: false,
        };
    }

    handleClick() {

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
    componentDidMount() {

        this.setState({
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
                        <span className="period">{tier.pricing.monthly.label}</span>
                    </h2>
                </div>
            )
        });

        let val1 = this.state.tiers[0].name;

        let val2 = this.state.tiers[1].name;

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

                                <div className="category-name">{item.name}&nbsp;
                                    <Tooltip message={item.info} position={'top'}>
                                        <span>
                                            <svg width="20px" height="20px" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">

                                                <path d="M12.13 11.59c-.16 1.25-1.78 2.53-3.03 2.57-2.93.04.79-4.7-.36-5.79.56-.21 1.88-.54 1.88.44 0 .82-.5 1.74-.74 2.51-1.22 3.84 2.25-.17 2.26-.14.02.03.02.17-.01.41-.05.36.03-.24 0 0zm-.57-5.92c0 1-2.2 1.48-2.2.36 0-1.03 2.2-1.49 2.2-.36z" />
                                                <circle cx="10" cy="10" r="9" fill="none" stroke="currentColor" stroke-width="1.1" />
                                            </svg>
                                        </span>
                                    </Tooltip>
                                </div>
                            </div>
                            <div className="pure-u-1-4 card category-feature">
                                <div>{item.values[val1]}</div>
                            </div>
                            <div className="pure-u-1-4 card category-feature">
                                <div>{item.values[val2]}</div>
                            </div>


                        </div>
                    </React.Fragment>
                )
            })
        })

        if (this.state && this.state.tierActions) {
            this.state.tierActions.forEach((tierAction) => {

                tierActions.push(
                    <div key={tierAction.label.name} className="pure-u-1-4" style={{ textAlign: 'center' }}>
                        <button className="sign-up-btn" style={{ width: '100%', fontSize: '12px !important' }}>
                            <a href={tierAction.label.url} className="action-link-lg-dtl" style={{fontSize: '12px !important'}}>{tierAction.label.text}</a>
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
                            <PlansAccordion className="accordion-plan-tier" />
                        </div>

                        <div className="simple-plan-container">

                                <SimplePlanTier onClick={() => this.handleClick()}
                                    className="plan-tier" />
                        </div>

                    </React.Fragment>
                    :
                    <React.Fragment>

                        <div className="accrd-view">
                            <PlansAccordion className="accordion-plan-tier" />
                        </div>
                        <div className="detail-plan-container">

                            <div style={{ background: '#fff', width: '80%' }}>

                                <div className="pure-g" style={{ marginBottom: '-60px' }}>

                                    <div class="pure-u-1-4">&nbsp;</div>

                                    {detailRows}

                                </div>

                                {categoryFeatures}

                                <br />
                                <div className="pure-g">

                                    <div class="pure-u-1-4" style={{ textAlign: 'center' }}>&nbsp;</div>

                                    {tierActions}
                                </div>

                                <br />

                                <button className="sign-up-btn view-simple-tier-btn" onClick={() => this.handleClick()}>
                                    <div className="action-link-lg view-simple-tier">{this.state.tiers[0].toggleText}</div>
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