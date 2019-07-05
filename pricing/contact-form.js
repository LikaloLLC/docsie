var contactForm = {
    "heading": "Contact Enterprise Sales",
    "sub_info": "Let's tallk entreprise.",
    "toggleContactFormText": "Go Back",
    "submitContactFormText": "Submit Form",
    "formInputs": [
        {
            "label": "First Name",
            "alias": "firstName",
            "type": "text",
            "placeholder": "enter your first name"
        }, {
            "label": "Last Name",
            "alias": "lastName",
            "type": "text",
            "placeholder": "enter your last name"
        }, {
            "label": "Company Name",
            "alias": "companyName",
            "type": "text",
            "placeholder": "enter your company name"
        }, 
        {
            "label": "Business Email",
            "alias": "businessEmail",
            "type": "email",
            "placeholder": "enter your business email"
        },
        {
            "label": "Industry",
            "alias": "industry",
            "type": "dropdown",
            "placeholder": "enter your industry",
            "options": [
                "opt1",
                "opt2"
            ]
        },
        {
            "label": "Job Title",
            "alias": "jobTitle",
            "type": "text",
            "placeholder": "enter your job title"
        }, {
            "label": "No. of employees",
            "alias": "employeesNumber",
            "type": "number",
            "placeholder": "enter # of employees"
        }, 
        {
            "label": "I'm interested in...",
            "alias": "offer_options",
            "type": "offer_options",
            "offer_options": [
                {
                    "alias": "Priority Support and SLA's",
                    "value": "Priority Support and SLA's",
                    "type": "checkbox"
                }, {
                    "alias": "AI powered documentation",
                    "value": "AI powered documentation",
                    "type": "checkbox"
                }
                // , {
                //     "alias": "Single tenant options",
                //     "value": "Single tenant options",
                //     "type": "checkbox"
                // }, {
                //     "alias": "Customer success manager",
                //     "value": "Customer success manager",
                //     "type": "checkbox"
                // }, {
                //     "alias": "Private onboarding and training sessions",
                //     "value": "Private onboarding and training sessions",
                //     "type": "checkbox"
                // }, {
                //     "alias": "Private cloud options",
                //     "value": "Private cloud options",
                //     "type": "checkbox"
                // }, {
                //     "alias": "Comprehensive project metrics",
                //     "value": "Comprehensive project metrics",
                //     "type": "checkbox"
                // }, {
                //     "alias": "SAML-based single sign-on (SSO)",
                //     "value": "SAML-based single sign-on (SSO)",
                //     "type": "checkbox"
                // }, {
                //     "alias": "Combining multiple projects",
                //     "value": "Combining multiple projects",
                //     "type": "checkbox"
                // }, {
                //     "alias": "Customer OAuth 2 Login",
                //     "value": "Customer OAuth 2 Login",
                //     "type": "checkbox"
                // }, {
                //     "alias": "Vendor Security Forms",
                //     "value": "Vendor Security Forms",
                //     "type": "checkbox"
                // }, {
                //     "alias": "SLA / ToS modifications",
                //     "value": "SLA / ToS modifications",
                //     "type": "checkbox"
                // }, {
                //     "alias": "Translations",
                //     "value": "Translations",
                //     "type": "checkbox"
                // }
            ],
            "optionsRequiredMsg": "*Please select atleast one option"
        }, 
        {
            "label": "Description",
            "alias": "description",
            "type": "text_area",
            "placeholder": "enter your description"
        }
    ],
    // this is used to set form initial state, alias names are put in here
    "formState": {
        "firstName": "",
        "lastName": "",
        "companyName": "",
        "businessEmail": "",
        "industry": "", 
        "jobTitle": "",
        "employeesNumber": "",
        "offer_options": [],
        "description": "",
        "requiredFields": [
            "firstName",
            "businessEmail",
            "Priority Support and SLA's"
        ],
        // this is used to disable submit button
        "disabled": true,
        // use this for contact post request endpoint
        "endPoint": "https://jsonplaceholder.typicode.com/posts"
    },
    
} 