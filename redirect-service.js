let ep = 'https://us-central1-docsie-io.cloudfunctions.net/geo-ip';
function getLocation() {
    fetch(ep, {
      headers: {
        'Content-Type': 'application/json'
      },
    })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      if (data.country.toLowerCase() == "us") {
        let redirectedPath =  window.location.origin + "/us" + window.location.pathname;
        window.location.href = redirectedPath;
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      window.location.href = "https://www.docsie.io/us/";
    });
  }
getLocation();