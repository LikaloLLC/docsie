tiers = {
  "Banner": "All features including the most advanced are forever free for open source projects and non-profits, please contact us with your project details",
  "show_radio_options": false,
  "radio_btn_monthly_opt": "Pay monthly",
  "radio_btn_yearly_opt": "Pay yearly (Save up to 30%)",
  "monthlyText": "when you pay yearly",
  "yearlyText": "billed yearly, Save",
  "compareText": "compare plans",
  // "toggleText": "Back to simple plans",
  "tiers": [
    {
      "name": "Large",
      "order": 1,
      "icon": "www.docsie.io/icon.png",
      "description": "Unlimited Feedback Submissions",
      "call_to_action": {
        // use type to make contact page as call to action on click of this
        "type": "contact",
        "text": "Talk to Us",
        "url": "#"
      },
      "popular": "False",
      "popularInfoText": "Most Popular",
      // use the following for showing contact page
      "showCallToAction": "True"
    },
    {
      "pricing": {
        "monthly": {
          "price": "28,000",
          "currency": "₹",
          "label": "/month"
        },
        "yearly": {
          "price": "23,000",
          "currency": "₹",
          "perAnnum": "283,248",
          "savedAmount": "5000",
          "label": "/month"
        }
      },
      "name": "Medium",
      "icon": "www.docsie.io/icon.png",
      "order": 2,
      "description": "Up to 50,000 feedback submissions per month.",
      "call_to_action": {
        "type": "pricing",
        "text": "Try it Free!",
        "url": "https://app.docsie.io/login/?dal=feedback&utm=Medium"
      },
      "showCallToAction": "False"
    },
    {
      "pricing": {
        "monthly": {
          "price": "5000",
          "currency": "₹",
          "label": "/month"
        },
        "yearly": {
          "price": "3500",
          "currency": "₹",
          "perAnnum": "42,000",
          "savedAmount": "1500",
          "label": "/month"
        }
      },
         "name": "Small",
         "icon" : "www.docsie.io/icon.png",
         "order": 4,
         "description": "Up to 5000 feedbacks submited per month.",
         "call_to_action" : {
            // use type to
            "type": "pricing",
            "text":"Sign-up Free!",
            "url": "https://app.docsie.io/login/?dal=feedback&utm=Small"
          },
          "showCallToAction": "False"
      }
  ]
}
