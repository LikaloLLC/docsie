
  // Update prices based on toggle state
  function updatePrices(isAnnual) {
    const plans = {
      'standard': { monthly: 45, yearly: 399 },
      'premium': { monthly: 199, yearly: 2040 },
      'business': { monthly: 449, yearly: 2988 },
      'organization': { monthly: 900, yearly: 8388 }
    };
    
    Object.keys(plans).forEach(planId => {
      const priceEl = document.getElementById(`${planId}-price`);
      const periodEl = document.getElementById(`${planId}-period`);
      const billingEl = document.getElementById(`${planId}-billing`);
      
      if (priceEl && periodEl && billingEl) {
        if (isAnnual) {
          const monthlyEquivalent = Math.round(plans[planId].yearly / 12);
          priceEl.textContent = '$' + monthlyEquivalent;
          periodEl.textContent = '/per month';
          billingEl.textContent = 'billed annually';
        } else {
          priceEl.textContent = '$' + plans[planId].monthly;
          periodEl.textContent = '/per month';
          billingEl.textContent = 'billed monthly';
        }
      }
    });
    
    // Update label styles
    if (isAnnual) {
      monthlyLabel.className = 'px-4 py-2 text-sm font-medium text-gray-600';
      annualLabel.className = 'px-4 py-2 text-sm font-medium text-blue-600 font-semibold';
    } else {
      monthlyLabel.className = 'px-4 py-2 text-sm font-medium text-blue-600 font-semibold';
      annualLabel.className = 'px-4 py-2 text-sm font-medium text-gray-600';
    }
  }