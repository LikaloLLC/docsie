const {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemPanel,
    AccordionItemButton } = reactAccessibleAccordion;

var teirsData = tiers;

var plansAndFeaturesData = plansAndFeatures;

// used to show offer options in contact form
class OfferOptions extends React.Component {
    constructor (props) {
        super(props);

        // // console.log("props in OfferOptions", props);
    }

    render() {

        let offerOptions = [];

        this.props.item.offer_options.forEach((option) => {

            let ref = option.alias;

            // // console.log("this", this, "this[ref]", this[ref]);

            offerOptions.push(
                <React.Fragment>
                    {/* {option.required ?  */}
                    {(this.props.requiredFields.indexOf(option.alias) != -1) ?
                        <React.Fragment>
                            <input type={option.type} className="offer-options" ref={this[ref]} name={option.alias} value={option.value} onChange={() => this.props.handleInputChange(this.props.item, event)} required/> <span>{option.value}*</span><br />
                        </React.Fragment>:
                        <React.Fragment>
                            <input type={option.type} className="offer-options" ref={ref} name={option.alias} value={option.value} onChange={() => this.props.handleInputChange(this.props.item, event)} /><span>{option.value}</span><br />
                        </React.Fragment>
                    }
                </React.Fragment>
            )
        })

        return (
            <React.Fragment>
                {offerOptions}
            </React.Fragment>
        )
    }
}

class SelectTag extends React.Component {

    constructor (props) {
        super(props);

        // // console.log("props in OfferOptions", props);
    }

