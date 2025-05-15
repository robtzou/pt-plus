# Planet Terp Plus

# How to use: 
    All finalized datasets will be within the data/summaries folder.
    Populate the user interface with data/summaries folder.
    
Project 1: Create a web application that displays all the professors for a course within one page.

The backend of this website has been built purely on generated content from SummLlama3.2 on HuggingFace and information pulled from PlanetTerp.com Public API.

Dev:
# DOM Manipulation Essentials

document.querySelector() and document.querySelectorAll() for selecting elements
element.addEventListener() for handling clicks and form submissions
document.createElement() for creating new task elements
element.appendChild() and parentNode.removeChild() for adding/removing tasks
element.classList.add/remove/toggle() for styling completed tasks

# Event Handling

Form submit events to add new tasks
Click events for completing/deleting tasks
Input events for filtering tasks
Event delegation for handling events on dynamically created elements

# Data Structures & Arrays

Arrays to store task objects/data
Array methods: push(), filter(), map(), forEach()
Creating task objects with properties (id, text, completed status)

# Local Storage

localStorage.setItem() to save tasks as JSON strings
localStorage.getItem() to retrieve saved tasks
JSON.stringify() and JSON.parse() for converting between objects and strings

# Functions

Creating reusable functions for adding, deleting, filtering tasks
Arrow functions for callbacks
Function scope and variables

# Conditional Logic

Using if/else statements for filtering logic
Ternary operators for simple conditions
Checking task status for conditional rendering

# Form Handling

Preventing default form submission with event.preventDefault()
Getting input values with input.value
Form validation (preventing empty tasks)