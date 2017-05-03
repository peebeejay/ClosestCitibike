# Closest Citibike

## Minimum Viable Product

This project will entail a significant refactor of a project I previously built named Closest Citibike. The goal of this refactor is to integrate skills and libraries I've learned over the past few weeks into the existing project.

Overall, Closest Citibike has two primary parts, a web interface that allows users to find the closest citibike stations and display the stations on a map, and a Facebook Messenger chatbot that performs a similar task.

Sub features would include the ability to view color-coded markers on a map that distinguishes the top 5 station choices from the rest based on your location; the ability to toggle between # available docks & # available bikes.

- [ ] Web Interface with Google Maps
- [ ] Facebook Messenger Chatbot
- [ ] Production README

## Technologies, Libraries, APIs

The current version of the application uses Python / Flask as its backend. This could be updated to use RoR / Sinatra and ruby in order to better integrate with the overall theme of our porfolios. At the same time, retaining python and refactoring could indicate a diverse skillset.

The front-end current uses vanilla js. I would like to upgrade the site to use jQuery for AJAX requests at the very least. React-Redux may be overkill in this situation, but could potentially lead to more elegant code.

The application will also make use of the Citibike API for bike data, and the Google Maps API, specifically the map itself in addition to the geocoding & reverse-geocoding functions. It will also use the Facebook Messenger API to interact with FB Messenger.

Some technical challenges that remain are displaying markers in a aesthetically pleasing, yet non-overwhelming way on the map.

Other challenges would be to rewrite the front-end to not use bootstrap, re-style the front-end in a more aesthetically pleasing way, & integrate Heroku SSL,

## Wireframes

The existing site can be used as a proxy for wireframes, namely, please visit closestcitibike.com

## Implementation Timeline

### Phase 1
1. Re-build the app as either a RoR React-Redux app, or a Flask React-Redux app
2. Build the map functionality
3. markers
4. Search
5. Styling throughout

### Phase 2
1. Facebook Messenger functionality
