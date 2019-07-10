tiers = {
  "Banner": "All features including the most advanced are forever free for open source projects, please contact us with your project details",
  "radio_btn_monthly_opt": "Pay monthly",
  "radio_btn_yearly_opt": "Pay yearly (Save up to 30%)",
  "monthlyText": "when you pay yearly",
  "yearlyText": "billed yearly, Save",
  "compareText": "compare plans",
  // "toggleText": "Back to simple plans",
  "tiers": [
    {
      "name": "Enterprise",
      "order": 1,
      "icon": "www.docsie.io/icon.png",
      "description": "Powerful features to accelerate your enterprise documentation.",
      "call_to_action": {
        // use type to make contact page as call to action on click of this
        "type": "contact",
        "text": "Get Started",
        "url": "#"
      },
      "popular": "True",
      "popularInfoText": "Most Popular",
      // use the following for showing contact page 
      "showCallToAction": "True"
    },
    // {
    //   "pricing": {
    //     "monthly": {
    //       "price": "7.00",
    //       "currency": "$",
    //       "label": "/user"
    //     },
    //     "yearly": {
    //       "price": "5.00",
    //       "currency": "$",
    //       "perAnnum": "60",
    //       "savedAmount": "24",
    //       "label": "/user"
    //     }
    //   },
    //   "name": "Business",
    //   "icon": "www.docsie.io/icon.png",
    //   "order": 2,
    //   "description": "Professional features and collaboration for your growing business.",
    //   "call_to_action": {
    //     "type": "pricing",
    //     "text": "Try it Free!",
    //     "url": "https://app.docsie.io/manager/?utm=business"
    //   },
    //   "showCallToAction": "False"
    // },
     {
         "name": "Start-up",
         "icon" : "www.docsie.io/icon.png",
         "order": 4,
         "description": "Professional product documentation tools for an up-and-coming start-up.",
         "call_to_action" : {
            // use type to 
            "type": "link",
            "text":"Sign-up Free!",
            "url": "https://app.docsie.io/manager/?utm=start-up"
          },
          "showCallToAction": "True"
      }
  ],
  //  used in detail view
  "tierActions": [
    {
      "label" : {
                  "name": "Entreprise",
                  "text":"Entreprise Sign-up Now!",
                  "url": "signup.com?utm=3423"
                }
    }
    // , {
    //   "label": {
    //               "name": "Business",
    //               "text": "Business Sign-up Now!",
    //               "url": "signup.com?utm=3423"
    //             }
    // }
    ,
    {
      "label": {
                  "name": "Start-up",
                  "text": "Start-up Sign-up Now!",
                  "url": "signup.com?utm=3423"
                }
    }
  ]
}
