# Commerce

#### Video Demo: [Auctions](https://youtu.be/LuWJ5TnIqdY)

## Problem to Solve

Design an e-commerce auction site that enable users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Understanding

`commerce` is a Django-based web application that mimics an eBay-like auction site, allowing users to create listings, place bids, comment on auctions, and categorize items. The application, located in a Django project called commerce, contains a single app named auctions, which handles all the core functionality of the auction site.

#### URL Configuration:
The URLs for the auctions app are defined in auctions/urls.py. Several default routes are already set up, including:
* `/`: The index route, which serves as the homepage.
* `/login`: A route that allows users to log in.
* `/logout`: A route for logging users out.
* `register`: A route that provides a registration form for new users.
These routes correspond to views defined in auctions/views.py, where the appropriate templates and logic for each action are handled.

#### Views:
* `index` view: The default homepage view that, for now, returns a basic template (index.html), which will later be populated with auction listings.
* `login_view`: This view handles both displaying the login form and authenticating users. When accessed via a GET request, it renders the login form. Upon submission (via POST request), it logs the user in and redirects them to the index page.
*`logout_view`: Logs users out and redirects them to the homepage.
* `register` view: Displays a registration form for new users. When the form is submitted, it creates a new user and logs them in.
The base HTML layout of the application can be found in `auctions/templates/auctions/layout.html`. This template contains logic to display different content depending on whether the user is signed in or not, using the `user.is_authenticated` condition. If a user is logged in, they will see personalized content, such as a “Signed in as” message, and links to features like creating an auction or bidding on items.

#### Models:

In `auctions/models.py`, the data models that define the structure of the auction site are set up. The project already includes a User model that inherits from Django’s built-in `AbstractUser`, which provides essential fields such as username, email, and password.

We will need to define additional models to represent the core functionalities of the auction site:
* Auction Listings: Model to represent items being auctioned, including details such as item title, description, starting bid, current price, and auction status.
* Bids: Model to handle bid placement, tracking the user who placed the bid and the bid amount.
* Comments: Model for users to leave comments on auction listings.
* Categories: Model to categorize auction listings, allowing users to filter items by category.

## Specification
The eBay-like auction site will allow users to create and bid on listings, manage watchlists, add comments, and categorize listings. The application will use Django’s powerful framework to handle user authentication, database management, and the admin interface. Below are the required functionalities and details for the project:

#### Models:
The application will include at least three models in addition to Django’s built-in User model:
* Auction Listings:
    * Title (string)
    * Description (text)
    * Starting bid (decimal)
    * Current price (decimal)
    * Image URL (optional, string)
    * Category (optional, string)
    * Active status (boolean, indicating whether the auction is active)
    * Foreign key to the User model (for the creator of the listing)
* Bids:
    * Bid amount (decimal)
    * Foreign key to the User model (for the bidder)
    * Foreign key to the Auction Listing model (to associate the bid with a specific listing)
* Comments:
    * Comment text (text)
    * Foreign key to the User model (for the commenter)
    * Foreign key to the Auction Listing model (to associate the comment with a specific listing)

#### Create Listing:
Users are able to visit a page to create a new auction listing. The listing creation form allows users to:
* Specify a title.
* Provide a description of the item.
* Set the starting bid.
* Optionally can provide a URL for an image and select a category from predefined options (e.g., Fashion, Electronics, Toys).
Once created, the listing should be saved in the database and become visible on the Active Listings page.

#### Active Listings Page:
The homepage (default route) displays all currently active auction listings.
* Title
* Description
* Current price (updated as bids are placed)
* Image (if one exists for the listing)
Users can click on a listing to view more details on its dedicated listing page.

#### Listing Page:
When a user clicks on a listing, they should be taken to a page specific to that listing. This page should display all relevant details, including:
Title, description, starting bid, current price, and image (if applicable).

For signed-in users:
* Users can add or remove the item from their watchlist.
* Users can place a bid on the item (if the auction is still active). The bid must be greater than the current price or the starting bid (if no bids have been placed yet). An error should be displayed if the bid does not meet these criteria.
* If the user created the listing, they should be able to close the auction, declaring the highest bidder as the winner and marking the listing as no longer active.
* If the user won the auction (i.e., they placed the highest bid on a closed listing), the page should display a message indicating they won the auction.
Users should be able to add comments to the listing page. All comments should be visible under the listing details.

#### Watchlist:
Signed-in users should have access to a Watchlist page that displays all the auction listings they have added to their watchlist.
Users can click on any listing in their watchlist to be taken to the specific listing page.

#### Categories:
A Categories page should display a list of all available categories of auction listings.
Clicking on a category should take the user to a page that displays all active listings in that category.
Each category page should show the same details as the Active Listings page (title, description, current price, and image).

#### Django Admin Interface:
The Django admin interface allows a site administrator to manage auction listings, bids, and comments.
Admins should be able to:
* View, add, edit, and delete any auction listings.
* View, add, edit, and delete any bids made on the site.
* View, add, edit, and delete any comments on auction listings.

## Credit

This problem was originally proposed by [CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/projects/2/commerce/).

