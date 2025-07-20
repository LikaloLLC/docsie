// Real G2 Reviews Data for Docsie
const g2Reviews = [
  {
    id: 1,
    name: "Nora D.",
    title: "Cyber Security Business Analyst",
    company: "Enterprise (> 1000 emp.)",
    rating: 5,
    date: "2/21/2023",
    review: "Docsie revolutionized our communication, documentation, and onboarding.",
    fullReview: "As an IT professional, I highly appreciate the functionality of linking and categorizing documents provided by our documentation company. The ability to consolidate essential information and processes in a single location accessible by both new and existing team members is invaluable."
  },
  {
    id: 2,
    name: "Anne T.",
    title: "Business Data Analyst", 
    company: "Enterprise (> 1000 emp.)",
    rating: 5,
    date: "2/15/2023",
    review: "Effortlessly Organize and Manage Content",
    fullReview: "I'm delighted to share my positive experience with Docsie! The rich text editor is superb and makes creating content a breeze. The feature that stands out the most to me is the history of changes, which has been a lifesaver on more than one occasion."
  },
  {
    id: 3,
    name: "Jose T.",
    title: "Business System Analyst",
    company: "Enterprise (> 1000 emp.)",
    rating: 4.5,
    date: "3/1/2023",
    review: "Highly recommend tool for creating a company knowledge base",
    fullReview: "I find Docsie to be a valuable tool due to its highly adaptable page layout and diverse range of functions available. With such flexibility, the possibilities for content creation are virtually limitless."
  },
  {
    id: 4,
    name: "Oren S.",
    title: "Account Manager",
    company: "Small-Business (50 or fewer emp.)",
    rating: 5,
    date: "8/12/2022",
    review: "Awesome platform and even better team of engineers supporting it",
    fullReview: "Flexible platform that is capable of lot custom features including images, dynamic content and complex nesting of our detailed datasheets. The best part is the team that supports Docsie. They are responsive, professional and able to take our input and turn it into results."
  },
  {
    id: 5,
    name: "Lindsay T.",
    title: "Information Technology Business Analyst",
    company: "Enterprise (> 1000 emp.)",
    rating: 5,
    date: "11/8/2022",
    review: "I still believe Docsie is fantastic!",
    fullReview: "Docsie is simple to use and integrates search with our process, making it simple to access information no matter where it is stored."
  },
  {
    id: 6,
    name: "Shelley L.",
    title: "Software Engineer",
    company: "Enterprise (> 1000 emp.)",
    rating: 5,
    date: "5/19/2022",
    review: "Beautiful product for creating docs fast!",
    fullReview: "There are a lot of features available in Docsie. Effective organisation, solid search, rich and attractive content, and a good model for sharing and permissions all contribute to a positive user experience. It is much faster than other wikis that provide a large number of features."
  },
  {
    id: 7,
    name: "Roxy R.",
    title: "Business Analyst",
    company: "Enterprise (> 1000 emp.)",
    rating: 5,
    date: "7/13/2022",
    review: "Fantastic, and fun to use doc creation tool!",
    fullReview: "Docsie team, you so much for creating an awesome documentation creation product! From end to end flow Docsie allows you to create, publish and maintain awesome looking documentation!"
  },
  {
    id: 8,
    name: "Jennifer K.",
    title: "Business Analyst",
    company: "Enterprise (> 1000 emp.)",
    rating: 5,
    date: "4/25/2022",
    review: "Docsie is required for awesome docs!",
    fullReview: "The simplest solution is always the best solution for a problem. My confidence in my ability to figure out how to create awesome docs has grown over the course of just a few weeks of using this tool Everything about this is amazing."
  },
  {
    id: 9,
    name: "Ghina S.",
    title: "Business Analyst",
    company: "Enterprise (> 1000 emp.)",
    rating: 4.5,
    date: "6/8/2022",
    review: "Excellent tool for knowledge sharing!",
    fullReview: "The tool's simplicity of use. It is incredibly intuitive and simple to use, which means that the entire team can access and utilise the system with little or no training."
  },
  {
    id: 10,
    name: "Linda J.",
    title: "User Experience Designer",
    company: "Small-Business (50 or fewer emp.)",
    rating: 5,
    date: "2/8/2022",
    review: "We love Docsie!",
    fullReview: "The ease with which it may be used. The UI is very user-friendly and simple to understand. Members of the team with no prior knowledge base creation experience have been able to grasp the concept quickly after a short training session."
  },
  {
    id: 11,
    name: "Diane S.",
    title: "Project Manager",
    company: "Small-Business (50 or fewer emp.)",
    rating: 5,
    date: "12/8/2021",
    review: "Life saver tool for client-side documentation!",
    fullReview: "Docsie has many amazing qualities. It publishes simple yet dynamic design documentation, which are easy to create, and has so many plugins to make them meet all requirements."
  },
  {
    id: 12,
    name: "Shannon R.",
    title: "Senior Business Analyst",
    company: "Small-Business (50 or fewer emp.)",
    rating: 5,
    date: "8/11/2021",
    review: "Great Documentation and Knowledge Management Solution. Awesome Support!",
    fullReview: "It's fast. We were able to get the portal hosted on the custom domain for free. The app works well and is conducive to collaboration between the teams. Docsie offers a lot of functionality for a low cost."
  }
];

// Function to get random reviews
function getRandomReviews(count = 3) {
  const shuffled = [...g2Reviews].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
}

// Function to get initials from name
function getInitials(name) {
  return name.split(' ').map(word => word.charAt(0)).join('');
}

// Function to render star rating
function renderStarRating(rating) {
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 !== 0;
  let starsHtml = '';
  
  for (let i = 0; i < fullStars; i++) {
    starsHtml += '<svg class="w-5 h-5 text-yellow-400 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>';
  }
  
  if (hasHalfStar) {
    starsHtml += '<svg class="w-5 h-5 text-yellow-400 fill-current" viewBox="0 0 20 20"><defs><linearGradient id="half-star"><stop offset="50%" stop-color="#fbbf24"/><stop offset="50%" stop-color="#d1d5db"/></linearGradient></defs><path fill="url(#half-star)" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>';
  }
  
  return starsHtml;
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { g2Reviews, getRandomReviews, getInitials, renderStarRating };
}