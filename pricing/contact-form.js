var contactForm = {
    "heading": "Contact Enterprise Sales",
    "sub_info": "Let's tallk entreprise.",
    "toggleContactFormText": "Go Back",
    "submitContactFormText": "Submit Form",
    "formInputs": [
        {
            "label": "Business Email",
            "alias": "businessEmail",
            "type": "text",
            "placeholder": "enter your business email"
        },
        {
            "label": "Industry",
            "alias": "industry",
            "type": "dropdown",
            "placeholder": "enter your industry",
            "options": [
                "Technology",
                "Other"
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
                    "value": "Priority Support and SLA's",
                    "type": "checkbox",
                    "required": true
                },{
                    "value": "AI powered documentation",
                    "type": "checkbox"
                },{
                    "label": "AI powered documentation",
                    "type": "checkbox"
                }, {
                    "label": "Single tenant options",
                    "type": "checkbox"
                }, {
                    "label": "Customer success manager",
                    "type": "checkbox"
                }, {
                    "label": "Private onboarding and training sessions",
                    "type": "checkbox"
                }, {
                    "label": "Private cloud options",
                    "type": "checkbox"
                }, {
                    "label": "Comprehensive project metrics",
                    "type": "checkbox"
                }, {
                    "label": "SAML-based single sign-on (SSO)",
                    "type": "checkbox"
                }, {
                    "label": "Combining multiple projects",
                    "type": "checkbox"
                }, {
                    "label": "Customer OAuth 2 Login",
                    "type": "checkbox"
                }, {
                    "label": "Vendor Security Forms",
                    "type": "checkbox"
                }, {
                    "label": "SLA / ToS modifications",
                    "type": "checkbox"
                }
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
        "description": ""
    }
}