    render() {

        return (
            <React.Fragment>
            {/* {this.props.item.required ?  */}
            {(this.props.requiredFields.indexOf(this.props.item.alias.label) != -1) ?
            <React.Fragment>
                <span className="form-label">{this.props.item.label}*</span><br />
                <select className={this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr"} name={this.props.item.alias.label} onChange={() => this.props.handleInputChange(this.props.item, event)} required>
                    <option value="Select" selected="selected">{this.props.item.selectMsg}</option>
                    {this.props.item.options.map((opt) =>
                        <option value={opt}>{opt}</option>
                    )}
                </select>
            </React.Fragment>   :
            <React.Fragment>
                <span className="form-label">{this.props.item.label}</span><br />
                <select className={this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr"} name={this.props.item.alias.label} onChange={() => this.props.handleInputChange(this.props.item, event)}>
                    <option value="Select" selected="selected">{this.props.item.selectMsg}</option>
                    {this.props.item.options.map((opt) =>
                        <option value={opt}>{opt}</option>
                    )}
                </select>
            </React.Fragment>
            }
            </React.Fragment>
        )
    }
}

// handles dynamic json to configure contact form input
class ContactFormInputs extends React.Component {

    constructor (props) {
        super(props);

        // this.state = contactForm.formState;
        
        // this.state = Object.assign(this.state, {formInputs: contactForm.formInputs});

        // create a ref to store the textInput DOM element
        this.emailInput = React.createRef();

        this.taInput = React.createRef();

        this.state = {};

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
        this.setContactFormState(contactForm.formInputs);
    }

    // sets contact form state
    setContactFormState(data, onSubmitRes, resData) {

        data.forEach((item) => {

            // create alias for offer_options
            if (item.type=="offer_options") {

                    this.state = Object.assign(this.state, {"optionsAlias": item.alias.label})

                    item.offer_options.forEach((opt) => {

                    let ref = opt.alias;
                    
                    // let refObj = React.createRef();
                    
                    // clear off checkbox
                    if (this[ref] && this[ref].current && this[ref].current.checked == true) {
                        this[ref].current.checked = false;
                    } else {

                        this[ref] = React.createRef(); 
                    }
                });
            }

            // check alias type and set status based on that
            if (item.alias) {
                if ((item.alias.valueType).toLowerCase() == "string") {
                    this.state[item.alias.label] = "";
                } else if ((item.alias.valueType).toLowerCase() == "array") {
                    if (item.alias.arrayType == "requiredFields")
                        this.state[item.alias.label] = item[item.alias.label];
                    else 
                    this.state[item.alias.label] = [];
                } else if ((item.alias.valueType).toLowerCase() == "number") {
                    this.state[item.alias.label] = 0;
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
            this.state.submitRes = <li id="notification" className="pure-notification-message pure-notification-success" style={{animationDuration: '6000ms'}}>
                                        <svg class="icon icon--check" viewBox="0 0 20 20" width="22" height="22" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M4 10l4 5 9-11" fill="none" stroke="currentColor" stroke-width="1.1"/>
                                        </svg>
                                    
                                        <span>{contactForm.submitRes}</span><div role="presentation" className="pure-notification-progress" style={{animationDuration: '6000ms'}}></div>
                                    </li>
        } else if (resData) {
           
            // this is used to show err msg from backend
            // get the keys of resData
            let resDatakeys = Object.keys(resData);

            let errNode = [];

            for (let key in resDatakeys) {

                errNode.push(
                    <span>
                        {key}: {resDatakeys[key]}
                    </span>
                )
            }

            this.state.submitRes = <li id="notification" className="pure-notification-message pure-notification-success" style={{animationDuration: '6000ms'}}>
                                        <svg class="icon icon--check" viewBox="0 0 20 20" width="22" height="22" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M4 10l4 5 9-11" fill="none" stroke="currentColor" stroke-width="1.1"/>
                                        </svg>
                                    
                                        <span>{errNode}</span><div role="presentation" className="pure-notification-progress" style={{animationDuration: '6000ms'}}></div>
                                    </li>            

        } else {
            this.state.submitRes = "";
        }
        // // console.log("this.state in contact form", this.state);

}


    setButtonDisability(item, event) {

        let disabledCount = 0;
        
        // check if all the required fields are entered and enable submit  button
        this.state.requiredFields.forEach((field) => {

            // // console.log("checking if value exists to remove disable option on button", this.state[field]);

            // // if value exists, set disabled state to false, else true 
            // // offer_options is an array
            // if (this.state[field] == "" || this.state[field] == undefined || (typeof this.state[field] == "object" && this.state[field].indexOf(field) == -1)) {

            //     disabledCount++;
            // }
            // if value exists, set disabled state to false, else true 
            // offer_options is an array
            if (this.state[field] == "" || this.state[field] == undefined || this.state[field] == "Select" || this.state[this.state.optionsAlias].length == 0) {

                disabledCount++;
            }
        })

        if(this.emailInput.current.validity.valid == false) {
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
            })
        } else {
            // this.state.disabled = false;
            this.setState({
                disabled: false
            })
        }
    }

    handleInputChange(item, event) {

        // // console.log("selected item", item, "value in handleInputChange", event.target.value);

        // // console.log("this.emailInput", this.emailInput);

        // if offer_options are selected, multiple checked fields are pushed and set into state
        if (item.type == "offer_options") {

            let updatedOffrOpts = this.state[item.alias.label];

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

            this.setState({
                [item.alias.label]: updatedOffrOpts
            }, function(){

                // // console.log("state in handleInputChange callback", this.state); 
                this.setButtonDisability(item, event);
            });

        } else {

            this.setState({
                [item.alias.label]: event.target.value
            }, function(){

                // // console.log("state in handleInputChange callback", this.state); 
                this.setButtonDisability(item, event);
            });
        }
    }

    submitContactForm() {

        // // console.log("in submitForm func, state is::", this.state);

        let reqBody = Object.assign({}, this.state);

        delete reqBody.requiredFields;

        delete reqBody.endPoint;

        delete reqBody.disabled;

        delete reqBody.formInputs;

        delete reqBody.optionsAlias;

        delete reqBody.notificationDuration;

        delete reqBody.submit;

        delete reqBody.submitRes;

        // // console.log("contact post request body", this.state);

        let submitResNode =  <li id="notification" className="pure-notification-message pure-notification-success" style={{animationDuration: '6000ms'}}>
                                <svg class="icon icon--check" viewBox="0 0 20 20" width="22" height="22" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M4 10l4 5 9-11" fill="none" stroke="currentColor" stroke-width="1.1"/>
                                </svg>
                            
                                <span>{contactForm.loadingMsg}</span><div role="presentation" className="pure-notification-progress" style={{animationDuration: '6000ms'}}></div>
                            </li>

        // show loading msg on cclicking submit
        this.setState({submitRes: submitResNode});

        fetch(this.state.endPoint, {
            method: 'POST',
            headers: {
                "Content-type": "application/json;"
            },
            body: JSON.stringify(reqBody)
        })
        .then(response => response.json())
        .then((result) => {
    
            // if (result.status == "ok") {

                // console.log("result after post request", result);

                // TODO: ADD ERROR HANDLING POPUP AS WELL BASED ON RESPONSE ENDPOINT

                // clear off textarea using ref
                // // console.log("this.taInput", this.taInput);
                this.taInput.current.value = "";

                // set contact form initial state
                this.setContactFormState(contactForm.formInputs, true);

                // restore form to initial state
                this.setState(this.state);

                setTimeout(
                    function() {
                        this.setState({submitRes: ""});
                    }
                    .bind(this),
                    this.state.notificationDuration
                );
            // } 
            // else {

            //     // this implies there has been an error response from server, do not reset form but rather show err msg
            //     this.setContactFormState(contactForm.formInputs, false, result);
            // }
    
        }, (error) => {
    
            console.log("error in submitting contact form", error);
        })
    }

    render() {

        let contactFormInputs = [];

        this.props.formInputs.forEach((item, i) => {

            // console.log("item, i", item, i);
            if (item.type == "text" || item.type == "number" || item.type == "radio") {

                // console.log("item.type is text");

                contactFormInputs.push(
                    <div className="pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 contact-input">
                        
                        {(this.state.requiredFields.indexOf(item.alias.label) != -1) ?
                        <React.Fragment>
                            <span className="form-label">{item.label}*</span><br />
                            <input className={this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr"} type={item.type} placeholder={item.placeholder}
                                name={item.alias.label} value={this.state[item.alias.label]} onChange={() => this.handleInputChange(item, event)} required/>
                        </React.Fragment> : 
                        <React.Fragment>
                            <span className="form-label">{item.label}</span><br />
                            <input className={this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr"} type={item.type} placeholder={item.placeholder}
                                name={item.alias.label} value={this.state[item.alias.label]} onChange={() => this.handleInputChange(item, event)} />
                        </React.Fragment>
                        }
                        {/* { (item.type=="email" && this.state.emailValidity == false) ? 
                            <span className="alert-msg">
                                {this.state.emailInValidMsg}
                            </span> :
                            '' 
                        } */}
                    </div>
                );
            }

            if (item.type == "email") {

                // console.log("item.type is text");

                let emailVal = this.state[item.alias.label];

                contactFormInputs.push(
                    <div className="pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 contact-input">
                        
                        {(this.state.requiredFields.indexOf(item.alias.label) != -1) ?
                        <React.Fragment>
                            <span className="form-label">{item.label}*</span><br />
                            <input className={this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr"} ref={this.emailInput} type={item.type} placeholder={item.placeholder}
                                id="email" name={item.alias.label} value={emailVal} onChange={() => this.handleInputChange(item, event)} required/>
                        </React.Fragment> : 
                        <React.Fragment>
                            <span className="form-label">{item.label}</span><br />
                            <input className={this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr"} ref={this.emailInput} type={item.type} placeholder={item.placeholder}
                                id="email" name={item.alias} value={emailVal} onChange={() => this.handleInputChange(item, event)} />
                        </React.Fragment>
                        }
                        {/* { (item.type=="email" && this.state.emailValidity == false) ? 
                            <span className="alert-msg">
                                {this.state.emailInValidMsg}
                            </span> :
                            '' 
                        } */}
                    </div>
                );
            }

            // for dropdown
            if (item.type == "dropdown" ) {
                contactFormInputs.push(
                    <div className="pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 contact-input">
                        
                        {/* <input className={this.props.accordionView ? "contact-attr contact-attr-wdt " : "contact-attr"} type={item.type} placeholder={item.placeholder}
                            id="contact-attr" name="contact-attr" /> */}
                            <SelectTag item={item} requiredFields={this.state.requiredFields} accordionView={this.props.accordionView} handleInputChange={() => this.handleInputChange(item, event)} />
                    </div>
                );
            }

            // for checkbox group
            if (item.type == "offer_options") {

                // console.log("item.type is offer_options");


                let offerOptions = [];

                item.offer_options.forEach((option) => {

                    let ref = option.alias;

                    // console.log("this", this, "this[ref]", this[option.alias]);

                    offerOptions.push(
                        <React.Fragment>
                            {/* {option.required ?  */}
                            {(this.state.requiredFields.indexOf(option.alias) != -1) ?
                                <React.Fragment>
                                    <input type={option.type} className="offer-options" ref={this[ref]} name={option.alias} value={option.value} onChange={() => this.handleInputChange(item, event)} required/> <span>{option.value}*</span><br />
                                </React.Fragment>:
                                <React.Fragment>
                                    <input type={option.type} className="offer-options" ref={this[ref]} name={option.alias} value={option.value} onChange={() => this.handleInputChange(item, event)} /><span>{option.value}</span><br />
                                </React.Fragment>
                            }
                        </React.Fragment>
                    )
                })

                contactFormInputs.push(
                    <div className="pure-u-xs-1 pure-u-sm-1-1 pure-u-md-1-1 pure-u-lg-1-3 pure-u-xl-1-3 offer-options">
                        <span class="optn-rqd-msg">{item.optionsRequiredMsg}</span>
                        <br />
                        {/* <OfferOptions item={item} requiredFields={this.state.requiredFields} handleInputChange={() => this.handleInputChange(item, event)} /> */}
                        {offerOptions}
                    </div>
                )
            }

            if (item.type == "text_area") {

                // console.log("item.type is text_area");

                contactFormInputs.push(
                    <div className="pure-u-xs-1 pure-u-sm-1-3 pure-u-md-1-3 pure-u-lg-1-3 pure-u-xl-1-3 contact-input">
                        
                        {(this.state.requiredFields.indexOf(item.alias.label) != -1) ?
                        <React.Fragment>
                            <span className="form-label-desc">{item.label}*</span>
                            <textarea className="text-area-tg" rows="5" cols="50" ref={this.taInput} placeholder={item.placeholder} onChange={() => this.handleInputChange(item, event)} required></textarea>
                        </React.Fragment> :
                        <React.Fragment>
                            <span className="form-label-desc">{item.label}</span>
                            <textarea className="text-area-tg" rows="5" cols="50" ref={this.taInput} placeholder={item.placeholder} onChange={() => this.handleInputChange(item, event)}></textarea> 
                        </React.Fragment>
                        }
                    </div>
                )
            }
        });

        return (
            <React.Fragment>
                <div className="pure-g-r">
                    {contactFormInputs}
                    {/* pure-u-xs-1 pure-u-sm-1-2 pure-u-md-1-2 pure-u-lg-1-3 pure-u-xl-1-3  */}
                    {/* <div className="contact-input"> */}
                    {/* <div className="pure-u-xs-1 pure-u-sm-1-2 pure-u-md-1-2 pure-u-lg-1-3 pure-u-xl-1-3 accrd-actn-btn">
                        <input className="contact-us-btn" style={{ color: '#fff', fontSize: '18px', fontWeight: '700'}} type="submit" value="Submit" onClick={() => this.props.submitContactForm()}/>
                    </div> */}
                </div>
                <div className="contact-input">
                    <button className="ct-btn back-to-plans-btn-accrd" onClick={() => this.props.contactFormToggle()}>
                        <div className="back-btn-action-link-lg-dtl">
                            <svg className="ct-btn-svg" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                <path d="M13 16l-6-6 6-6" fill="none" stroke="red" stroke-width="1.03" />
                            </svg>
                            {this.props.toggleContactFormText}
                        </div>
                    </button>
                    <button className="ct-btn contact-us-btn-xs ct-btn-2" disabled={this.state.disabled} onClick={() => this.submitContactForm()}>{this.props.submitContactFormText}</button>
                    
                </div>
                <aside className="pure-notification-container">
                        <ul>
                            {this.state.submitRes ? 
                            this.state.submitRes : ''
                        }
                        </ul>
                    </aside>
            </React.Fragment>
        )
    }
}

// tooltip class used in detail component
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

// use this to show data about each tier in detailed view which also has tooltip for category feature
class DetailCategoryFeatures extends React.Component {

    constructor (props) {
        super(props);
    }

    render() {

        let val;

        let detailCategoryFeatures = [];

        for (let i = 0; i < this.props.tiers.length; i++) {

            val = this.props.tiers[i].name;

            detailCategoryFeatures.push(
                <div className="pure-u-1-4 category-feature">
                    {(this.props.item.values[val]).toLowerCase() == "yes" ? 
                        <svg class="c-check" xmlns="http://www.w3.org/2000/svg" viewBox="-255 347 100 100">
                            <title></title>
                            <path d="M-217.1 431.8c-1 1.2-2.6 2.2-4 2.3-1.4.1-3-.8-4.3-1.9l-27.5-24.5 7.8-8.7 23.2 20.6 54.6-61.7 8.6 7.9-58.4 66z"></path>
                        </svg>: 
                        <div className="category-name">{this.props.item.values[val]}</div>
                    }
                </div>
            )
        }

        return (
            <React.Fragment>
                {detailCategoryFeatures}
            </React.Fragment>
        )
    }
}

// contact form 
class ContactForm extends React.Component {

    constructor (props) {
        super(props);

        this.state = contactForm.formState;
    }

    render() {

        return (

            <React.Fragment>
                {/* <form className="contact-form-container" action={this.state.endPoint} method="post" target="_self"> */}
                <div id="contact-form" className="contact-form-container">
                    <div className={this.props.accordionView ? "pricing-contact-form-wdt" : "pricing-contact-form"}>
                        <div className="pure-g">
                            <div className="pure-u-1">

                                <svg class="ct-frm-svg" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M1.4 6.5L10 11l8.6-4.5" fill="none" stroke="currentColor" />
                                    <path d="M1 4v12h18V4H1zm17 11H2V5h16v10z" />
                                </svg>
                                <br />
                                {this.props.contactFormData.heading}
                            </div>
                        </div>
                        <div className="pure-g">
                            <div className="pure-u-1">
                                {this.props.contactFormData.sub_info}
                            </div>
                        </div>
                        <br />

                        {/* this.props.accordionView implies it is mobile viewport and show responsive contact form */}
                        <React.Fragment>
                            {this.props.accordionView ?
                                <React.Fragment>

                                    <ContactFormInputs formInputs={this.props.contactFormData.formInputs}
                                        accordionView={this.props.accordionView}
                                        contactFormToggle={() => this.props.contactFormToggle()}
                                        toggleContactFormText={this.props.contactFormData.toggleContactFormText}
                                        submitContactFormText={this.props.contactFormData.submitContactFormText} />

                                </React.Fragment>
                                :
                                <React.Fragment>

                                    <ContactFormInputs formInputs={this.props.contactFormData.formInputs}
                                        accordionView={this.props.accordionView}
                                        contactFormToggle={() => this.props.contactFormToggle()}
                                        toggleContactFormText={this.props.contactFormData.toggleContactFormText}
                                        submitContactFormText={this.props.contactFormData.submitContactFormText} />

                                </React.Fragment>
                            }
                        </React.Fragment>

                        <br />
                    </div>
                </div>
            </React.Fragment>
        )
    }
}

// simple plan tier
class SimplePlanTier extends React.Component {

    constructor (props) {
        super(props);

        // console.log("props in simplePlanTier", props);

        this.state = {
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
    }

    render() {

        const rows = [];

        this.state.tiers.forEach((tier) => {

            rows.push(
                <div key={tier.name} className="pure-u-xs-1 pure-u-sm-1-2 pure-u-md-1-3 pure-u-lg-1-3 pure-u-xl-1-3">
                    <div className="price-card">
                        <div className="pricing-panel-wrapper wrp-2">
                            <div className="pricing-panel">
                                {(tier.popular && tier.popular == "True") ?
                                    <div class="pricing-panel-ribbon">
                                        <h5 class="featured-title">
                                            {tier.popularInfoText}
                                        </h5>
                                    </div> :
                                    <div className="wrp-arnd"></div>}
                                {/* <div className={(tier.popular == "True") ? "pricing-panel-header popular-header" : "pricing-panel-header"}> */}
                                <div className="pricing-panel-header">
                                    <h6 className="pricing-panel-tier" >{tier.name}</h6>
                                    {(tier.showCallToAction && tier.showCallToAction == "True") ?
                                        <React.Fragment>
                                            {/* if  tier.call_to_action.type is CONTACT, add contactFormToggle func */}
                                            {(tier.call_to_action.type == "contact") ?
                                                // add contact page toggle if type is contact
                                                <button className="contact-us-btn" onClick={() => this.props.contactFormToggle()}>
                                                    {/* <div className="contact-action-label">{tier.contactFormText}</div> */}
                                                    <span className="contact-action-label">{tier.call_to_action.text}</span>
                                                </button>
                                                :
                                                <React.Fragment>
                                                    {/* if tier.call_to_action.type is sign-up-free, call to action is of type link */}
                                                {(tier.call_to_action.type == "link") ?
                                                    <a href={tier.call_to_action.url} className="contact-us-btn">
                                                        {/* <div className="contact-action-label">{tier.contactFormText}</div> */}
                                                        <span className="contact-action-label">{tier.call_to_action.text}</span>
                                                    </a> : '' }
                                                </React.Fragment>
                                            }
                                        </React.Fragment> :
                                        <React.Fragment>
                                            {this.props.showMonthlyPlan ?
                                                <React.Fragment>
                                                    <h2 className="product-price product-price-lg">
                                                        <span className="currency">{tier.pricing.monthly.currency}</span>
                                                        <span className="price">{tier.pricing.monthly.price}</span>
                                                        <span className="period">{tier.pricing.monthly.label}</span>
                                                    </h2>
                                                    <div className="pricing-panel-info">
                                                        <div className="text-yearly-color">
                                                            <p data-alt-text="$950 billed yearly<br />Save $238/year" className="year-pricing">
                                                                {tier.pricing.yearly.currency}{tier.pricing.yearly.price}{tier.pricing.monthly.label} <div className="yearly" onClick={() => this.props.yearlyToggle()}> {this.state.monthlyText}</div>
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
                                                                {tier.pricing.yearly.currency}{tier.pricing.yearly.perAnnum} {this.state.yearlyText} {tier.pricing.yearly.currency}{tier.pricing.yearly.savedAmount}{tier.pricing.yearly.label}
                                                            </p>
                                                        </div>
                                                    </div>
                                                </React.Fragment>
                                            }
                                        </React.Fragment>
                                    }
                                    <p></p>
                                    {(tier.showCallToAction && tier.showCallToAction == "True") ?
                                        <p className="desc-text">{tier.description}</p>
                                        :
                                        <p>{tier.description}</p>
                                    }
                                    <p></p>
                                </div>
                                <div className="pricing-panel-footer">
                                    {(tier.showCallToAction && tier.showCallToAction == "False") ?
                                        <div className="cta-wrapper">
                                            <a href={tier.call_to_action.url} className="sign-up-btn">
                                                <div className="action-link-lg">{tier.call_to_action.text}</div>
                                            </a>
                                        </div> : <div className="ftr-wrp"></div>
                                    }
                                    <a href="#detail-plan-container" className="compare-plans pln" onClick={() => this.props.onClick()}>{this.state.compareText}</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );

        });

        return (
            <React.Fragment>
                {this.props.showContactForm ?
                    <div className="contact-form-container-smpl">
                        <ContactForm contactFormData={this.state.contactFormData} contactFormToggle={() => this.props.contactFormToggle()}
                            showContactForm={this.props.showContactForm} submitContactForm={() => this.props.submitContactForm()} />
                    </div>
                    :
                    <React.Fragment>
                        <div className="simple-plans-container">
                            <div className="pure-g-r">
                                {rows}
                            </div>
                        </div>
                    </React.Fragment>
                }
            </React.Fragment>
        );
    }
};

class DetailedPlanTier extends React.Component {

    constructor (props) {
        super(props);

        this.state = {
            plansAndFeaturesInfo: plansAndFeaturesData.plansAndFeaturesInfo
        }
    }

    render() {

        let detailRows = [];

        let categoryFeatures = [];

        let tierActions = [];

        this.props.tiers.forEach((tier) => {

            detailRows.push(
                <div key={tier.name} className="pure-u-1-4 category-feature-head">
                    <h4 className="pricing-name">{tier.name}</h4>
                    {(tier.showCallToAction && tier.showCallToAction == "True") ?
                        <React.Fragment>
                        {/* if  tier.call_to_action.type is CONTACT, add contactFormToggle func */}
                        {(tier.call_to_action.type == "contact") ?
                            // add contact page toggle if type is contact
                            <button className="contact-us-btn-dtl" onClick={() => this.props.contactFormToggle()}>
                                {/* <div className="contact-action-label">{tier.contactFormText}</div> */}
                                <span className="contact-action-label">{tier.call_to_action.text}</span>
                            </button>
                            :
                            <React.Fragment>
                                {/* if tier.call_to_action.type is sign-up-free, call to action is of type link */}
                            {(tier.call_to_action.type == "link") ?
                                <a href={tier.call_to_action.url} className="contact-us-btn-dtl">
                                    {/* <div className="contact-action-label">{tier.contactFormText}</div> */}
                                    <span className="contact-action-label">{tier.call_to_action.text}</span>
                                </a> : '' }
                            </React.Fragment>
                        }
                    </React.Fragment> :
                        <React.Fragment>
                            {this.props.showMonthlyPlan ?
                                <React.Fragment>
                                    <h2 className="product-price product-price-md">
                                        <span className="currency">{tier.pricing.monthly.currency}</span>
                                        <span className="price">{tier.pricing.monthly.price}</span>
                                        <span className="period">{tier.pricing.monthly.label}</span>
                                    </h2>
                                    {/* <div className="pricing-panel-info">
                                        <div className="text-yearly-color">
                                            <p data-alt-text="$950 billed yearly<br />Save $238/year" className="year-pricing">
                                                {tier.pricing.yearly.currency}{tier.pricing.yearly.price}{tier.pricing.monthly.label} {this.state.tiers[0].monthlyText} <div className="yearly" onClick={() => this.yearlyToggle()}> {this.state.tiers[0].payText}</div>
                                            </p>
                                        </div>
                                    </div> */}
                                </React.Fragment>
                                :
                                <React.Fragment>
                                    <h2 className="product-price product-price-md">
                                        <span className="currency">{tier.pricing.yearly.currency}</span>
                                        <span className="price">{tier.pricing.yearly.price}</span>
                                        <span className="period">{tier.pricing.monthly.label}</span>
                                    </h2>
                                    {/* <div className="pricing-panel-info">
                                        <div className="text-yearly-color">
                                            <p data-alt-text="$950 billed yearly<br />Save $238/year" className="year-pricing">
                                                {tier.pricing.yearly.currency}{tier.pricing.yearly.perAnnum} {this.state.tiers[0].yearlyText1}<br /> {this.state.tiers[0].yearlyText2} {tier.pricing.yearly.currency}{tier.pricing.yearly.savedAmount}{tier.pricing.yearly.label}
                                            </p>
                                        </div>
                                    </div> */}
                                </React.Fragment>
                            }
                        </React.Fragment>
                    }
                    {/* <h2 className="product-price product-price-md">
                        <span className="currency">{tier.pricing.monthly.currency}</span>
                        <span className="price">{tier.pricing.monthly.price}</span>
                        <span className="period">{tier.pricing.monthly.label}</span>
                    </h2> */}
                </div>
            )
        });

        this.props.categories.forEach((category, i) => {
            category.features.forEach((item, j) => {

                categoryFeatures.push(

                    <React.Fragment>

                        {/* {i != 0 && j == 0 ? */}
                        {j == 0 ?
                            <React.Fragment>
                                <div className="category-name-hdr">
                                    <h4>{category.name}</h4>
                                </div>
                            </React.Fragment>
                            : ''}
                        <div className="pure-g" key={item.name}>
                            <div className="pure-u-1-4 card category-feature-name ctg-wrp">

                                <div className="category-name">{item.name}&nbsp;
                                { 
                                    item.info ?
                                        <Tooltip message={item.info} position={'top'}>
                                            <span>
                                                <svg class="ttp-svg" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">

                                                    <path d="M12.13 11.59c-.16 1.25-1.78 2.53-3.03 2.57-2.93.04.79-4.7-.36-5.79.56-.21 1.88-.54 1.88.44 0 .82-.5 1.74-.74 2.51-1.22 3.84 2.25-.17 2.26-.14.02.03.02.17-.01.41-.05.36.03-.24 0 0zm-.57-5.92c0 1-2.2 1.48-2.2.36 0-1.03 2.2-1.49 2.2-.36z" />
                                                    <circle cx="10" cy="10" r="9" fill="none" stroke="currentColor" stroke-width="1.1" />
                                                </svg>
                                            </span>
                                        </Tooltip> : '' 
                                }
                                </div>
                            </div>
                            {/* <div className="pure-u-1-4 card category-feature">
                                <div>{item.values[val1]}</div>
                            </div>
                            <div className="pure-u-1-4 card category-feature">
                                <div>{item.values[val2]}</div>
                            </div>
                            <div className="pure-u-1-4 card category-feature">
                                <div>{item.values[val3]}</div>
                            </div> */}

                            {/* send tiers, item props and get each tier feature details */}
                            <DetailCategoryFeatures tiers={this.props.tiers} item={item} />

                        </div>
                    </React.Fragment>
                )
            })
        })

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

        this.props.tiers.forEach((tier) => {

            tierActions.push(
                <React.Fragment>
                    {(tier.showCallToAction && tier.showCallToAction == "True") ?

                    <React.Fragment>
                        {/* if  tier.call_to_action.type is CONTACT, add contactFormToggle func */}
                        {(tier.call_to_action.type == "contact") ?
                            // add contact page toggle if type is contact
                            <a href="#contact-form" className="pure-u-1-4 card-actn category-feature-actn cta-dtl-wrp" onClick={() => this.props.contactFormToggle()}>
                                {/* <div className="contact-action-label">{tier.contactFormText}</div> */}
                                <span className="tier-actn">{tier.call_to_action.text}</span>
                            </a>
                            :
                            <React.Fragment>
                                {/* if tier.call_to_action.type is sign-up-free, call to action is of type link */}
                            {(tier.call_to_action.type == "link") ?
                                <a href={tier.call_to_action.url} className="pure-u-1-4 card-actn category-feature-actn">
                                    {/* <div className="contact-action-label">{tier.contactFormText}</div> */}
                                    <span className="tier-actn">{tier.call_to_action.text}</span>
                                </a> : '' }
                            </React.Fragment>
                        }
                    </React.Fragment>: ''}
                </React.Fragment>)
        });

        return (
            <React.Fragment>
                {this.props.showContactForm ?

                    <React.Fragment>
                        {/* <div className="contact-form-container-smpl contact-form-container-dtl">
                            <ContactForm contactFormData={this.props.contactFormData}
                                contactFormToggle={() => this.props.contactFormToggle()}
                                submitContactForm={() => this.props.submitContactForm()} />
                        </div> */}
                    </React.Fragment>
                     :
                    <React.Fragment>
                        <div id="detail-plan-container" className="detail-plan-container">

                        <div className="detail-cmp-info">
                            {this.state.plansAndFeaturesInfo ? <h1>{this.state.plansAndFeaturesInfo}</h1>:
                                <React.Fragment>
                                <h1>&nbsp;</h1>
                                </React.Fragment>
                            }
                        </div>

                            <div className="pure-g dtl-wrp">

                                <div class="pure-u-1-4 card category-feature-name ctg-wrp dtl-hdr">&nbsp;</div>

                                {detailRows}

                            </div>

                            {categoryFeatures}

                            <br />
                            <div className="pure-g">

                                <div class="pure-u-1-4 card category-feature-name ctg-wrp dtl-hdr">
                                    {/* <button className="back-to-plans-btn" onClick={() => this.handleClick()}>
                    <svg width="30px" height="30px" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path d="M13 16l-6-6 6-6" fill="none" stroke="red" stroke-width="1.03"/>
                    </svg>
                    <a href="#" className="back-btn-action-link-lg-dtl">{this.state.tiers[0].toggleText}</a>
                    </button> */}
                                    {/* <button className="tier-actn-bck" onClick={() => this.props.handleClick()}>
                                        <span className="tier-actn-link">
                                            <svg class="bck-svg" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                                <path d="M13 16l-6-6 6-6" fill="none" stroke="red" stroke-width="1.03" />
                                            </svg>
                                            {this.props.toggleText}
                                        </span>
                                    </button> */}
                                    &nbsp;
                                </div>
                                {tierActions}

                            </div>

                            <br />

                        </div>
                    </React.Fragment>
                }
            </React.Fragment>
        )
    }
}

// used in accordion description for category
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

                        {j == 0 && item.values[val] ?
                            <span className="ctg-name-wrp">{category.name}</span>
                            : ''}
                        <div className="plan-desc-feature">
                            <div sm="2" className="category-feature-xs">
                                {/* if value is blank, do not show, */}
                                {/* if value is yes show it */}
                                {/* if value if custom text, it is as is */}
                                <div>
                                {item.values[val] && item.values[val].toLowerCase() != "yes" ? 
                                    <span>{item.values[val]}&nbsp;{item.name}&nbsp;</span> : 
                                    item.values[val] && item.values[val].toLowerCase() == "yes" ? <span>{item.name}&nbsp;</span> :
                                    // <span>&nbsp;</span>    
                                    ''
                                }
                                { 
                                    item.values[val] && item.info ?
                                        <Tooltip message={item.info} position={'top'}>
                                            <span>
                                                <svg class="accrdn-ttp-svg" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">

                                                    <path d="M12.13 11.59c-.16 1.25-1.78 2.53-3.03 2.57-2.93.04.79-4.7-.36-5.79.56-.21 1.88-.54 1.88.44 0 .82-.5 1.74-.74 2.51-1.22 3.84 2.25-.17 2.26-.14.02.03.02.17-.01.41-.05.36.03-.24 0 0zm-.57-5.92c0 1-2.2 1.48-2.2.36 0-1.03 2.2-1.49 2.2-.36z" />
                                                    <circle cx="10" cy="10" r="9" fill="none" stroke="currentColor" stroke-width="1.1" />
                                                </svg>
                                            </span>
                                        </Tooltip> : '' 
                                }
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
            accordionPlans: plansAndFeatures,
            contactFormData: contactForm
        };
    }

    yearlyToggle() {
        // console.log("in yearlyToggle func, this.state", this.state);
        this.setState({
            showMonthlyPlan: !this.state.showMonthlyPlan
        })
    }

    render() {

        let plansAccordion = [];

        this.props.tiers.forEach((tier, i) => {

            // console.log("this.props.showMonthlyPlan", this.props.showMonthlyPlan);

            plansAccordion.push(
                <AccordionItem key={tier.name}>
                    {/* {this.props.showMonthlyPlan ? */}
                    <React.Fragment>
                        <AccordionItemHeading>
                            <AccordionItemButton>
                                {/* get this data from tiers uusing index reference whilst iterating over plans_and_features */}
                                <span className="plan-name">{tier.name}</span>

                                <h2 className="product-price product-price-sm">

                                    <React.Fragment>
                                        {(tier.showCallToAction && tier.showCallToAction == "True") ?
                                            <React.Fragment>
                                                {/* <button className="contact-us-btn-xs" onClick={() => this.props.contactFormToggle()}>
                                                            <div className="contact-action-label">{tier.contactFormText}</div>
                                                        </button> */}
                                            </React.Fragment> :
                                            <React.Fragment>
                                                {this.props.showMonthlyPlan ?
                                                    <React.Fragment>
                                                        <span className="currency" data-alt-text="$">{tier.pricing.monthly.currency}</span>
                                                        <span className="price" data-alt-text="79">{tier.pricing.monthly.price}</span>
                                                        <span className="period">{tier.pricing.monthly.label}</span>
                                                    </React.Fragment> :
                                                    <React.Fragment>
                                                        <span className="currency" data-alt-text="$">{tier.pricing.yearly.currency}</span>
                                                        <span className="price" data-alt-text="79">{tier.pricing.yearly.price}</span>
                                                        <span className="period">{tier.pricing.monthly.label}</span>
                                                    </React.Fragment>
                                                }
                                            </React.Fragment>
                                        }
                                    </React.Fragment>
                                </h2>
                            </AccordionItemButton>
                        </AccordionItemHeading>
                        <AccordionItemPanel className="accrd-panel-wrp">
                        {(tier.showCallToAction && tier.showCallToAction == "True") ?
                                <React.Fragment>
                                    {/* if  tier.call_to_action.type is CONTACT, add contactFormToggle func */}
                                    {(tier.call_to_action.type == "contact") ?
                                        // add contact page toggle if type is contact
                                        <button className="contact-us-btn" onClick={() => this.props.contactFormToggle()}>
                                            {/* <div className="contact-action-label">{tier.contactFormText}</div> */}
                                            <span className="contact-action-label">{tier.call_to_action.text}</span>
                                        </button>
                                        :
                                        <React.Fragment>
                                            {/* if tier.call_to_action.type is sign-up-free, call to action is of type link */}
                                        {(tier.call_to_action.type == "link") ?
                                            <a href={tier.call_to_action.url} className="contact-us-btn">
                                                {/* <div className="contact-action-label">{tier.contactFormText}</div> */}
                                                <span className="contact-action-label">{tier.call_to_action.text}</span>
                                            </a> : '' }
                                        </React.Fragment>
                                    }
                                </React.Fragment> :
                                <React.Fragment>
                                    {/* get this from tiers as well */}
                                    {this.props.showMonthlyPlan ?
                                        <p className="text-light-gray">{tier.pricing.monthly.currency}{tier.pricing.yearly.price} {this.props.tiers.monthlyText} <div className="yearly" onClick={() => this.props.yearlyToggle()}> {this.props.tiers.payText}</div></p>
                                        :
                                        <p className="text-light-gray">{tier.pricing.monthly.currency}{tier.pricing.yearly.perAnnum} {this.props.tiers.yearlyText1}<br /> {this.props.tiers.yearlyText2} {tier.pricing.monthly.currency}{tier.pricing.yearly.savedAmount}{tier.pricing.yearly.label}</p>
                                    }
                                    <p>{tier.description}</p>
                                    <a href={tier.call_to_action.url} className="sign-up-btn-xs">
                                        <span className="action-link">{tier.call_to_action.text}</span>
                                    </a>
                                </React.Fragment>
                            }
                            {/* get this from plans_and_features.js */}
                            <CategoryFeatures categories={this.props.accordionPlans.categories} plan_name={tier.name} />
                        </AccordionItemPanel>
                    </React.Fragment>
                    {/* :
                        <React.Fragment>
                        //     <AccordionItemHeading>
                        //         <AccordionItemButton>
                        //             {/* get this data from tiers uusing index reference whilst iterating over plans_and_features 
                        //             <span className="plan-name">{tier.name}</span>
                        //             <h2 className="product-price product-price-sm">
                        //                 <span className="currency" data-alt-text="$">{tier.pricing.yearly.currency}</span>
                        //                 <span className="price" data-alt-text="79">{tier.pricing.yearly.price}</span>
                        //                 <span className="period">{tier.pricing.monthly.label}</span>
                        //             </h2>
                        //         </AccordionItemButton>
                        //     </AccordionItemHeading>
                        //     <AccordionItemPanel style={{ background: '#fff', textAlign: 'center' }}>
                        //         <p className="text-light-gray">{tier.pricing.monthly.currency}{tier.pricing.yearly.perAnnum} {this.props.tiers[0].yearlyText1}<br /> {this.props.tiers[0].yearlyText2} {tier.pricing.monthly.currency}{tier.pricing.yearly.savedAmount}{tier.pricing.yearly.label}</p>
                        //         <p>{tier.description}</p>
                        //         <button className="sign-up-btn-xs">
                        //             <a href={tier.call_to_action.url} className="action-link">{tier.call_to_action.text}</a>
                        //         </button>
                        //         <CategoryFeatures categories={this.props.accordionPlans.categories} plan_name={tier.name} />
                        //     </AccordionItemPanel>
                        // </React.Fragment>  */}

                    <br />
                </AccordionItem>
            );
        })

        return (
            <React.Fragment>
                {this.props.showContactForm ?
                    // <div className="contact-form-container">
                    <ContactForm contactFormData={this.state.contactFormData} contactFormToggle={() => this.props.contactFormToggle()}
                        submitContactForm={() => this.props.submitContactForm()} accordionView={true} />
                    // {/* </div> */}
                    :
                    <Accordion allowZeroExpanded={true}>
                        {plansAccordion}
                    </Accordion>
                }
            </React.Fragment>
        );
    }
};

class PricingPage extends React.Component {

    constructor (props) {
        super(props);

        this.state = {
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
    }

    handleClick() {

        // this.setState({ showDetailedPlanOveriew: !this.state.showDetailedPlanOveriew });
    }

    radioChange(e) {
        this.setState({
            // selectedOption: e.currentTarget.value,
            selectedOption: !this.state.selectedOption,
            showMonthlyPlan: !this.state.showMonthlyPlan
        });
    }

    yearlyToggle() {
        // console.log("in yearlyToggle func, this.state", this.state);
        this.setState({
            selectedOption: !this.state.selectedOption,
            showMonthlyPlan: !this.state.showMonthlyPlan
        })
    }

    contactFormToggle() {
        // console.log("in contactFormToggle func, this.state", this.state);
        window.scrollTo(180, 180);
        this.setState({
            showContactForm: !this.state.showContactForm
        })
    }

    submitContactForm() {
        // console.log("submit form clicked");
    }

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


    render() {

        return (
            <div className="simple-detail-plan-tier-sm-md-lg">

                {!this.state.showContactForm && this.state.showRadioOptions ?
                    <div className="pure-g">
                        <div className="pure-u-1-2 input-radio-plan input-radio-plan-monthly">
                            <input type="radio"
                                value={true}
                                checked={this.state.selectedOption == true}
                                onChange={($event) => this.radioChange($event)} />&nbsp;<span>{this.state.radio_btn_monthly_opt}</span>
                        </div>
                        <div className="pure-u-1-2 input-radio-plan input-radio-plan-yearly">
                            <input type="radio"
                                value={false}
                                checked={this.state.selectedOption == false}
                                onChange={($event) => this.radioChange($event)} />&nbsp;<span className="radio-btn-wrp">{this.state.radio_btn_yearly_opt}</span>
                        </div>
                    </div> : ''}
                <br />

                {/* {!this.state.showDetailedPlanOveriew
                    ? */}
                    <React.Fragment>

                        <div className="accrd-view">
                            <PlansAccordion className="accordion-plan-tier" accordionPlans={this.state.accordionPlans}
                                showMonthlyPlan={this.state.showMonthlyPlan}
                                tiers={this.state.tiers}
                                yearlyToggle={() => this.yearlyToggle()}
                                contactFormToggle={() => this.contactFormToggle()}
                                showContactForm={this.state.showContactForm}
                                submitContactForm={() => this.submitContactForm()}
                            />
                        </div>

                        {/* <div className="pure-g"> */}
                            {/* <div className="pure-u-1"> */}
                            <SimplePlanTier onClick={() => this.handleClick()}
                                className="plan-tier" 
                                showMonthlyPlan={this.state.showMonthlyPlan}
                                yearlyToggle={() => this.yearlyToggle()}
                                contactFormToggle={() => this.contactFormToggle()}
                                showContactForm={this.state.showContactForm}
                                submitContactForm={() => this.submitContactForm()} />
                            {/* </div> */}
                            {/* <div className="pure-u-1"> */}

                            <DetailedPlanTier 
                                showMonthlyPlan={this.state.showMonthlyPlan}
                                showContactForm={this.state.showContactForm}
                                tiers={this.state.tiers}
                                categories={this.state.categories}
                                tierActions={this.state.tierActions}
                                yearlyToggle={() => this.yearlyToggle()}
                                contactFormToggle={() => this.contactFormToggle()}
                                submitContactForm={() => this.submitContactForm()} 
                                handleClick={() => this.handleClick()}
                                contactFormData={this.state.contactFormData} />     
                            {/* </div> */}
                        {/* </div> */}

                    </React.Fragment>
                    {/* :
                    <React.Fragment>

                        <div className="accrd-view">
                            <PlansAccordion className="accordion-plan-tier" accordionPlans={this.state.accordionPlans}
                                showMonthlyPlan={this.state.showMonthlyPlan}
                                tiers={this.state.tiers}
                                yearlyToggle={() => this.yearlyToggle()}
                                contactFormToggle={() => this.contactFormToggle()}
                                showContactForm={this.state.showContactForm}
                                submitContactForm={() => this.submitContactForm()}
                            />
                        </div> */}
                        {/* <React.Fragment>
                            {this.state.showContactForm ?

                                <React.Fragment>
                                    <div className="detail-plan-container contact-form-container-dtl">
                                        <ContactForm contactFormData={this.state.contactFormData}
                                            contactFormToggle={() => this.contactFormToggle()}
                                            submitContactForm={() => this.submitContactForm()} />
                                    </div>
                                </React.Fragment> :
                                <React.Fragment>
                                    <div className="detail-plan-container">

                                        <div className="pure-g" style={{ marginBottom: '-60px' }}>

                                            <div class="pure-u-1-4">&nbsp;</div>

                                            {detailRows}

                                        </div>

                                        {categoryFeatures}

                                        <br />
                                        <div className="pure-g">

                                            <div class="pure-u-1-4 card-actn category-feature-actn" style={{ textAlign: 'center' }}>
                                                {/* <button className="back-to-plans-btn" onClick={() => this.handleClick()}>
                                        <svg width="30px" height="30px" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M13 16l-6-6 6-6" fill="none" stroke="red" stroke-width="1.03"/>
                                        </svg>
                                        <a href="#" className="back-btn-action-link-lg-dtl">{this.state.tiers[0].toggleText}</a>
                                        </button> */}
                                                {/* <button className="tier-actn-bck" onClick={() => this.handleClick()}>
                                                    <svg width="30px" height="30px" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                                        <path d="M13 16l-6-6 6-6" fill="none" stroke="red" stroke-width="1.03" />
                                                    </svg>
                                                    <a href="#" className="tier-actn-link">{this.state.toggleText}</a></button>
                                            </div>
                                            {tierActions}

                                        </div>

                                        <br />

                                    </div>
                                </React.Fragment>
                            }
                        </React.Fragment>  */}
                    {/* </React.Fragment> */}
                {/* // } */}
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