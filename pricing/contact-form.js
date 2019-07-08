var contactForm = {
    "heading": "Contact Enterprise Sales",
    "sub_info": "Let's tallk entreprise.",
    "toggleContactFormText": "Go Back",
    "submitContactFormText": "Submit Form",
    "endPoint": "https://jsonplaceholder.typicode.com/posts",
    "disabled": true,
    "formInputs": [
        {
            "label": "Business Email",
            "alias": {
                "label": "businessEmail",
                "valueType": "string"
            },
            "type": "email",
            "placeholder": "enter your business email"
        },
        {
            "label": "Industry",
            "alias": {
                "label": "industry",
                "valueType": "string"
            },
            "type": "dropdown",
            "placeholder": "enter your industry",
            "options": [
                "Technology",
                "Other"
            ]
        },
        {
            "label": "Job Title",
            "alias": {
                "label": "jobTitle",
                "valueType": "string"
            },
            "type": "text",
            "placeholder": "enter your job title"
        }, {
            "label": "No. of employees",
            "alias": {
                "label": "employeesNumber",
                "valueType": "number"
            },
            "type": "number",
            "placeholder": "enter # of employees"
        }, 
        {
            "label": "I'm interested in...",
            "alias": {
                "label": "off_options",
                "valueType": "array",
                "arrayType": "options"
            },
            // type and offer_options array belong to this options type, cannot be changed
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
            ],
            "optionsRequiredMsg": "*Please select atleast one option"
        }, 
        {
            "label": "Description",
            "alias": {
                "label": "description",
                "valueType": "string"
            },
            "type": "text_area",
            "placeholder": "enter your description"
        },
        {
            "label": "requiredFields",
            "alias": {
                "label": "requiredFields",
                "valueType": "array",
                "arrayType": "requiredFields"
            },
            "requiredFields": [
            "businessEmail",
            "Priority Support and SLA's"
            ]
        }
    ]
} 