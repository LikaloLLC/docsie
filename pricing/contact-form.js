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
            "placeholder": "enter your first name",
            "required": true
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
            "type": "text",
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
            ],
            // "required": true
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
                }, {
                    "value": "Single tenant options",
                    "type": "checkbox"
                }, {
                    "value": "Customer success manager",
                    "type": "checkbox"
                }, {
                    "value": "Private onboarding and training sessions",
                    "type": "checkbox"
                }, {
                    "value": "Private cloud options",
                    "type": "checkbox"
                }, {
                    "value": "Comprehensive project metrics",
                    "type": "checkbox"
                }, {
                    "value": "SAML-based single sign-on (SSO)",
                    "type": "checkbox"
                }, {
                    "value": "Combining multiple projects",
                    "type": "checkbox"
                }, {
                    "value": "Customer OAuth 2 Login",
                    "type": "checkbox"
                }, {
                    "value": "Vendor Security Forms",
                    "type": "checkbox"
                }, {
                    "value": "SLA / ToS modifications",
                    "type": "checkbox"
                }, {
                    "value": "Translations",
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